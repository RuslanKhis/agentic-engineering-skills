"""Synthetic, offline tests for the bundled read-only AG-UI trace checker."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_agui_trace.py"
SPEC = importlib.util.spec_from_file_location("check_agui_trace", SCRIPT)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def start(run="run-1", thread="thread-1"):
    return {"type": "RUN_STARTED", "threadId": thread, "runId": run}


def finish(run="run-1", thread="thread-1"):
    return {"type": "RUN_FINISHED", "threadId": thread, "runId": run}


def tool_events():
    return [
        {"type": "TOOL_CALL_START", "toolCallId": "call-1", "toolCallName": "classify"},
        {"type": "TOOL_CALL_ARGS", "toolCallId": "call-1", "delta": '{"ticket":'},
        {"type": "TOOL_CALL_ARGS", "toolCallId": "call-1", "delta": '"billing"}'},
        {"type": "TOOL_CALL_END", "toolCallId": "call-1"},
        {"type": "TOOL_CALL_RESULT", "toolCallId": "call-1", "messageId": "result-1", "content": "routed"},
    ]


def text_events():
    return [
        {"type": "TEXT_MESSAGE_START", "messageId": "answer-1", "role": "assistant"},
        {"type": "TEXT_MESSAGE_CONTENT", "messageId": "answer-1", "delta": "Routed to "},
        {"type": "TEXT_MESSAGE_CONTENT", "messageId": "answer-1", "delta": "billing."},
        {"type": "TEXT_MESSAGE_END", "messageId": "answer-1"},
    ]


def ndjson(events):
    return "\n".join(json.dumps(event) for event in events) + "\n"


class TraceTests(unittest.TestCase):
    def check(self, events):
        return checker.validate(ndjson(events))

    def assert_invalid(self, events, code):
        with self.assertRaises(checker.TraceError) as caught:
            self.check(events)
        self.assertEqual(caught.exception.code, code)

    def test_text_and_fragmented_tool_arguments_complete_successfully(self):
        result = self.check([start(), *tool_events(), *text_events(), finish()])
        self.assertEqual(result["successful_runs"], 1)
        self.assertEqual(result["text_chunks"], 2)
        self.assertEqual(result["tool_results"], 1)

    def test_arguments_are_not_parsed_until_end(self):
        events = [start(), *tool_events()[:2]]
        # The incomplete JSON chunk is legal until END; an error may abort it.
        self.assertEqual(self.check([*events, {"type": "RUN_ERROR", "message": "aborted"}])["error_runs"], 1)
        self.assert_invalid([*events, {"type": "TOOL_CALL_END", "toolCallId": "call-1"}],
                            "invalid_complete_tool_arguments")

    def test_parseable_chunk_does_not_allow_result_before_end(self):
        self.assert_invalid([start(), tool_events()[0],
                             {"type": "TOOL_CALL_ARGS", "toolCallId": "call-1", "delta": "{}"},
                             tool_events()[4]], "tool_result_before_end_or_duplicate")

    def test_repeated_partial_and_final_call_id_is_rejected(self):
        self.assert_invalid([start(), *tool_events()[:2], tool_events()[0]], "duplicate_tool_call_id")

    def test_complete_tool_arguments_must_be_unique_key_object(self):
        for argument in ('[]', '{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}', '{}{}'):
            with self.subTest(argument=argument):
                events = [start(), tool_events()[0],
                          {"type": "TOOL_CALL_ARGS", "toolCallId": "call-1", "delta": argument},
                          tool_events()[3]]
                with self.assertRaises(checker.TraceError):
                    self.check(events)

    def test_zero_argument_tool_is_supported(self):
        self.assertEqual(self.check([start(), tool_events()[0], *tool_events()[3:], finish()])["tool_results"], 1)

    def test_duplicate_result_and_late_argument_are_rejected(self):
        self.assert_invalid([start(), *tool_events(), tool_events()[4]], "tool_result_before_end_or_duplicate")
        self.assert_invalid([start(), *tool_events(), tool_events()[1]], "tool_arguments_not_open")

    def test_unknown_tool_and_missing_result_are_rejected(self):
        self.assert_invalid([start(), tool_events()[4]], "unknown_tool_call_id")
        self.assert_invalid([start(), *tool_events()[:4], finish()], "unfinished_backend_tool_call")

    def test_text_correlation_and_unique_message_ids(self):
        self.assert_invalid([start(), text_events()[1]], "text_message_not_open")
        self.assert_invalid([start(), *text_events(), text_events()[0]], "duplicate_message_id")
        collision = {**tool_events()[4], "messageId": "answer-1"}
        self.assert_invalid([start(), *text_events(), *tool_events()[:4], collision], "duplicate_message_id")

    def test_unfinished_text_and_eof_are_rejected(self):
        self.assert_invalid([start(), text_events()[0], finish()], "unfinished_text_message")
        self.assert_invalid([start(), *text_events()], "unfinished_run_at_eof")
        self.assert_invalid([], "no_run")

    def test_error_after_answer_remains_error(self):
        result = self.check([start(), *text_events(), {"type": "RUN_ERROR", "message": "late failure"}])
        self.assertEqual((result["successful_runs"], result["error_runs"]), (0, 1))

    def test_error_is_terminal_and_can_abort_open_text(self):
        events = [start(), text_events()[0], {"type": "RUN_ERROR", "message": "failure"}]
        self.assertEqual(self.check(events)["error_runs"], 1)
        self.assert_invalid([*events, finish()], "event_outside_active_run")
        self.assert_invalid([*events, text_events()[1]], "event_outside_active_run")

    def test_run_identity_and_nonoverlap(self):
        self.assert_invalid([start(), finish(run="other")], "terminal_run_mismatch")
        self.assert_invalid([start(), start(run="other")], "overlapping_run")
        self.assert_invalid([start(), finish(), start()], "duplicate_run_id")
        self.assert_invalid([finish()], "event_outside_active_run")
        self.assertEqual(self.check([start(), finish(), start("run-2"), finish("run-2")])["runs"], 2)

    def test_optional_events_and_nested_steps_are_accepted(self):
        optional = [
            {"type": "STATE_SNAPSHOT", "snapshot": {}},
            {"type": "STATE_DELTA", "delta": []},
            {"type": "MESSAGES_SNAPSHOT", "messages": []},
            {"type": "CUSTOM", "name": "progress", "value": {"done": False}},
            {"type": "RAW", "event": None},
            {"type": "ACTIVITY_SNAPSHOT", "messageId": "activity-1", "activityType": "status", "content": {}},
            {"type": "ACTIVITY_DELTA", "messageId": "activity-1", "activityType": "status", "patch": []},
        ]
        events = [start(), *optional,
                  {"type": "STEP_STARTED", "stepName": "outer"},
                  {"type": "STEP_STARTED", "stepName": "inner"},
                  {"type": "STEP_FINISHED", "stepName": "inner"},
                  {"type": "STEP_FINISHED", "stepName": "outer"}, finish()]
        self.assertEqual(self.check(events)["ancillary_events"], 7)

    def test_optional_field_types_and_steps_are_checked(self):
        self.assert_invalid([start(), {"type": "STATE_DELTA", "delta": {}}], "invalid_event_field")
        self.assert_invalid([start(), {"type": "CUSTOM", "name": "status"}], "invalid_event_field")
        self.assert_invalid([start(), {"type": "STEP_FINISHED", "stepName": "unknown"}], "step_not_open_or_out_of_order")
        self.assert_invalid([start(), {"type": "STEP_STARTED", "stepName": "open"}, finish()], "unfinished_step")

    def test_unsupported_profiles_are_explicitly_rejected(self):
        for event_type in ("TEXT_MESSAGE_CHUNK", "TOOL_CALL_CHUNK", "REASONING_START", "SUBAGENT_STARTED", "FUTURE_EVENT"):
            with self.subTest(event_type=event_type):
                self.assert_invalid([start(), {"type": event_type}], "unsupported_event_type")
        self.assert_invalid([start(), {**finish(), "outcome": {"type": "interrupt", "interrupts": []}}], "unsupported_run_outcome")
        self.assert_invalid([start(), {**text_events()[0], "subagentRunId": "sub"}], "unsupported_subagent_scope")

    def test_nonobject_and_duplicate_key_events_are_rejected(self):
        self.assert_invalid([[]], "event_object_required")
        with self.assertRaises(checker.TraceError) as caught:
            checker.validate('{"type":"RUN_STARTED","type":"RUN_FINISHED"}')
        self.assertEqual(caught.exception.code, "invalid_event_json")

    def test_malformed_role_types_produce_controlled_errors(self):
        self.assert_invalid([start(), {**text_events()[0], "role": []}], "invalid_message_role")
        self.assert_invalid([start(), *tool_events()[:4], {**tool_events()[4], "role": {}}],
                            "invalid_tool_result_role")

    def test_unicode_line_separator_is_text_not_ndjson_delimiter(self):
        events = [start(), text_events()[0],
                  {**text_events()[1], "delta": "before\u2028after"}, text_events()[3], finish()]
        content = "\r\n".join(json.dumps(event, ensure_ascii=False) for event in events)
        self.assertEqual(checker.validate(content)["text_chunks"], 1)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.trace = self.directory / "trace.ndjson"
        self.trace.write_text(ndjson([start(), *tool_events(), *text_events(), finish()]), encoding="utf-8")

    def run_cli(self, *args, script=SCRIPT):
        return subprocess.run([sys.executable, str(script), *map(str, args)],
                              cwd=self.directory, capture_output=True, text=True, timeout=10)

    def test_help_and_repeated_dry_run_are_portable_read_only(self):
        copied = self.directory / "copied" / "check_agui_trace.py"
        copied.parent.mkdir()
        shutil.copy2(SCRIPT, copied)
        help_result = self.run_cli("--help", script=copied)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("--dry-run", help_result.stdout)
        before = hashlib.sha256(self.trace.read_bytes()).hexdigest()
        outcomes = [self.run_cli(self.trace, "--dry-run", script=copied) for _ in range(2)]
        self.assertEqual([result.returncode for result in outcomes], [0, 0])
        self.assertEqual(outcomes[0].stdout, outcomes[1].stdout)
        self.assertEqual(before, hashlib.sha256(self.trace.read_bytes()).hexdigest())
        self.assertEqual(sorted(item.name for item in self.directory.iterdir()), ["copied", "trace.ndjson"])

    def test_late_error_is_not_success_and_can_be_expected(self):
        self.trace.write_text(ndjson([start(), *text_events(), {"type": "RUN_ERROR", "message": "synthetic-secret"}]), encoding="utf-8")
        result = self.run_cli(self.trace)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["error_runs"], 1)
        self.assertNotIn("synthetic-secret", result.stdout + result.stderr)
        self.assertEqual(self.run_cli(self.trace, "--expect-outcome", "error").returncode, 0)
        self.assertEqual(self.run_cli(self.trace, "--expect-outcome", "either").returncode, 0)

    def test_success_does_not_satisfy_expected_error(self):
        self.assertEqual(self.run_cli(self.trace, "--expect-outcome", "error").returncode, 3)

    def test_errors_never_echo_trace_content_or_path(self):
        self.trace.write_text('synthetic-secret-token', encoding="utf-8")
        result = self.run_cli(self.trace)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("synthetic-secret", result.stdout + result.stderr)
        self.assertNotIn(str(self.trace), result.stdout + result.stderr)
        missing = self.run_cli(self.directory / "synthetic-secret-missing")
        self.assertEqual(missing.returncode, 2)
        self.assertNotIn("synthetic-secret", missing.stdout + missing.stderr)

    def test_file_and_event_limits_and_invalid_arguments(self):
        for arguments in (("--max-bytes", "1"), ("--max-events", "1"),
                          ("--max-bytes", "0"), ("--max-events", "100001"),
                          ("--max-bytes", "67108865"), ("--max-events", "secret-value"),
                          ("--unknown-secret-flag",)):
            with self.subTest(arguments=arguments):
                result = self.run_cli(self.trace, *arguments)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("secret", result.stdout + result.stderr)
        self.assertEqual(self.run_cli(self.directory).returncode, 2)

    def test_invalid_utf8_and_sse_input_are_rejected(self):
        self.trace.write_bytes(b"\xff")
        self.assertEqual(self.run_cli(self.trace).returncode, 2)
        self.trace.write_text('data: {"type":"RUN_STARTED"}\n\n', encoding="utf-8")
        self.assertEqual(self.run_cli(self.trace).returncode, 1)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is unavailable on this platform")
    def test_fifo_is_rejected_without_waiting_for_a_writer(self):
        fifo = self.directory / "trace.fifo"
        os.mkfifo(fifo)
        result = self.run_cli(fifo)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["code"], "regular_file_required")


if __name__ == "__main__":
    unittest.main()
