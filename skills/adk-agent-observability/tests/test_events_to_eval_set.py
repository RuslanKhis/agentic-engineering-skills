"""Offline checks for the session-to-EvalSet converter.

Synthetic fixtures only. These tests establish the field shape the converter
emits and its redaction behaviour, not acceptance by a particular google-adk
release unless the optional SDK check runs in an environment that has it.
"""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "events_to_eval_set.py"
SPEC = importlib.util.spec_from_file_location("events_to_eval_set", SCRIPT)
converter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(converter)

SECRET = "SYNTHETIC_SECRET_VALUE"
EMAIL = "someone@example.invalid"
HOOK_MODULE = "synthetic_redact_hook"


def event(invocation, author, parts, timestamp, **more):
    return {"invocationId": invocation, "author": author, "timestamp": timestamp,
            "content": {"role": "user" if author == "user" else "model", "parts": parts}, **more}


def session():
    return {"id": "synthetic session", "appName": "demo_app", "userId": "real-user-7", "events": [
        event("inv-1", "user", [{"text": "look up order 42"}], 1.0),
        event("inv-1", "agent", [{"text": "checking", "thought": True},
                                 {"functionCall": {"id": "c1", "name": "get_order", "args": {"id": 42}}}], 2.0),
        event("inv-1", "agent", [{"functionResponse": {"id": "c1", "name": "get_order",
               "response": {"status": "success", "result": "shipped"}}}], 3.0),
        event("inv-1", "agent", [{"text": "Order 42 has shipped."}], 4.0, finishReason="STOP"),
        event("inv-2", "user", [{"text": f"email {EMAIL} the receipt"}], 5.0),
        event("inv-2", "agent", [{"text": "p"}], 5.5, partial=True),
        event("inv-2", "agent", [{"functionCall": {"id": "c2", "name": "send_mail", "args": {"to": EMAIL}}}], 6.0),
        event("inv-2", "agent", [{"functionResponse": {"id": "c2", "name": "send_mail",
               "response": {"error": f"smtp refused {SECRET}", "status": "error"}}}], 7.0),
        event("inv-2", "agent", [{"inlineData": {"mimeType": "image/png", "data": "AAAA"}},
                                 {"text": "I could not send the email, see https://status.example.invalid/x"}], 8.0),
        event("inv-3", "user", [{"text": "thanks"}], 9.0),
        event("inv-3", "agent", [{"text": "You are welcome."}], 10.0),
    ]}


def write_hook(root):
    (root / f"{HOOK_MODULE}.py").write_text(
        "def scrub(case):\n"
        "    case['eval_id'] = case['eval_id'] + '_hooked'\n"
        "    for invocation in case['conversation']:\n"
        "        invocation['user_content']['parts'] = [{'text': '[HOOKED]'}]\n"
        "    return case\n"
        "def broken(case):\n"
        "    raise ValueError('nope')\n"
        "def wrong(case):\n"
        "    return 'not a dict'\n")


