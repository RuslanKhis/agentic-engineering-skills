#!/usr/bin/env python3
"""Convert a saved ADK session export into an ADK EvalSet JSON file.

Reads one saved session (a JSON object with an ``events`` list, a bare JSON
event array, or JSONL events) and writes an EvalSet in the field shape of
``google.adk.evaluation.eval_set.EvalSet`` / ``eval_case.EvalCase`` as read in
google-adk 2.8.0: ``eval_set_id``, ``eval_cases[].eval_id``,
``conversation[].user_content``, ``final_response``,
``intermediate_data.tool_uses`` / ``tool_responses`` /
``intermediate_responses`` and ``session_input``. Those models accept snake_case
field names (``populate_by_name=True``).

Selection: ``--select all`` writes one eval case holding the whole conversation;
``--select tool_error`` writes one eval case per invocation that contains a tool
error (a function response dict with a truthy ``error``, ``isError`` or
``is_error`` key, or an error status),
each case holding the conversation up to and including that invocation.

Redaction is a required step. By default every text part and every string inside
tool arguments or responses is replaced by ``[REDACTED]`` when it is longer than
``--max-text-chars`` or contains an email address or URL, and string values under
``error`` / ``error_message`` keys are always replaced. ``--allow-content``
disables that default scan; ``--redact-hook MODULE:FUNC`` runs a caller-supplied
function over each eval case dict after the default scan. Binary, file and
thought parts are dropped. Session state is never copied.

The only file written is ``--out``. The script never calls a model and never
imports the inspected application. ``--validate-with-sdk`` additionally runs
``EvalSet.model_validate`` when google-adk is importable; otherwise the report
says the output was not validated against the SDK.
"""
# Copyright (c) 2026 RuslanKhis. SPDX-License-Identifier: MIT
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 16 * 1024 * 1024
MAX_EVENTS = 5000
MAX_PARTS = 1000
MAX_DEPTH = 32
DEFAULT_MAX_TEXT_CHARS = 2000
REDACTED = "[REDACTED]"
ERROR_STATUS_VALUES = {"error", "failed", "failure"}
ERROR_TEXT_KEYS = {"error", "error_message", "errorMessage"}
ID_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
URL_PATTERN = re.compile(r"(?i)\b(?:https?|ftp|gs|s3)://|\bwww\.")
HOOK_PATTERN = re.compile(r"^[A-Za-z_][\w.]*:[A-Za-z_]\w*$")


class InvalidInput(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "events_to_eval_set: invalid arguments; values omitted; see --help.\n")


