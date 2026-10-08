"""Offline checks for the saved-session invocation summary helper.

Synthetic fixtures only. These tests establish the helper's reporting over
saved JSON, not provider usage accounting, billed cost or any live session.
"""

import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "invocation_summary.py"
SPEC = importlib.util.spec_from_file_location("invocation_summary", SCRIPT)
summary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(summary)

SECRET = "SYNTHETIC_SECRET_VALUE"


def event(invocation, author, parts, timestamp, **more):
    return {"invocationId": invocation, "author": author, "timestamp": timestamp,
            "content": {"role": "user" if author == "user" else "model", "parts": parts}, **more}


def usage(prompt, candidates, cached=None, thoughts=None, total=None):
    value = {"promptTokenCount": prompt, "candidatesTokenCount": candidates}
    if cached is not None:
        value["cachedContentTokenCount"] = cached
    if thoughts is not None:
        value["thoughtsTokenCount"] = thoughts
    if total is not None:
        value["totalTokenCount"] = total
    return value


def clean_session():
    return {"id": "synthetic-session", "events": [
        event("inv-1", "user", [{"text": f"first question {SECRET}"}], 1.0),
        event("inv-1", "agent", [{"functionCall": {"id": "c1", "name": "get_rows", "args": {"n": 3}}}], 2.0,
              usageMetadata=usage(100, 10, 0, 5), modelVersion="model-a"),
        event("inv-1", "agent", [{"functionResponse": {"id": "c1", "name": "get_rows",
               "response": {"status": "success", "result": f"rows {SECRET}"}}}], 3.5),
        event("inv-1", "agent", [{"text": "three rows"}], 4.0, finishReason="STOP",
              usageMetadata=usage(120, 8, 96, 2), modelVersion="model-a"),
        event("inv-2", "user", [{"text": "second question"}], 5.0),
        event("inv-2", "agent", [{"text": "answer two"}], 6.0, finishReason="STOP",
              usageMetadata=usage(140, 5), modelVersion="model-b"),
    ]}


def tool_error_session():
    session = clean_session()
    session["events"][2]["content"]["parts"][0]["functionResponse"]["response"] = {
        "error": f"boom {SECRET}", "status": "error"}
    session["events"].append(event("inv-2", "agent", [{"functionCall": {"id": "c2", "name": "send", "args": {}}}], 7.0,
                                   usageMetadata=usage(10, 1)))
    session["events"].append(event("inv-2", "agent", [{"functionResponse": {"id": "c2", "name": "send",
                                   "response": {"status": "FAILED"}}}], 8.0))
    return session


def streaming_session():
    return {"events": [
        event("inv-s", "user", [{"text": "stream it"}], 1.0),
        event("inv-s", "agent", [{"text": "par"}], 1.1, partial=True, usageMetadata=usage(50, 2)),
        event("inv-s", "agent", [{"text": "partial"}], 1.2, partial=True, usageMetadata=usage(50, 4)),
        event("inv-s", "agent", [{"text": "partial answer"}], 1.3, finishReason="STOP",
              usageMetadata=usage(50, 6), modelVersion="model-a"),
        event("inv-t", "user", [{"text": "again"}], 2.0),
        event("inv-t", "agent", [{"text": "a"}], 2.1, partial=True, usageMetadata=usage(70, 3)),
        event("inv-t", "agent", [{"text": "ab"}], 2.2, partial=True, usageMetadata=usage(70, 9)),
        event("inv-t", "agent", [{"text": "abc"}], 2.3, finishReason="STOP"),
    ]}


PRICES = {"currency": "USD", "per_million": {
    "model-a": {"input": 1.0, "output": 4.0, "cached_input": 0.25},
    "default": {"input": 2.0, "output": 8.0},
}}