class ConversionChecks(unittest.TestCase):
    def convert(self, select="all", allow_content=False, max_text_chars=2000):
        counters = {"skipped_malformed_items": 0, "dropped_parts": 0, "redactions": {"text_parts": 0, "strings": 0}}
        groups = converter.group_invocations(session()["events"], counters)
        settings = {"select": select, "allow_content": allow_content, "max_text_chars": max_text_chars,
                    "hook": None, "eval_set_id": "synthetic_session", "app_name": "demo_app", "user_id": "eval_user"}
        eval_set, selected = converter.build_eval_set(groups, settings, counters)
        return eval_set, selected, counters

    def test_all_invocations_become_one_case_with_the_2_8_0_field_names(self):
        eval_set, selected, counters = self.convert(allow_content=True)
        self.assertEqual(selected, 3)
        self.assertEqual(set(eval_set), {"eval_set_id", "name", "description", "eval_cases", "creation_timestamp"})
        self.assertEqual(eval_set["eval_set_id"], "synthetic_session")
        self.assertEqual(eval_set["creation_timestamp"], 9.0)
        case = eval_set["eval_cases"][0]
        self.assertEqual(set(case), {"eval_id", "conversation", "session_input", "creation_timestamp"})
        self.assertEqual(case["session_input"], {"app_name": "demo_app", "user_id": "eval_user", "state": {}})
        self.assertEqual([inv["invocation_id"] for inv in case["conversation"]], ["inv-1", "inv-2", "inv-3"])
        first = case["conversation"][0]
        self.assertEqual(first["user_content"], {"role": "user", "parts": [{"text": "look up order 42"}]})
        self.assertEqual(first["final_response"], {"role": "model", "parts": [{"text": "Order 42 has shipped."}]})
        self.assertEqual(first["intermediate_data"]["tool_uses"], [{"id": "c1", "name": "get_order", "args": {"id": 42}}])
        self.assertEqual(first["intermediate_data"]["tool_responses"],
                         [{"id": "c1", "name": "get_order", "response": {"status": "success", "result": "shipped"}}])
        self.assertEqual(first["intermediate_data"]["intermediate_responses"], [])
        self.assertEqual(first["creation_timestamp"], 1.0)
        second = case["conversation"][1]
        self.assertEqual(second["final_response"]["parts"][0]["text"][:21], "I could not send the ")
        self.assertEqual(counters["dropped_parts"], 2)  # thought part and inline image
        self.assertEqual(converter.check_structure(eval_set), [])

    def test_tool_error_selection_emits_prefix_conversations(self):
        eval_set, selected, _ = self.convert(select="tool_error")
        self.assertEqual(selected, 1)
        self.assertEqual(len(eval_set["eval_cases"]), 1)
        case = eval_set["eval_cases"][0]
        self.assertEqual(case["eval_id"], "synthetic_session_inv_2")
        self.assertEqual([inv["invocation_id"] for inv in case["conversation"]], ["inv-1", "inv-2"])
        self.assertEqual(converter.check_structure(eval_set), [])

    def test_mcp_is_error_counts_as_tool_error(self):
        for key in ("isError", "is_error"):
            with self.subTest(key=key):
                self.assertTrue(converter.tool_response_error({key: True, "content": []}))
        self.assertFalse(converter.tool_response_error({"isError": False, "status": "ok"}))
        self.assertTrue(converter.tool_response_error({"status": "FAILED"}))

    def test_default_redaction_replaces_emails_urls_long_text_and_tool_strings(self):
        eval_set, _, counters = self.convert(max_text_chars=30)
        case = eval_set["eval_cases"][0]
        second = case["conversation"][1]
        self.assertEqual(second["user_content"]["parts"], [{"text": converter.REDACTED}])
        self.assertEqual(second["final_response"]["parts"], [{"text": converter.REDACTED}])
        self.assertEqual(second["intermediate_data"]["tool_uses"][0]["args"], {"to": converter.REDACTED})
        self.assertEqual(second["intermediate_data"]["tool_responses"][0]["response"]["error"], converter.REDACTED)
        self.assertEqual(second["intermediate_data"]["tool_responses"][0]["response"]["status"], "error")
        first = case["conversation"][0]
        self.assertEqual(first["user_content"]["parts"], [{"text": "look up order 42"}])
        self.assertEqual(first["final_response"]["parts"], [{"text": "Order 42 has shipped."}])
        self.assertEqual(counters["redactions"], {"text_parts": 2, "strings": 2})
        dumped = json.dumps(eval_set)
        self.assertNotIn(SECRET, dumped)
        self.assertNotIn(EMAIL, dumped)
        self.assertNotIn("real-user-7", dumped)

    def test_structural_checker_names_problems(self):
        eval_set, _, _ = self.convert()
        eval_set["eval_set_id"] = "bad id"
        eval_set["eval_cases"][0]["conversation_scenario"] = {}
        eval_set["eval_cases"][0]["conversation"][0]["user_content"]["parts"] = []
        self.assertEqual(converter.check_structure(eval_set),
                         ["conversation_xor_scenario", "eval_set_id_pattern", "user_content_without_parts"])
        self.assertEqual(converter.check_structure({"eval_set_id": "x", "eval_cases": []}), ["no_eval_cases"])

    def test_sanitise_id_and_hook_spec_validation(self):
        self.assertEqual(converter.sanitise_id("my session.json", "x"), "my_session_json")
        self.assertEqual(converter.sanitise_id("///", "fallback"), "fallback")
        for spec in ("nomodule", "mod:", ":func", "mod:func()", "../x:y"):
            with self.subTest(spec=spec):
                with self.assertRaises(converter.InvalidInput):
                    converter.load_hook(spec)
        with self.assertRaises(converter.InvalidInput):
            converter.load_hook("definitely_missing_module_xyz:func")


