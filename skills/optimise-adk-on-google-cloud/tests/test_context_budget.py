"""Offline checks for the saved-session context budget helper.

Synthetic fixtures only. These tests establish the helper's reporting over
saved JSON, not provider token counts, compaction quality or any live session.
"""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "context_budget.py"
SPEC = importlib.util.spec_from_file_location("context_budget", SCRIPT)
budget = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(budget)

SECRET = "SYNTHETIC_SECRET_VALUE"


def event(invocation, author, parts, timestamp, **more):
    return {"invocationId": invocation, "author": author, "timestamp": timestamp,
            "content": {"role": "user" if author == "user" else "model", "parts": parts}, **more}


def usage(prompt, candidates, cached=None):
    value = {"promptTokenCount": prompt, "candidatesTokenCount": candidates}
    if cached is not None:
        value["cachedContentTokenCount"] = cached
    return value


def clean_session(result_text="rows: 1, 2, 3"):
    return {"id": "synthetic-session", "events": [
        event("inv-1", "user", [{"text": f"first question {SECRET}"}], 1.0),
        event("inv-1", "agent", [{"functionCall": {"id": "c1", "name": "get_rows", "args": {"n": 3}}}], 2.0),
        event("inv-1", "agent", [{"functionResponse": {"id": "c1", "name": "get_rows",
               "response": {"status": "success", "result": result_text}}}], 3.0),
        event("inv-1", "agent", [{"text": "three rows"}], 4.0, finishReason="STOP",
              usageMetadata=usage(120, 8, 0)),
        event("inv-2", "user", [{"text": "second question"}], 5.0),
        event("inv-2", "agent", [{"text": "answer two"}], 6.0, finishReason="STOP",
              usageMetadata=usage(140, 5, 96)),
    ]}


