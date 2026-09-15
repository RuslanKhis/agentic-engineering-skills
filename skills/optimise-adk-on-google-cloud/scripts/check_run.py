#!/usr/bin/env python3
"""Check a saved ADK event array against an explicit, offline acceptance contract.

Never calls a model, imports application code, writes files or prints event data.
An accepted file establishes consistency of that file, not its authenticity.
"""
# Copyright (c) 2026 RuslanKhis. SPDX-License-Identifier: MIT
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 8 * 1024 * 1024
MAX_EVENTS = 2000
NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]{0,127}\Z")


class InvalidInput(Exception):
    pass


class Rejected(Exception):
    """Only fixed public reason codes are stored in this exception."""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "check_run: invalid arguments; values omitted; see --help.\n")


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise InvalidInput()
        result[key] = value
    return result


def invalid_number(_value):
    raise InvalidInput()


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise InvalidInput()
    return result


def read_json(path, limit):
    try:
        path = Path(path)
        if not stat.S_ISREG(path.lstat().st_mode):
            raise InvalidInput()
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        flags |= getattr(os, "O_NONBLOCK", 0)
        with os.fdopen(os.open(path, flags), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise InvalidInput()
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise InvalidInput()
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=invalid_number, parse_float=finite_float)
    except (OSError, ValueError, UnicodeError, RecursionError):
        raise InvalidInput() from None


def scalar(value):
    return (value is None or type(value) in (str, bool, int)
            or type(value) is float and math.isfinite(value))


def strings(value):
    return (isinstance(value, list) and 1 <= len(value) <= 32
            and all(isinstance(s, str) and 1 <= len(s) <= 1000 for s in value))


def pointer_parts(pointer):
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise InvalidInput()
    if len(pointer) > 512 or re.search(r"~(?![01])", pointer):
        raise InvalidInput()
    return [s.replace("~1", "/").replace("~0", "~")
            for s in pointer[1:].split("/")]


def contract(document):
    allowed = {"schema_version", "answer_author", "tools", "answer_contains",
               "require_cache_hit", "min_partial_events"}
    if (not isinstance(document, dict) or set(document) - allowed
            or type(document.get("schema_version")) is not int
            or document["schema_version"] != 1
            or not isinstance(document.get("answer_author"), str)
            or not NAME.fullmatch(document["answer_author"])
            or not strings(document.get("answer_contains"))):
        raise InvalidInput()
    if type(document.get("require_cache_hit", False)) is not bool:
        raise InvalidInput()
    minimum = document.get("min_partial_events", 0)
    if type(minimum) is not int or not 0 <= minimum <= 100:
        raise InvalidInput()
    rules = document.get("tools")
    if not isinstance(rules, list) or not 1 <= len(rules) <= 16:
        raise InvalidInput()
    names = set()
    for rule in rules:
        if (not isinstance(rule, dict)
                or set(rule) - {"name", "result_equals", "result_contains"}
                or not isinstance(rule.get("name"), str)
                or not NAME.fullmatch(rule["name"]) or rule["name"] in names):
            raise InvalidInput()
        names.add(rule["name"])
        conditions = 0
        for kind in ("result_equals", "result_contains"):
            values = rule.get(kind, {})
            if not isinstance(values, dict) or len(values) > 32:
                raise InvalidInput()
            for pointer, expected in values.items():
                pointer_parts(pointer)
                if not (scalar(expected) if kind == "result_equals"
                        else strings(expected)):
                    raise InvalidInput()
                conditions += 1
        if conditions == 0:
            raise InvalidInput()
    return document


def alias(value, snake, camel):
    if snake in value and camel in value and value[snake] != value[camel]:
        raise Rejected("conflicting_aliases")
    return value.get(snake, value.get(camel))


def reported_error(value):
    for key in ("error", "errors", "errorCode", "errorMessage",
                "error_code", "error_message"):
        if key in value and value[key] not in (None, "", [], {}):
            raise Rejected("reported_error")


def lookup(value, pointer):
    for key in pointer_parts(pointer):
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r"0|[1-9][0-9]*", key):
            index = int(key)
            if index >= len(value):
                raise Rejected("missing_result_field")
            value = value[index]
        else:
            raise Rejected("missing_result_field")
    return value


def check_result(value, rule):
    if not isinstance(value, dict):
        raise Rejected("invalid_tool_result")
    reported_error(value)
    # Common ADK wrapper. Arbitrary tabular cells are not scanned as envelopes.
    if isinstance(value.get("result"), dict):
        reported_error(value["result"])
    for envelope in (value, value.get("result")):
        if isinstance(envelope, dict) and isinstance(envelope.get("status"), str):
            if envelope["status"].lower() in {
                "error", "failed", "failure", "blocked", "denied", "cancelled", "incomplete",
            }:
                raise Rejected("failed_tool_result")
    for pointer, expected in rule.get("result_equals", {}).items():
        actual = lookup(value, pointer)
        if type(actual) is not type(expected) or actual != expected:
            raise Rejected("result_assertion_failed")
    for pointer, expected in rule.get("result_contains", {}).items():
        actual = lookup(value, pointer)
        if not isinstance(actual, str) or not all(s in actual for s in expected):
            raise Rejected("result_assertion_failed")