class CommandChecks(unittest.TestCase):
    def run_cli(self, *arguments, cwd=None):
        return subprocess.run([sys.executable, str(SCRIPT), *arguments],
                              text=True, capture_output=True, timeout=20, cwd=cwd)

    def test_help_and_bad_arguments(self):
        self.assertEqual(self.run_cli("--help").returncode, 0)
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(self.run_cli("--session", "x.json").returncode, 2)
        result = self.run_cli("--session", "x.json", "--out", "y.json", "--select", "SYNTHETIC_SECRET_VALUE")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)
        self.assertEqual(self.run_cli("--session", "x.json", "--out", "y.json", "--max-text-chars", "0").returncode, 2)

    def test_cli_writes_only_the_output_and_reports_redactions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "session.json"
            source.write_text(json.dumps(session()))
            out = root / "regressions.evalset.json"
            result = self.run_cli("--session", str(source), "--out", str(out), "--select", "tool_error")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual((report["verdict"], report["writes"], report["eval_cases"]), ("INSPECTED", 1, 1))
            self.assertEqual(report["invocations_selected"], 1)
            self.assertEqual(report["out"], "regressions.evalset.json")
            self.assertEqual(report["sdk_validation"], "not run (pass --validate-with-sdk)")
            self.assertEqual(report["structural_problems"], [])
            self.assertNotIn(directory, result.stdout + result.stderr)
            written = json.loads(out.read_text())
            self.assertEqual(written["eval_set_id"], "synthetic_session")
            self.assertEqual(written["eval_cases"][0]["eval_id"], "synthetic_session_inv_2")
            self.assertNotIn(SECRET, out.read_text())
            self.assertNotIn(EMAIL, out.read_text())
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["regressions.evalset.json", "session.json"])
            repeat = self.run_cli("--session", str(source), "--out", str(out), "--select", "tool_error")
            self.assertEqual(repeat.returncode, 1)
            self.assertEqual(json.loads(repeat.stdout)["reason"], "output_exists_use_force")
            forced = self.run_cli("--session", str(source), "--out", str(out), "--select", "tool_error", "--force")
            self.assertEqual(forced.returncode, 0)
            self.assertEqual(forced.stdout, result.stdout)
            sdk = self.run_cli("--session", str(source), "--out", str(out), "--force", "--validate-with-sdk")
            self.assertEqual(sdk.returncode, 0, sdk.stderr)
            status = json.loads(sdk.stdout)["sdk_validation"]
            self.assertTrue(status.startswith("validated") or status.startswith("not validated against SDK"), status)
            dry = self.run_cli("--session", str(source), "--out", str(root / "dry.json"), "--dry-run")
            self.assertEqual(dry.returncode, 0)
            self.assertEqual(json.loads(dry.stdout)["writes"], 0)
            self.assertFalse((root / "dry.json").exists())

    def test_cli_hook_and_failure_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_hook(root)
            source = root / "session.json"
            source.write_text(json.dumps(session()))
            out = root / "hooked.evalset.json"
            result = self.run_cli("--session", str(source), "--out", str(out),
                                  "--redact-hook", f"{HOOK_MODULE}:scrub", cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            written = json.loads(out.read_text())
            self.assertEqual(written["eval_cases"][0]["eval_id"], "synthetic_session_hooked")
            self.assertEqual(written["eval_cases"][0]["conversation"][0]["user_content"]["parts"], [{"text": "[HOOKED]"}])
            for function in ("broken", "wrong"):
                with self.subTest(function=function):
                    failed = self.run_cli("--session", str(source), "--out", str(root / f"{function}.json"),
                                          "--redact-hook", f"{HOOK_MODULE}:{function}", cwd=root)
                    self.assertEqual(failed.returncode, 1)
                    self.assertEqual(json.loads(failed.stdout)["reason"], "invalid_or_unsupported_input")
                    self.assertFalse((root / f"{function}.json").exists())
            missing_hook = self.run_cli("--session", str(source), "--out", str(root / "m.json"),
                                        "--redact-hook", "no_such_module_xyz:f", cwd=root)
            self.assertEqual(missing_hook.returncode, 1)
            self.assertEqual(json.loads(missing_hook.stdout)["reason"], "invalid_redact_hook")
            clean = {"events": [event("inv-1", "user", [{"text": "hi"}], 1.0),
                                event("inv-1", "agent", [{"text": "hello"}], 2.0)]}
            source.write_text(json.dumps(clean))
            none = self.run_cli("--session", str(source), "--out", str(root / "none.json"), "--select", "tool_error")
            self.assertEqual(none.returncode, 1)
            self.assertEqual(json.loads(none.stdout)["verdict"], "NO_CASES")
            self.assertFalse((root / "none.json").exists())
            source.write_text("{not json")
            malformed = self.run_cli("--session", str(source), "--out", str(root / "bad.json"))
            self.assertEqual(malformed.returncode, 1)
            self.assertEqual(json.loads(malformed.stdout)["verdict"], "MALFORMED")
            self.assertFalse((root / "bad.json").exists())
            self.assertEqual(self.run_cli("--session", str(root / "absent.json"), "--out", str(root / "a.json")).returncode, 1)
            for name in root.iterdir():
                if name.name.endswith(".pyc") or name.name == "__pycache__":
                    continue
                self.assertIn(name.name, {"session.json", "hooked.evalset.json", f"{HOOK_MODULE}.py"})


if __name__ == "__main__":
    unittest.main()