class InspectChecks(unittest.TestCase):
    def test_clean_session_counts_calls_tools_usage_and_timing(self):
        report = summary.inspect_events(clean_session()["events"])
        self.assertEqual(report["verdict"], "INSPECTED")
        self.assertEqual([row["invocation_id"] for row in report["invocations"]], ["inv-1", "inv-2"])
        first, second = report["invocations"]
        self.assertEqual((first["model_calls"], first["tool_calls"], first["tool_responses"]), (2, 1, 1))
        self.assertEqual(first["tool_calls_by_name"], {"get_rows": 1})
        self.assertEqual(first["tool_errors_by_name"], {})
        self.assertEqual(first["finish_reasons"], {"STOP": 1})
        self.assertEqual(first["usage"]["input_tokens"], 220)
        self.assertEqual(first["usage"]["output_tokens"], 25)
        self.assertEqual(first["usage"]["cached_input_tokens"], 96)
        self.assertEqual(first["usage"]["reasoning_output_tokens"], 7)
        self.assertEqual(first["usage_unknown_calls"], 0)
        self.assertEqual(first["wall_seconds"], 3.0)
        self.assertEqual([step["seconds_from_previous"] for step in first["steps"]], [1.0, 1.5, 0.5])
        self.assertEqual(first["longest_steps"][0]["kind"], "tool_response")
        self.assertEqual(first["flags"], [])
        self.assertEqual(second["usage"]["input_tokens"], 140)
        self.assertEqual(report["totals"]["model_calls"], 3)
        self.assertEqual(report["totals"]["input_tokens"], 360)
        self.assertIsNone(report["totals"]["estimated_cost"])
        self.assertEqual(report["usage_counting_rule"], summary.USAGE_RULE)
        self.assertNotIn(SECRET, json.dumps(report))

    def test_tool_errors_are_counted_by_name_without_text(self):
        report = summary.inspect_events(tool_error_session()["events"])
        first, second = report["invocations"]
        self.assertEqual(first["tool_errors_by_name"], {"get_rows": 1})
        self.assertEqual(second["tool_errors_by_name"], {"send": 1})
        self.assertIn("tool_errors", first["flags"])
        self.assertEqual(report["totals"]["tool_errors"], 2)
        self.assertNotIn(SECRET, json.dumps(report))

    def test_streaming_partials_are_not_summed(self):
        report = summary.inspect_events(streaming_session()["events"])
        first, second = report["invocations"]
        self.assertEqual((first["model_calls"], first["partial_events"]), (1, 2))
        self.assertEqual((first["usage"]["input_tokens"], first["usage"]["output_tokens"]), (50, 6))
        self.assertIn("partial_events_present", first["flags"])
        self.assertEqual((second["usage"]["input_tokens"], second["usage"]["output_tokens"]), (70, 9))
        self.assertEqual(second["usage_unknown_calls"], 0)
        self.assertIn("usage_taken_from_newest_partial_on_1_calls", second["flags"])
        self.assertEqual(len(second["steps"]), 1)

    def test_missing_usage_and_error_codes_are_flagged(self):
        events = clean_session()["events"]
        del events[5]["usageMetadata"]
        events.append({"invocationId": "inv-2", "author": "agent", "timestamp": 6.5,
                       "errorCode": "MAX_TOKENS", "errorMessage": SECRET})
        report = summary.inspect_events(events)
        second = report["invocations"][1]
        self.assertEqual(second["model_calls"], 2)
        self.assertEqual(second["usage_unknown_calls"], 2)
        self.assertEqual(second["model_error_codes"], {"MAX_TOKENS": 1})
        self.assertIn("usage_missing_on_2_model_calls", second["flags"])
        self.assertIn("model_error_codes", second["flags"])
        self.assertNotIn(SECRET, json.dumps(report))

    def test_prices_apply_per_model_with_default_and_cached_rates(self):
        report = summary.inspect_events(clean_session()["events"], summary.load_prices(json.dumps(PRICES).encode()))
        first, second = report["invocations"]
        # call 1: 100 input (0 cached) * 1.0 + 15 output * 4.0 = 160; call 2: 24 * 1.0 + 96 * 0.25 + 10 * 4.0 = 88
        self.assertAlmostEqual(first["estimated_cost"]["amount"], 248 / 1_000_000)
        self.assertEqual(first["estimated_cost"]["priced_calls"], 2)
        self.assertAlmostEqual(second["estimated_cost"]["amount"], (140 * 2.0 + 5 * 8.0) / 1_000_000)
        self.assertIn("priced_with_default_entry", second["flags"])
        self.assertEqual(report["cost_basis"], {"currency": "USD", "source": "user_supplied_price_table"})
        self.assertAlmostEqual(report["totals"]["estimated_cost"], (248 + 320) / 1_000_000)

    def test_unpriced_model_is_flagged_not_guessed(self):
        prices = summary.load_prices(json.dumps({"per_million": {"model-a": {"input": 1, "output": 1}}}).encode())
        report = summary.inspect_events(clean_session()["events"], prices)
        second = report["invocations"][1]
        self.assertIsNone(second["estimated_cost"]["amount"])
        self.assertEqual(second["estimated_cost"]["unpriced_calls"], 1)
        self.assertIn("unpriced_model", second["flags"])
        self.assertEqual(report["cost_basis"]["currency"], "unspecified")
        for bad in (b"[]", b"{}", b'{"per_million": {"m": {"input": -1, "output": 1}}}',
                    b'{"per_million": {"m": {"input": 1}}}', b'{"per_million": {"m": {"input": "1", "output": 1}}}'):
            with self.subTest(bad=bad):
                with self.assertRaises(summary.InvalidInput):
                    summary.load_prices(bad)

    def test_malformed_items_make_report_partial_and_empty_input_invalid(self):
        events = clean_session()["events"] + ["not an event", {"author": "agent", "content": "wrong"}]
        report = summary.inspect_events(events)
        self.assertEqual(report["verdict"], "PARTIAL")
        self.assertEqual(report["skipped_malformed_items"], 2)
        for bad in ([], "events", {"events": []}):
            with self.subTest(bad=bad):
                with self.assertRaises(summary.InvalidInput):
                    summary.inspect_events(bad)

    def test_load_events_accepts_object_array_and_jsonl(self):
        events = clean_session()["events"]
        self.assertEqual(summary.load_events(json.dumps({"events": events}).encode())[1], "session_object")
        self.assertEqual(summary.load_events(json.dumps(events).encode())[1], "event_array")
        lines, kind = summary.load_events("\n".join(json.dumps(e) for e in events).encode())
        self.assertEqual((len(lines), kind), (6, "jsonl"))
        for raw in (b"", b'{"id": 1}', b"not json\n{\"a\": 1}", b"\xff\xfe", b"42"):
            with self.subTest(raw=raw):
                with self.assertRaises(summary.InvalidInput):
                    summary.load_events(raw)

    def test_csv_has_one_row_per_invocation(self):
        report = summary.inspect_events(tool_error_session()["events"])
        rows = list(csv.reader(io.StringIO(summary.to_csv(report))))
        self.assertEqual(tuple(rows[0]), summary.CSV_COLUMNS)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1][0], "inv-1")
        self.assertEqual(rows[1][rows[0].index("tool_errors")], "1")
        self.assertIn("tool_errors", rows[1][rows[0].index("flags")])


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
        self.assertEqual(self.run_cli("--session", "x.json", "--format", "xml").returncode, 2)

    def test_cli_is_read_only_repeatable_and_redacted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "session.json"
            path.write_text(json.dumps(tool_error_session()))
            prices = root / "prices.json"
            prices.write_text(json.dumps(PRICES))
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            first = self.run_cli("--session", str(path), "--prices", str(prices))
            second = self.run_cli("--session", str(path), "--prices", str(prices), "--dry-run")
            self.assertEqual((first.returncode, second.returncode), (0, 0))
            self.assertEqual(first.stdout, second.stdout)
            parsed = json.loads(first.stdout)
            self.assertEqual(parsed["source_format"], "session_object")
            self.assertEqual(parsed["totals"]["tool_errors"], 2)
            self.assertIsNotNone(parsed["totals"]["estimated_cost"])
            self.assertNotIn(SECRET, first.stdout + first.stderr)
            as_csv = self.run_cli("--session", str(path), "--format", "csv")
            self.assertEqual(as_csv.returncode, 0)
            self.assertTrue(as_csv.stdout.startswith("invocation_id,"))
            self.assertNotIn(SECRET, as_csv.stdout)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})
            prices.write_text("{not json")
            bad_prices = self.run_cli("--session", str(path), "--prices", str(prices))
            self.assertEqual(bad_prices.returncode, 1)
            self.assertEqual(json.loads(bad_prices.stdout)["reason"], "invalid_price_table")
            path.write_text("{not json")
            malformed = self.run_cli("--session", str(path))
            self.assertEqual(malformed.returncode, 1)
            self.assertEqual(json.loads(malformed.stdout)["verdict"], "MALFORMED")
            self.assertNotIn(directory, malformed.stdout + malformed.stderr)
            self.assertEqual(self.run_cli("--session", str(root / "absent.json")).returncode, 1)
            path.write_text(json.dumps(clean_session()["events"] + [SECRET]))
            partial = self.run_cli("--session", str(path))
            self.assertEqual(partial.returncode, 1)
            self.assertEqual(json.loads(partial.stdout)["verdict"], "PARTIAL")
            self.assertNotIn(SECRET, partial.stdout + partial.stderr)
            link = root / "link.json"
            link.symlink_to(path)
            self.assertEqual(self.run_cli("--session", str(link)).returncode, 1)


if __name__ == "__main__":
    unittest.main()