def check_events(events, expected):
    expected = contract(expected)
    if not isinstance(events, list) or not 1 <= len(events) <= MAX_EVENTS:
        raise InvalidInput()
    rules = {rule["name"]: rule for rule in expected["tools"]}
    calls, replies, invocation_ids = {}, set(), set()
    called_names, completed_names = set(), set()
    final_count = partials = cache_events = 0
    cached_max = None
    for event in events:
        if not isinstance(event, dict):
            raise InvalidInput()
        reported_error(event)
        if event.get("interrupted"):
            raise Rejected("interrupted")
        finish = alias(event, "finish_reason", "finishReason")
        if finish not in (None, "STOP"):
            raise Rejected("incomplete_generation")
        invocation = alias(event, "invocation_id", "invocationId")
        if not isinstance(invocation, str) or not invocation:
            raise Rejected("missing_invocation_identity")
        invocation_ids.add(invocation)
        if len(invocation_ids) != 1:
            raise Rejected("mixed_invocations")
        partial = event.get("partial", False)
        if partial is None:
            partial = False
        if type(partial) is not bool:
            raise InvalidInput()
        usage = alias(event, "usage_metadata", "usageMetadata")
        if usage is not None:
            if not isinstance(usage, dict):
                raise InvalidInput()
            cached = alias(usage, "cached_content_token_count", "cachedContentTokenCount")
            if cached is not None:
                if type(cached) is not int or cached < 0:
                    raise InvalidInput()
                cache_events += 1
                cached_max = max(cached_max or 0, cached)
        content = event.get("content")
        if content is None:
            continue
        if not isinstance(content, dict):
            raise InvalidInput()
        reported_error(content)
        parts = content.get("parts")
        if parts is None:
            parts = []
        if not isinstance(parts, list) or len(parts) > 1000:
            raise InvalidInput()
        texts, tool_parts = [], []
        for part in parts:
            if not isinstance(part, dict):
                raise InvalidInput()
            reported_error(part)
            call = alias(part, "function_call", "functionCall")
            reply = alias(part, "function_response", "functionResponse")
            if call is not None and reply is not None:
                raise Rejected("ambiguous_tool_part")
            if call is not None or reply is not None:
                tool = call if call is not None else reply
                if not isinstance(tool, dict):
                    raise InvalidInput()
                reported_error(tool)
                for key in ("name", "id"):
                    if tool.get(key) is not None and not isinstance(tool[key], str):
                        raise InvalidInput()
                payload_key = "args" if call is not None else "response"
                if tool.get(payload_key) is not None and not isinstance(tool[payload_key], dict):
                    raise InvalidInput()
                tool_parts.append((call, reply))
            text = part.get("text")
            if text is not None and not isinstance(text, str):
                raise InvalidInput()
            if text and not part.get("thought"):
                texts.append(text)
        if final_count and tool_parts:
            raise Rejected("tool_after_final")
        if not partial:
            for call, reply in tool_parts:
                tool = call if call is not None else reply
                if (not isinstance(tool, dict) or tool.get("name") not in rules
                        or not isinstance(tool.get("id"), str) or not tool["id"]):
                    raise Rejected("unexpected_tool")
                name, call_id = tool["name"], tool["id"]
                if call is not None:
                    if call_id in calls or name in called_names:
                        raise Rejected("repeated_tool_call")
                    calls[call_id] = name
                    called_names.add(name)
                else:
                    if calls.get(call_id) != name or call_id in replies:
                        raise Rejected("uncorrelated_tool_response")
                    check_result(tool.get("response"), rules[name])
                    replies.add(call_id)
                    completed_names.add(name)
        if (not tool_parts and content.get("role") == "model"
                and event.get("author") == expected["answer_author"]
                and "".join(texts).strip()):
            if final_count:
                raise Rejected("text_after_final")
            if partial:
                partials += 1
            else:
                if finish != "STOP":
                    raise Rejected("missing_completion_metadata")
                if completed_names != set(rules) or replies != set(calls):
                    raise Rejected("answer_before_tools_complete")
                if not all(value in "".join(texts) for value in expected["answer_contains"]):
                    raise Rejected("answer_assertion_failed")
                final_count += 1
    if final_count != 1 or completed_names != set(rules) or replies != set(calls):
        raise Rejected("missing_completed_work")
    if partials < expected.get("min_partial_events", 0):
        raise Rejected("insufficient_partial_events")
    if expected.get("require_cache_hit", False) and not cached_max:
        raise Rejected("cache_hit_not_observed")
    return {"verdict": "PASS", "events": len(events), "correlated_tool_calls": len(calls),
            "complete_answers": final_count, "visible_partial_events": partials,
            "cache_usage_events": cache_events, "maximum_cached_tokens_observed": cached_max,
            "cache_evidence": "unknown" if cached_max is None else "hit" if cached_max > 0 else "zero",
            "scope": "saved_event_consistency_only", "network_calls": 0, "writes": 0}


def main(argv=None):
    parser = Parser(description=__doc__, epilog=(
        "Input: one complete JSON array of ADK events (snake_case or camelCase), "
        "up to 8 MiB/2000 events; expectation contract up to 64 KiB. "
        "Exactly one invocation, one call per declared tool and one STOP answer. "
        "No SSE parsing or live requests. Exit 0: accepted; 2: invalid input; "
        "3: acceptance failed. Errors omit input values and paths."))
    parser.add_argument("--events", required=True, help="Saved event-array JSON file.")
    parser.add_argument("--expect", required=True, help="Version-1 expectation JSON; see references/validation.md.")
    parser.add_argument("--dry-run", action="store_true", help="Explicit synonym for the always read-only validation.")
    args = parser.parse_args(argv)
    try:
        result = check_events(read_json(args.events, MAX_BYTES), read_json(args.expect, 65536))
    except Rejected as error:
        print(json.dumps({"verdict": "FAIL", "reason": str(error), "network_calls": 0, "writes": 0}))
        return 3
    except (InvalidInput, RecursionError, OverflowError):
        print(json.dumps({"verdict": "INVALID", "reason": "invalid_or_unsupported_input",
                          "network_calls": 0, "writes": 0}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