def read_bytes(path, limit):
    try:
        path = Path(path)
        if not stat.S_ISREG(path.lstat().st_mode):
            raise InvalidInput()
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        with os.fdopen(os.open(path, flags), "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise InvalidInput()
            raw = stream.read(limit + 1)
    except OSError:
        raise InvalidInput() from None
    if len(raw) > limit:
        raise InvalidInput()
    return raw


def load_session(raw):
    """Return (session_fields, events, format); raise InvalidInput."""
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        raise InvalidInput() from None
    try:
        document = json.loads(text)
    except ValueError:
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            raise InvalidInput() from None
        events = []
        for line in lines:
            try:
                events.append(json.loads(line))
            except ValueError:
                raise InvalidInput() from None
        return {}, events, "jsonl"
    if isinstance(document, dict):
        events = document.get("events")
        if not isinstance(events, list):
            raise InvalidInput()
        fields = {key: document.get(snake) if document.get(snake) is not None else document.get(camel)
                  for key, (snake, camel) in {"id": ("id", "id"), "app_name": ("app_name", "appName"),
                                               "user_id": ("user_id", "userId")}.items()}
        return {key: value for key, value in fields.items() if isinstance(value, str) and value}, events, "session_object"
    if isinstance(document, list):
        return {}, document, "event_array"
    raise InvalidInput()


def alias(value, snake, camel):
    if not isinstance(value, dict):
        return None
    result = value.get(snake)
    return result if result is not None else value.get(camel)


def number(value):
    return value if isinstance(value, (int, float)) and type(value) is not bool else None


def tool_response_error(response):
    if not isinstance(response, dict):
        return False
    if response.get("error") or response.get("isError") or response.get("is_error"):
        return True
    status = response.get("status")
    return isinstance(status, str) and status.strip().lower() in ERROR_STATUS_VALUES


def sanitise_id(value, fallback):
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", value) if isinstance(value, str) else ""
    cleaned = cleaned.strip("_")
    return cleaned if cleaned else fallback


def convert_part(part, counters):
    """Return a snake_case eval part dict, or None when the part is dropped."""
    if not isinstance(part, dict):
        counters["dropped_parts"] += 1
        return None
    call = alias(part, "function_call", "functionCall")
    reply = alias(part, "function_response", "functionResponse")
    if isinstance(call, dict) and isinstance(call.get("name"), str):
        value = {"name": call["name"], "args": call.get("args") if isinstance(call.get("args"), dict) else {}}
        if isinstance(call.get("id"), str):
            value["id"] = call["id"]
        return {"function_call": value}
    if isinstance(reply, dict) and isinstance(reply.get("name"), str):
        value = {"name": reply["name"],
                 "response": reply.get("response") if isinstance(reply.get("response"), dict) else {}}
        if isinstance(reply.get("id"), str):
            value["id"] = reply["id"]
        return {"function_response": value}
    if isinstance(part.get("text"), str) and not part.get("thought"):
        return {"text": part["text"]}
    counters["dropped_parts"] += 1
    return None


def group_invocations(events, counters):
    """Return ordered invocation summaries built from raw events."""
    order, groups = [], {}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            counters["skipped_malformed_items"] += 1
            continue
        invocation = alias(event, "invocation_id", "invocationId")
        if not isinstance(invocation, str) or not invocation:
            invocation = "unknown"
        if invocation not in groups:
            order.append(invocation)
            groups[invocation] = {"user_parts": [], "tool_uses": [], "tool_responses": [],
                                  "intermediate": [], "final": None, "has_tool_error": False,
                                  "timestamp": None, "index": index}
        group = groups[invocation]
        timestamp = number(event.get("timestamp"))
        if timestamp is not None and (group["timestamp"] is None or timestamp < group["timestamp"]):
            group["timestamp"] = timestamp
        content = event.get("content")
        if content is None or event.get("partial") is True:
            continue
        parts = content.get("parts") if isinstance(content, dict) else None
        if not isinstance(parts, list) or len(parts) > MAX_PARTS:
            counters["skipped_malformed_items"] += 1
            continue
        converted = [value for value in (convert_part(part, counters) for part in parts) if value is not None]
        author = event.get("author") if isinstance(event.get("author"), str) else "unknown"
        calls = [value["function_call"] for value in converted if "function_call" in value]
        replies = [value["function_response"] for value in converted if "function_response" in value]
        texts = [value for value in converted if "text" in value]
        if author == "user" and not replies:
            group["user_parts"].extend(texts)
            continue
        for call in calls:
            group["tool_uses"].append(call)
        for reply in replies:
            group["tool_responses"].append(reply)
            if tool_response_error(reply.get("response")):
                group["has_tool_error"] = True
        if texts and not calls and not replies:
            if group["final"] is not None:
                group["intermediate"].append([group["final"][0], group["final"][1]])
            group["final"] = (author, texts)
    return [dict(groups[name], invocation_id=name) for name in order]


def build_invocation(group):
    user_parts = group["user_parts"] or [{"text": REDACTED}]
    invocation = {
        "invocation_id": group["invocation_id"],
        "user_content": {"role": "user", "parts": user_parts},
        "intermediate_data": {
            "tool_uses": group["tool_uses"],
            "tool_responses": group["tool_responses"],
            "intermediate_responses": group["intermediate"],
        },
        "creation_timestamp": group["timestamp"] if group["timestamp"] is not None else 0.0,
    }
    if group["final"] is not None:
        invocation["final_response"] = {"role": "model", "parts": group["final"][1]}
    return invocation


def default_redact_text(text, max_chars):
    if len(text) > max_chars or EMAIL_PATTERN.search(text) or URL_PATTERN.search(text):
        return REDACTED
    return text


def redact_value(value, max_chars, counters, depth=0):
    if depth > MAX_DEPTH:
        counters["strings"] += 1
        return REDACTED
    if isinstance(value, str):
        replaced = default_redact_text(value, max_chars)
        if replaced is not value:
            counters["strings"] += 1
        return replaced
    if isinstance(value, list):
        return [redact_value(item, max_chars, counters, depth + 1) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if str(key) in ERROR_TEXT_KEYS and isinstance(item, str):
                counters["strings"] += 1
                result[str(key)] = REDACTED
            else:
                result[str(key)] = redact_value(item, max_chars, counters, depth + 1)
        return result
    return value


def redact_parts(parts, max_chars, counters):
    result = []
    for part in parts:
        if "text" in part:
            replaced = default_redact_text(part["text"], max_chars)
            if replaced is not part["text"]:
                counters["text_parts"] += 1
            result.append({"text": replaced})
        elif "function_call" in part:
            call = dict(part["function_call"])
            call["args"] = redact_value(call.get("args", {}), max_chars, counters)
            result.append({"function_call": call})
        elif "function_response" in part:
            reply = dict(part["function_response"])
            reply["response"] = redact_value(reply.get("response", {}), max_chars, counters)
            result.append({"function_response": reply})
    return result


def default_redact_case(case, max_chars, counters):
    for invocation in case["conversation"]:
        invocation["user_content"]["parts"] = redact_parts(invocation["user_content"]["parts"], max_chars, counters)
        if "final_response" in invocation:
            invocation["final_response"]["parts"] = redact_parts(invocation["final_response"]["parts"], max_chars, counters)
        data = invocation["intermediate_data"]
        data["tool_uses"] = [dict(call, args=redact_value(call.get("args", {}), max_chars, counters))
                             for call in data["tool_uses"]]
        data["tool_responses"] = [dict(reply, response=redact_value(reply.get("response", {}), max_chars, counters))
                                  for reply in data["tool_responses"]]
        data["intermediate_responses"] = [[author, redact_parts(parts, max_chars, counters)]
                                          for author, parts in data["intermediate_responses"]]
    return case


def load_hook(spec):
    if not isinstance(spec, str) or not HOOK_PATTERN.match(spec):
        raise InvalidInput()
    module_name, function_name = spec.split(":", 1)
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
    try:
        module = importlib.import_module(module_name)
        hook = getattr(module, function_name)
    except Exception:  # noqa: BLE001 - any import failure is a bad hook
        raise InvalidInput() from None
    if not callable(hook):
        raise InvalidInput()
    return hook


def apply_hook(hook, case):
    try:
        result = hook(json.loads(json.dumps(case)))
    except Exception:  # noqa: BLE001 - a failing hook must fail the conversion
        raise InvalidInput() from None
    if not isinstance(result, dict):
        raise InvalidInput()
    return result


def build_eval_set(groups, settings, counters):
    selected = groups if settings["select"] == "all" else [group for group in groups if group["has_tool_error"]]
    cases = []
    if settings["select"] == "all" and selected:
        cases.append(make_case(settings["eval_set_id"], [build_invocation(group) for group in selected], settings))
    elif settings["select"] == "tool_error":
        for position, group in enumerate(groups):
            if not group["has_tool_error"]:
                continue
            conversation = [build_invocation(item) for item in groups[:position + 1]]
            eval_id = sanitise_id("%s_%s" % (settings["eval_set_id"], group["invocation_id"]), "case_%d" % position)
            cases.append(make_case(eval_id, conversation, settings))
    processed = []
    for case in cases:
        if not settings["allow_content"]:
            case = default_redact_case(case, settings["max_text_chars"], counters["redactions"])
        if settings["hook"] is not None:
            case = apply_hook(settings["hook"], case)
        processed.append(case)
    timestamps = [group["timestamp"] for group in selected if group["timestamp"] is not None]
    return {
        "eval_set_id": settings["eval_set_id"],
        "name": settings["eval_set_id"],
        "description": ("Generated by events_to_eval_set from a saved ADK session; selection=%s; "
                        "default redaction %s; expected outputs are the observed outputs and need review."
                        % (settings["select"], "disabled" if settings["allow_content"] else "applied")),
        "eval_cases": processed,
        "creation_timestamp": max(timestamps) if timestamps else 0.0,
    }, len(selected)


def make_case(eval_id, conversation, settings):
    return {
        "eval_id": eval_id,
        "conversation": conversation,
        "session_input": {"app_name": settings["app_name"], "user_id": settings["user_id"], "state": {}},
        "creation_timestamp": conversation[-1]["creation_timestamp"] if conversation else 0.0,
    }


def check_structure(eval_set):
    """Offline structural checks mirroring the 2.8.0 models; return a list of problems."""
    problems = []
    if not ID_PATTERN.match(eval_set.get("eval_set_id", "")):
        problems.append("eval_set_id_pattern")
    if not eval_set.get("eval_cases"):
        problems.append("no_eval_cases")
    seen = set()
    for case in eval_set.get("eval_cases", []):
        if not ID_PATTERN.match(case.get("eval_id", "")):
            problems.append("eval_id_pattern")
        if case.get("eval_id") in seen:
            problems.append("duplicate_eval_id")
        seen.add(case.get("eval_id"))
        if ("conversation" in case) == ("conversation_scenario" in case):
            problems.append("conversation_xor_scenario")
        if not case.get("conversation"):
            problems.append("empty_conversation")
        for invocation in case.get("conversation", []):
            parts = invocation.get("user_content", {}).get("parts")
            if not parts:
                problems.append("user_content_without_parts")
            data = invocation.get("intermediate_data", {})
            for key in ("tool_uses", "tool_responses", "intermediate_responses"):
                if not isinstance(data.get(key), list):
                    problems.append("intermediate_data_%s" % key)
        session_input = case.get("session_input", {})
        if not session_input.get("app_name") or not session_input.get("user_id"):
            problems.append("session_input_identity")
    return sorted(set(problems))


def validate_with_sdk(eval_set):
    try:
        module = importlib.import_module("google.adk.evaluation.eval_set")
    except Exception:  # noqa: BLE001 - absence of the SDK is the expected case
        return "not validated against SDK: google-adk not importable"
    try:
        module.EvalSet.model_validate(eval_set)
    except Exception as error:  # noqa: BLE001 - report the failure class only
        return "failed: %s" % type(error).__name__
    return "validated with google.adk.evaluation.eval_set.EvalSet.model_validate"


def positive_int(value):
    try:
        result = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("expected a positive integer") from None
    if result <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return result


def main(argv=None):
    parser = Parser(description=__doc__, epilog=(
        "Exit 0: eval set written; 1: malformed input, no case selected, hook "
        "failure or existing output without --force; 2: invalid arguments. The "
        "report names counts and the output file name only."))
    parser.add_argument("--session", required=True, help="Saved session export path.")
    parser.add_argument("--out", required=True, help="EvalSet JSON file to write (conventionally *.evalset.json).")
    parser.add_argument("--select", choices=("tool_error", "all"), default="all",
                        help="Which invocations become eval cases (default all).")
    parser.add_argument("--redact-hook", metavar="MODULE:FUNC",
                        help="Caller-supplied function(case_dict) -> case_dict applied after the default scan; "
                             "MODULE is imported from the current directory or PYTHONPATH.")
    parser.add_argument("--allow-content", action="store_true",
                        help="Disable the default text redaction (a hook may still run).")
    parser.add_argument("--max-text-chars", type=positive_int, default=DEFAULT_MAX_TEXT_CHARS,
                        help="Default scan replaces text longer than this (default 2000).")
    parser.add_argument("--eval-set-id", help="Override the eval set id (letters, digits, underscore).")
    parser.add_argument("--app-name", help="session_input.app_name (default: session app_name or 'app').")
    parser.add_argument("--user-id", help="session_input.user_id (default: 'eval_user'; never the real user).")
    parser.add_argument("--validate-with-sdk", action="store_true",
                        help="Also run EvalSet.model_validate when google-adk is importable.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing --out file.")
    parser.add_argument("--dry-run", action="store_true", help="Build and validate without writing.")
    args = parser.parse_args(argv)

    def fail(reason):
        print(json.dumps({"verdict": "MALFORMED", "reason": reason, "network_calls": 0, "writes": 0}))
        return 1

    out_path = Path(args.out)
    if out_path.exists() and not args.force and not args.dry_run:
        return fail("output_exists_use_force")
    try:
        hook = load_hook(args.redact_hook) if args.redact_hook else None
    except InvalidInput:
        return fail("invalid_redact_hook")
    try:
        session, events, source_format = load_session(read_bytes(args.session, MAX_BYTES))
        if not events or len(events) > MAX_EVENTS:
            raise InvalidInput()
        counters = {"skipped_malformed_items": 0, "dropped_parts": 0,
                    "redactions": {"text_parts": 0, "strings": 0}}
        groups = group_invocations(events, counters)
        settings = {
            "select": args.select,
            "allow_content": args.allow_content,
            "max_text_chars": args.max_text_chars,
            "hook": hook,
            "eval_set_id": sanitise_id(args.eval_set_id or session.get("id") or out_path.name.split(".")[0], "eval_set"),
            "app_name": args.app_name or session.get("app_name") or "app",
            "user_id": args.user_id or "eval_user",
        }
        eval_set, selected = build_eval_set(groups, settings, counters)
    except (InvalidInput, RecursionError, OverflowError):
        return fail("invalid_or_unsupported_input")
    problems = check_structure(eval_set)
    report = {
        "verdict": "INSPECTED",
        "source_format": source_format,
        "events": len(events),
        "invocations_seen": len(groups),
        "invocations_selected": selected,
        "eval_cases": len(eval_set["eval_cases"]),
        "eval_set_id": eval_set["eval_set_id"],
        "skipped_malformed_items": counters["skipped_malformed_items"],
        "dropped_parts": counters["dropped_parts"],
        "redactions": counters["redactions"],
        "default_redaction": "disabled" if args.allow_content else "applied",
        "hook": args.redact_hook or None,
        "structural_problems": problems,
        "sdk_validation": validate_with_sdk(eval_set) if args.validate_with_sdk else "not run (pass --validate-with-sdk)",
        "out": out_path.name,
        "network_calls": 0,
        "writes": 0,
    }
    if not eval_set["eval_cases"]:
        report["verdict"] = "NO_CASES"
    elif problems or counters["skipped_malformed_items"]:
        report["verdict"] = "PARTIAL"
    if report["verdict"] != "NO_CASES" and not args.dry_run:
        try:
            out_path.write_text(json.dumps(eval_set, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        except OSError:
            return fail("output_not_writable")
        report["writes"] = 1
    print(json.dumps(report, sort_keys=True))
    return 0 if report["verdict"] == "INSPECTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
