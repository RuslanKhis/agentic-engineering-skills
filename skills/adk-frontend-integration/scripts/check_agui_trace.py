#!/usr/bin/env python3
"""Check recorded AG-UI event ordering without making network calls.

Input is UTF-8 NDJSON: one camelCase wire-event object per nonblank line, not
an SSE stream. The supported profile is explicit, sequential, non-overlapping
runs with backend tool execution. Text START/CONTENT/END and tool START/ARGS/
END/RESULT events are correlated by ID. Explicit text/result message IDs and
tool-call IDs cannot repeat within a run; run IDs cannot repeat within a file.
parentMessageId is syntax-checked; links to initial history are not verified.
Arguments are assembled and parsed as a JSON
object only at TOOL_CALL_END; no argument chunks means an empty object.
Successful runs must close text, steps, and calls and contain every tool result.
RUN_ERROR may abort open work, is terminal, and never counts as success.

STATE_SNAPSHOT, STATE_DELTA, MESSAGES_SNAPSHOT, ACTIVITY_SNAPSHOT,
ACTIVITY_DELTA, RAW and CUSTOM are accepted with envelope/field-type checks.
Their payload semantics, JSON Patch operations and snapshot message histories
are not checked. STEP_STARTED/STEP_FINISHED are checked as a nested stack.
Unrecognised events, compact CHUNK events, reasoning/thinking/subagent events,
subagentRunId and interrupted/human-in-the-loop runs are outside this profile.
Normalise those formats or extend the profile deliberately before checking.
Optional metadata and additional fields do not establish any guarantees.

This is a regression aid, not a complete AG-UI schema validator. It cannot
prove model/provider behaviour, authentication, authorisation, tool side effects,
tool-result semantics, redaction, cancellation, or production readiness. A
successful protocol run need not contain assistant text or a tool call.

Output contains counts and fixed diagnostic codes, never input paths, IDs,
arguments, results, error messages or other trace content. No files are written.
--dry-run performs the same read-only validation. Limits are enforced even if
the input grows while being read. Only regular files are accepted.

Exit codes: 0 valid and expected outcome; 1 invalid/unsupported trace;
2 argument, file, encoding or size-limit error; 3 valid but unexpected outcome.
--expect-outcome success (default) requires all runs to finish successfully;
error requires all runs to end in RUN_ERROR; either accepts both outcomes.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import stat
import sys


DEFAULT_MAX_BYTES = 8 * 1024 * 1024
HARD_MAX_BYTES = 64 * 1024 * 1024
DEFAULT_MAX_EVENTS = 10_000
HARD_MAX_EVENTS = 100_000


class TraceError(Exception):
    def __init__(self, code: str, event: int = 0, exit_code: int = 1):
        self.code = code
        self.event = event
        self.exit_code = exit_code


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _constant(_value):
    raise ValueError("non-finite number")


def _float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("non-finite number")
    return result


def strict_json(value: str):
    return json.loads(value, object_pairs_hook=_object, parse_constant=_constant,
                      parse_float=_float)


def read_trace(path: Path, max_bytes: int) -> str:
    descriptor = None
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise TraceError("regular_file_required", exit_code=2)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise TraceError("byte_limit_exceeded", exit_code=2)
        return data.decode("utf-8")
    except UnicodeError:
        raise TraceError("utf8_required", exit_code=2) from None
    except (OSError, ValueError):
        raise TraceError("input_unreadable", exit_code=2) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


class Validator:
    def __init__(self):
        self.counts = dict(events=0, runs=0, successful_runs=0, error_runs=0,
                           text_messages=0, text_chunks=0, tool_calls=0,
                           tool_results=0, ancillary_events=0)
        self.run_ids = set()
        self.active = None
        self.messages = {}
        self.tools = {}
        self.steps = []

    def fail(self, code):
        raise TraceError(code, self.counts["events"])

    def require(self, event, key, kind):
        if key not in event or not isinstance(event[key], kind):
            self.fail("invalid_event_field")
        return event[key]

    def identifier(self, event, key):
        value = self.require(event, key, str)
        if not value or len(value) > 512 or any(ord(char) < 32 for char in value):
            self.fail("invalid_identifier")
        return value

    def optional_identifier(self, event, key):
        if event.get(key) is not None:
            self.identifier(event, key)

    def new_message(self, message_id, state):
        if message_id in self.messages:
            self.fail("duplicate_message_id")
        self.messages[message_id] = state

    def accept(self, event):
        self.counts["events"] += 1
        if not isinstance(event, dict):
            self.fail("event_object_required")
        event_type = self.require(event, "type", str)
        if event.get("subagentRunId") is not None:
            self.fail("unsupported_subagent_scope")
        if event_type == "RUN_STARTED":
            if self.active is not None:
                self.fail("overlapping_run")
            thread_id = self.identifier(event, "threadId")
            run_id = self.identifier(event, "runId")
            if event.get("parentRunId") is not None:
                self.fail("unsupported_child_run")
            if run_id in self.run_ids:
                self.fail("duplicate_run_id")
            self.run_ids.add(run_id)
            self.active = (thread_id, run_id)
            self.messages, self.tools, self.steps = {}, {}, []
            self.counts["runs"] += 1
            return
        if self.active is None:
            self.fail("event_outside_active_run")
        if event_type in {"RUN_FINISHED", "RUN_ERROR"}:
            self.terminal(event, event_type)
        elif event_type == "TEXT_MESSAGE_START":
            message_id = self.identifier(event, "messageId")
            if event.get("role", "assistant") not in (
                "assistant", "user", "system", "developer"
            ):
                self.fail("invalid_message_role")
            self.new_message(message_id, "text_open")
            self.counts["text_messages"] += 1
        elif event_type in {"TEXT_MESSAGE_CONTENT", "TEXT_MESSAGE_END"}:
            message_id = self.identifier(event, "messageId")
            if self.messages.get(message_id) != "text_open":
                self.fail("text_message_not_open")
            if event_type == "TEXT_MESSAGE_CONTENT":
                self.require(event, "delta", str)
                self.counts["text_chunks"] += 1
            else:
                self.messages[message_id] = "text_closed"
        elif event_type == "TOOL_CALL_START":
            tool_id = self.identifier(event, "toolCallId")
            self.identifier(event, "toolCallName")
            self.optional_identifier(event, "parentMessageId")
            if tool_id in self.tools:
                self.fail("duplicate_tool_call_id")
            self.tools[tool_id] = {"state": "args", "chunks": []}
            self.counts["tool_calls"] += 1
        elif event_type in {"TOOL_CALL_ARGS", "TOOL_CALL_END", "TOOL_CALL_RESULT"}:
            self.tool_event(event, event_type)
        elif event_type == "STEP_STARTED":
            self.steps.append(self.identifier(event, "stepName"))
        elif event_type == "STEP_FINISHED":
            name = self.identifier(event, "stepName")
            if not self.steps or self.steps[-1] != name:
                self.fail("step_not_open_or_out_of_order")
            self.steps.pop()
        else:
            self.ancillary(event, event_type)

    def terminal(self, event, event_type):
        if event_type == "RUN_ERROR":
            self.require(event, "message", str)
            if event.get("code") is not None:
                self.require(event, "code", str)
            # RUN_ERROR does not require runId/threadId in AG-UI. If supplied,
            # reject a mismatch rather than silently attributing another run.
            for index, key in enumerate(("threadId", "runId")):
                if key in event and event[key] != self.active[index]:
                    self.fail("terminal_run_mismatch")
            self.counts["error_runs"] += 1
        else:
            identity = (self.identifier(event, "threadId"),
                        self.identifier(event, "runId"))
            if identity != self.active:
                self.fail("terminal_run_mismatch")
            outcome = event.get("outcome")
            if outcome is not None:
                if not isinstance(outcome, dict) or outcome.get("type") != "success":
                    self.fail("unsupported_run_outcome")
            if "text_open" in self.messages.values():
                self.fail("unfinished_text_message")
            if self.steps:
                self.fail("unfinished_step")
            if any(tool["state"] != "result" for tool in self.tools.values()):
                self.fail("unfinished_backend_tool_call")
            self.counts["successful_runs"] += 1
        self.active = None

    def tool_event(self, event, event_type):
        tool_id = self.identifier(event, "toolCallId")
        tool = self.tools.get(tool_id)
        if tool is None:
            self.fail("unknown_tool_call_id")
        if event_type in {"TOOL_CALL_ARGS", "TOOL_CALL_END"}:
            if tool["state"] != "args":
                self.fail("tool_arguments_not_open")
            if event_type == "TOOL_CALL_ARGS":
                tool["chunks"].append(self.require(event, "delta", str))
                return
            arguments = "".join(tool["chunks"])
            try:
                parsed = strict_json(arguments) if arguments.strip() else {}
            except (ValueError, RecursionError):
                self.fail("invalid_complete_tool_arguments")
            if not isinstance(parsed, dict):
                self.fail("tool_arguments_object_required")
            tool["chunks"] = []
            tool["state"] = "ended"
        else:
            if tool["state"] != "ended":
                self.fail("tool_result_before_end_or_duplicate")
            message_id = self.identifier(event, "messageId")
            self.require(event, "content", str)
            if event.get("role") not in (None, "tool"):
                self.fail("invalid_tool_result_role")
            self.new_message(message_id, "tool_result")
            tool["state"] = "result"
            self.counts["tool_results"] += 1

    def ancillary(self, event, event_type):
        fields = {
            "STATE_SNAPSHOT": (("snapshot", dict),),
            "STATE_DELTA": (("delta", list),),
            "MESSAGES_SNAPSHOT": (("messages", list),),
            "ACTIVITY_SNAPSHOT": (("content", object),),
            "ACTIVITY_DELTA": (("patch", list),),
            "RAW": (("event", object),),
            "CUSTOM": (("value", object),),
        }
        if event_type not in fields:
            self.fail("unsupported_event_type")
        for key, kind in fields[event_type]:
            self.require(event, key, kind)
        if event_type.startswith("ACTIVITY_"):
            self.identifier(event, "messageId")
            self.identifier(event, "activityType")
            if "replace" in event and not isinstance(event["replace"], bool):
                self.fail("invalid_event_field")
        if event_type == "CUSTOM":
            self.identifier(event, "name")
        if event_type == "RAW" and event.get("source") is not None:
            self.require(event, "source", str)
        self.counts["ancillary_events"] += 1

    def finish(self):
        if not self.counts["runs"]:
            self.fail("no_run")
        if self.active is not None:
            self.fail("unfinished_run_at_eof")
        return self.counts.copy()


def validate(text: str, max_events: int = DEFAULT_MAX_EVENTS):
    validator = Validator()
    # NDJSON separates records with LF (optionally preceded by CR). Other
    # Unicode line separators are legal inside JSON strings, not delimiters.
    for line in text.split("\n"):
        if not line.strip():
            continue
        if validator.counts["events"] >= max_events:
            raise TraceError("event_limit_exceeded", validator.counts["events"] + 1, 2)
        try:
            event = strict_json(line)
        except (ValueError, RecursionError):
            raise TraceError("invalid_event_json", validator.counts["events"] + 1) from None
        validator.accept(event)
    return validator.finish()


class SafeParser(argparse.ArgumentParser):
    def error(self, _message):
        # argparse normally echoes arbitrary command-line values. Keep errors
        # content-free too; --help provides the complete invocation contract.
        raise TraceError("invalid_arguments", exit_code=2)


def positive_limit(ceiling):
    def parse(value):
        try:
            number = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("positive integer required") from None
        if not 1 <= number <= ceiling:
            raise argparse.ArgumentTypeError("value outside permitted limits")
        return number
    return parse


def main(argv=None):
    try:
        parser = SafeParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("trace", type=Path, help="UTF-8 NDJSON regular file")
        parser.add_argument("--dry-run", action="store_true", help="same read-only validation; never writes")
        parser.add_argument("--expect-outcome", choices=("success", "error", "either"), default="success",
                            help="expected terminal outcome for every run (default: success)")
        parser.add_argument("--max-bytes", type=positive_limit(HARD_MAX_BYTES), default=DEFAULT_MAX_BYTES,
                            help="file byte limit (default: 8388608; maximum: 67108864)")
        parser.add_argument("--max-events", type=positive_limit(HARD_MAX_EVENTS), default=DEFAULT_MAX_EVENTS,
                            help="nonblank event limit (default: 10000; maximum: 100000)")
        args = parser.parse_args(argv)
        counts = validate(read_trace(args.trace, args.max_bytes), args.max_events)
        unexpected = (args.expect_outcome == "success" and counts["error_runs"] > 0
                      or args.expect_outcome == "error" and counts["successful_runs"] > 0)
        print(json.dumps({"status": "outcome_mismatch" if unexpected else "valid",
                          "scope": "explicit_backend_tool_runs", **counts}, sort_keys=True))
        return 3 if unexpected else 0
    except TraceError as error:
        print(json.dumps({"status": "input_error" if error.exit_code == 2 else "invalid",
                          "code": error.code, "event": error.event}, sort_keys=True))
        return error.exit_code


if __name__ == "__main__":
    sys.exit(main())