class InspectChecks(unittest.TestCase):
    def test_clean_session_reports_pairs_bytes_growth_and_usage(self):
        report = budget.inspect_events(clean_session()["events"], 20000)
        self.assertEqual(report["verdict"], "INSPECTED")
        self.assertEqual(report["events"], 6)
        self.assertEqual([i["invocation_id"] for i in report["invocations"]], ["inv-1", "inv-2"])
        first, second = report["invocations"]
        self.assertEqual(first["events"], 4)
        self.assertEqual(first["function_call_pairs"], 1)
        self.assertEqual(first["orphan_function_calls"], [])
        self.assertEqual(first["orphan_function_responses"], [])
        self.assertGreater(first["bytes_by_part"]["function_response"], 0)
        self.assertGreater(first["bytes_by_part"]["function_call"], 0)
        self.assertEqual(first["bytes_by_part"]["other"], 0)
        self.assertEqual(first["estimated_tokens_by_part"]["text"], first["bytes_by_part"]["text"] // 4)
        self.assertEqual(set(first["bytes_by_author"]), {"user", "agent"})
        self.assertEqual(first["largest_tool_results"][0]["name"], "get_rows")
        self.assertEqual(first["last_usage_metadata"], {
            "prompt_token_count": 120, "candidates_token_count": 8,
            "cached_content_token_count": 0, "event_index": 3})
        self.assertEqual(second["last_usage_metadata"]["cached_content_token_count"], 96)
        self.assertEqual(second["cumulative_bytes"], first["invocation_bytes"] + second["invocation_bytes"])
        self.assertEqual([g["invocation_id"] for g in report["growth"]], ["inv-1", "inv-2"])
        self.assertLess(report["growth"][0]["cumulative_estimated_tokens"],
                        report["growth"][1]["cumulative_estimated_tokens"])
        self.assertEqual(report["compaction"], [])
        self.assertEqual(report["flagged_tool_results"], [])
        self.assertEqual(report["token_estimate_method"], budget.ESTIMATE_METHOD)
        self.assertNotIn(SECRET, json.dumps(report))

    def test_oversized_tool_result_is_flagged_with_name_and_size(self):
        events = clean_session(result_text="x" * 30000)["events"]
        report = budget.inspect_events(events, 20000)
        self.assertEqual(len(report["flagged_tool_results"]), 1)
        flagged = report["flagged_tool_results"][0]
        self.assertEqual((flagged["invocation_id"], flagged["name"]), ("inv-1", "get_rows"))
        self.assertGreater(flagged["bytes"], 30000)
        self.assertEqual(report["invocations"][0]["tool_results_over_limit"], 1)
        self.assertEqual(budget.inspect_events(events, 40000)["flagged_tool_results"], [])

    def test_orphan_call_and_orphan_response_are_reported_separately(self):
        events = clean_session()["events"]
        events[2]["content"]["parts"][0]["functionResponse"]["id"] = "c-other"
        report = budget.inspect_events(events, 20000)
        first = report["invocations"][0]
        self.assertEqual(first["function_call_pairs"], 0)
        self.assertEqual(first["orphan_function_calls"], [{"name": "get_rows", "event_index": 1}])
        self.assertEqual(first["orphan_function_responses"], [{"name": "get_rows", "event_index": 2}])
        del events[2]["content"]["parts"][0]["functionResponse"]["id"]
        del events[1]["content"]["parts"][0]["functionCall"]["id"]
        self.assertEqual(budget.inspect_events(events, 20000)["invocations"][0]["function_call_pairs"], 1)

    def test_compaction_event_reports_span_and_covered_events(self):
        events = clean_session()["events"]
        events.insert(4, {"invocationId": "inv-1", "author": "user", "timestamp": 4.5,
                          "content": None,
                          "actions": {"compaction": {
                              "startTimestamp": 1.0, "endTimestamp": 4.0,
                              "compactedContent": {"role": "user", "parts": [{"text": "SUMMARY"}]}}}})
        report = budget.inspect_events(events, 20000)
        self.assertEqual(len(report["compaction"]), 1)
        span = report["compaction"][0]
        self.assertEqual((span["start_timestamp"], span["end_timestamp"]), (1.0, 4.0))
        self.assertEqual(span["covered_events"], 4)
        self.assertGreater(span["summary_bytes"], 0)
        self.assertEqual(report["invocations"][0]["compaction_events"], 1)
        self.assertEqual(report["invocations"][0]["events"], 5)

    def test_malformed_items_make_report_partial_and_empty_input_invalid(self):
        events = clean_session()["events"] + ["not an event", {"author": "agent", "content": "wrong"}]
        report = budget.inspect_events(events, 20000)
        self.assertEqual(report["verdict"], "PARTIAL")
        self.assertEqual(report["skipped_malformed_items"], 2)
        for bad in ([], "events", {"events": []}, [[]]):
            with self.subTest(bad=bad):
                if bad == [[]]:
                    self.assertEqual(budget.inspect_events(bad, 20000)["verdict"], "PARTIAL")
                    continue
                with self.assertRaises(budget.InvalidInput):
                    budget.inspect_events(bad, 20000)

    def test_load_events_accepts_object_array_and_jsonl(self):
        events = clean_session()["events"]
        self.assertEqual(budget.load_events(json.dumps({"events": events}).encode())[1], "session_object")
        self.assertEqual(budget.load_events(json.dumps(events).encode())[1], "event_array")
        lines, kind = budget.load_events("\n".join(json.dumps(e) for e in events).encode())
        self.assertEqual((len(lines), kind), (6, "jsonl"))
        for raw in (b"", b"\n", b'{"id": 1}', b"not json\n{\"a\": 1}", b"\xff\xfe", b"42"):
            with self.subTest(raw=raw):
                with self.assertRaises(budget.InvalidInput):
                    budget.load_events(raw)


class CommandChecks(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), *arguments],
                              text=True, capture_output=True, timeout=10)

    def test_help_and_bad_arguments(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        self.assertEqual(self.run_cli().returncode, 2)
        result = self.run_cli("--session", "x.json", "--SYNTHETIC_SECRET_FLAG")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)
        for value in ("0", "-5", "many"):
            with self.subTest(value=value):
                self.assertEqual(self.run_cli("--session", "x.json", "--max-result-bytes", value).returncode, 2)

    def test_cli_is_read_only_repeatable_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "session.json"
            path.write_text(json.dumps(clean_session()))
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            first = self.run_cli("--session", str(path))
            second = self.run_cli("--session", str(path), "--dry-run", "--max-result-bytes", "20000")
            self.assertEqual((first.returncode, second.returncode), (0, 0))
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(json.loads(first.stdout)["source_format"], "session_object")
            self.assertNotIn(SECRET, first.stdout + first.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            path.write_text("{not json")
            malformed = self.run_cli("--session", str(path))
            self.assertEqual(malformed.returncode, 1)
            self.assertEqual(json.loads(malformed.stdout)["verdict"], "MALFORMED")
            self.assertNotIn(directory, malformed.stdout + malformed.stderr)
            missing = self.run_cli("--session", str(root / "absent.json"))
            self.assertEqual(missing.returncode, 1)
            events = clean_session()["events"] + [SECRET]
            path.write_text(json.dumps(events))
            partial = self.run_cli("--session", str(path))
            self.assertEqual(partial.returncode, 1)
            self.assertEqual(json.loads(partial.stdout)["verdict"], "PARTIAL")
            self.assertNotIn(SECRET, partial.stdout + partial.stderr)
            link = root / "link.json"
            link.symlink_to(path)
            self.assertEqual(self.run_cli("--session", str(link)).returncode, 1)


if __name__ == "__main__":
    unittest.main()
