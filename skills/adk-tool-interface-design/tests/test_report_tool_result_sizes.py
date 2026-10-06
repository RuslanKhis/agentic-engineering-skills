"""Exercise the result-size reporter through its CLI with synthetic event files."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "report_tool_result_sizes.py"


def call(name, args, call_id="c1"):
    return {"author": "root", "content": {"role": "model", "parts": [
        {"function_call": {"name": name, "args": args, "id": call_id}}]}}


def response(name, payload, call_id="c1", camel=False):
    key = "functionResponse" if camel else "function_response"
    return {"author": "root", "content": {"role": "user", "parts": [
        {key: {"name": name, "response": payload, "id": call_id}}]}}


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def write(self, name, content):
        path = self.dir / name
        path.write_text(content)
        return path

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT)] + list(args),
                              capture_output=True, text=True, check=False)

    def report(self, path, *args):
        result = self.run_cli("--events", str(path), *args)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        return result, json.loads(result.stdout)

    def test_help_and_bad_arguments(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.run_cli("--events", str(self.dir / "absent.json")).returncode, 2)
        path = self.write("events.json", "[]")
        for value in ("0", "-3", "many"):
            self.assertEqual(self.run_cli("--events", str(path), "--max-bytes", value).returncode, 2)

    def test_json_list_sizes_tokens_and_flags(self):
        secret = "RESPONSE_CONTENT_MUST_NOT_PRINT"
        big = {"status": "success", "rows": [secret] * 50}
        events = [call("search_docs", {"query": "q"}), response("search_docs", big),
                  call("search_docs", {"query": "q2"}, "c2"), response("search_docs", big, "c2"),
                  call("get_time", {}, "c3"), response("get_time", {"status": "success", "time": "10:00"}, "c3"),
                  {"author": "root", "content": {"role": "model", "parts": [{"text": "done"}]}}]
        path = self.write("events.json", json.dumps(events))
        result, data = self.report(path, "--max-bytes", "500")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout)
        self.assertFalse(data["partial"])
        self.assertEqual(data["events_seen"], 7)
        by_name = {t["tool"]: t for t in data["tools"]}
        self.assertEqual(set(by_name), {"search_docs", "get_time"})
        search = by_name["search_docs"]
        self.assertEqual((search["calls"], search["responses"]), (2, 2))
        expected = len(json.dumps(big, sort_keys=True, ensure_ascii=False).encode())
        self.assertEqual(search["response_bytes_max"], expected)
        self.assertEqual(search["response_bytes_p95"], expected)
        self.assertEqual(search["approx_tokens_max"], expected // 4)
        self.assertEqual(search["repeated_identical_responses"], 1)
        self.assertEqual(search["over_max_bytes"], 2)
        self.assertEqual(search["status_values"], {"success": 2})
        self.assertEqual(data["token_estimate"], "bytes_divided_by_4")
        flags = {(f["flag"], f["tool"]) for f in data["flags"]}
        self.assertIn(("response_exceeds_max_bytes", "search_docs"), flags)
        self.assertIn(("repeated_identical_response", "search_docs"), flags)
        self.assertEqual(by_name["get_time"]["over_max_bytes"], 0)
        self.assertEqual(result.stdout, self.run_cli("--events", str(path), "--max-bytes", "500").stdout)

    def test_jsonl_camel_case_and_events_wrapper(self):
        lines = [json.dumps(call("lookup", {"order_id": "ORD-1"})),
                 json.dumps(response("lookup", {"status": "error", "error": "not found"}, camel=True)),
                 ""]
        path = self.write("events.jsonl", "\n".join(lines))
        result, data = self.report(path)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["tools"][0]["tool"], "lookup")
        self.assertEqual(data["tools"][0]["responses"], 1)
        self.assertEqual(data["tools"][0]["status_values"], {"error": 1})
        wrapped = self.write("session.json", json.dumps({"id": "s1", "events": [
            call("lookup", {}), response("lookup", "plain string")]}))
        result, data = self.report(wrapped)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data["tools"][0]["response_bytes_total"], len(json.dumps("plain string").encode()))

    def test_malformed_file_is_partial(self):
        path = self.write("broken.json", "{not json\n[also not json\n")
        result = self.run_cli("--events", str(path))
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertTrue(data["partial"])
        self.assertEqual(data["tools"], [])
        self.assertEqual(data["issues"][0]["reason"], "malformed_jsonl_lines")
        self.assertNotIn("not json", result.stdout)
        mixed = self.write("mixed.json", json.dumps([call("a", {}), 42, {"content": {"parts": ["text"]}}]))
        result, data = self.report(mixed)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data["events_skipped"], 2)
        self.assertEqual(data["tools"][0]["calls"], 1)

    def test_symlink_is_rejected(self):
        target = self.write("events.json", "[]")
        link = self.dir / "link.json"
        link.symlink_to(target)
        self.assertEqual(self.run_cli("--events", str(link)).returncode, 2)


if __name__ == "__main__":
    unittest.main()
