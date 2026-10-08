#!/usr/bin/env python3
"""Summarise model calls, tool calls, usage, timing and optional cost per invocation.

Reads one saved ADK session export (a JSON object with an ``events`` list, a bare
JSON event array, or JSONL with one event per line) and emits one row per
invocation: logical model calls, tool calls and tool errors by name, the last
authoritative usage per logical model call (streaming partials are not summed;
the non-partial final event wins, else the newest partial report), finish
reasons, model error codes, wall time per step from event timestamps, and an
optional cost estimate from a user-supplied price table. Never calls a model,
imports application code, writes files or prints event text. Usage figures are
the model's reported counts; cost is only as good as the supplied prices.
"""
# Copyright (c) 2026 RuslanKhis. SPDX-License-Identifier: MIT
from __future__ import annotations

import argparse
import csv
import io
import json
import os
from pathlib import Path
import stat
import sys

MAX_BYTES = 16 * 1024 * 1024
MAX_EVENTS = 5000
MAX_PARTS = 1000
MAX_PRICE_BYTES = 256 * 1024
LONGEST_STEPS = 3
USAGE_RULE = "last_authoritative_usage_per_logical_call_partials_not_summed"
ERROR_STATUS_VALUES = {"error", "failed", "failure"}
CSV_COLUMNS = (
    "invocation_id", "events", "model_calls", "partial_events", "tool_calls",
    "tool_responses", "tool_errors", "model_error_codes", "input_tokens",
    "output_tokens", "cached_input_tokens", "reasoning_output_tokens",
    "usage_unknown_calls", "wall_seconds", "estimated_cost", "flags",
)


class InvalidInput(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "invocation_summary: invalid arguments; values omitted; see --help.\n")


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


def load_events(raw):
    """Return (events, format) from JSON or JSONL bytes; raise InvalidInput."""
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
        return events, "jsonl"
    if isinstance(document, dict):
        events = document.get("events")
        if not isinstance(events, list):
            raise InvalidInput()
        return events, "session_object"
    if isinstance(document, list):
        return document, "event_array"
    raise InvalidInput()


def alias(value, snake, camel):
    if not isinstance(value, dict):
        return None
    result = value.get(snake)
    return result if result is not None else value.get(camel)


def nonnegative_int(value):
    return value if type(value) is int and value >= 0 else None


def number(value):
    return value if isinstance(value, (int, float)) and type(value) is not bool else None


def usage_counts(usage):
    """Return the usage fields this helper reads, each an int or None."""
    if not isinstance(usage, dict):
        return None
    fields = {
        "prompt": ("prompt_token_count", "promptTokenCount"),
        "candidates": ("candidates_token_count", "candidatesTokenCount"),
        "thoughts": ("thoughts_token_count", "thoughtsTokenCount"),
        "cached": ("cached_content_token_count", "cachedContentTokenCount"),
        "tool_use": ("tool_use_prompt_token_count", "toolUsePromptTokenCount"),
        "total": ("total_token_count", "totalTokenCount"),
    }
    counts = {key: nonnegative_int(alias(usage, snake, camel)) for key, (snake, camel) in fields.items()}
    if counts["prompt"] is None and counts["candidates"] is None and counts["thoughts"] is None:
        return None
    return counts


def tool_response_error(response):
    """A dict with a truthy ``error``, MCP ``isError``/``is_error`` key, or an error status."""
    if not isinstance(response, dict):
        return False
    if response.get("error") or response.get("isError") or response.get("is_error"):
        return True
    status = response.get("status")
    return isinstance(status, str) and status.strip().lower() in ERROR_STATUS_VALUES


def load_prices(raw):
    """Validate a user-supplied price table; raise InvalidInput on any defect."""
    try:
        table = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError):
        raise InvalidInput() from None
    if not isinstance(table, dict):
        raise InvalidInput()
    per_million = table.get("per_million")
    currency = table.get("currency", "unspecified")
    if not isinstance(per_million, dict) or not per_million or not isinstance(currency, str):
        raise InvalidInput()
    for model, entry in per_million.items():
        if not isinstance(model, str) or not isinstance(entry, dict):
            raise InvalidInput()
        for key in ("input", "output"):
            if number(entry.get(key)) is None or entry[key] < 0:
                raise InvalidInput()
        for key in ("cached_input",):
            if key in entry and (number(entry[key]) is None or entry[key] < 0):
                raise InvalidInput()
    return {"currency": currency, "per_million": per_million}


def price_call(prices, model, totals):
    """Return (cost, flag) for one model call; flag names the shortfall when any."""
    entry = prices["per_million"].get(model) if isinstance(model, str) else None
    flag = None
    if entry is None:
        entry = prices["per_million"].get("default")
        flag = "priced_with_default_entry" if entry is not None else "unpriced_model"
    if entry is None:
        return None, flag
    cached = totals["cached"] or 0
    noncached = max((totals["input"] or 0) - cached, 0)
    cached_rate = entry.get("cached_input")
    if cached_rate is None:
        cached_rate = entry["input"]
        if cached:
            flag = flag or "cached_input_charged_at_input_rate"
    cost = (noncached * entry["input"] + cached * cached_rate + (totals["output"] or 0) * entry["output"]) / 1_000_000
    return cost, flag


def new_record():
    return {
        "events": 0, "partial_events": 0, "model_calls": 0, "usage_unknown_calls": 0,
        "usage_from_partial_calls": 0, "tool_calls": 0, "tool_responses": 0,
        "tool_calls_by_name": {}, "tool_errors_by_name": {}, "finish_reasons": {},
        "model_error_codes": {}, "authors": {}, "orphan_calls": 0,
        "tokens": {"input": 0, "output": 0, "cached": 0, "reasoning": 0, "tool_use": 0, "reported_total": 0},
        "calls": [], "pending_usage": None, "pending_call_ids": set(),
        "first_timestamp": None, "last_timestamp": None, "previous_timestamp": None,
        "steps": [], "missing_timestamps": 0,
    }


def classify_parts(parts):
    calls, replies, has_text = [], [], False
    for part in parts:
        if not isinstance(part, dict):
            continue
        call = alias(part, "function_call", "functionCall")
        reply = alias(part, "function_response", "functionResponse")
        if isinstance(call, dict):
            calls.append(call)
        elif isinstance(reply, dict):
            replies.append(reply)
        elif isinstance(part.get("text"), str) and not part.get("thought"):
            has_text = True
    return calls, replies, has_text


def inspect_events(events, prices=None):
    if not isinstance(events, list) or not events or len(events) > MAX_EVENTS:
        raise InvalidInput()
    order, records, skipped = [], {}, 0
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            skipped += 1
            continue
        invocation = alias(event, "invocation_id", "invocationId")
        if not isinstance(invocation, str) or not invocation:
            invocation = "unknown"
        author = event.get("author") if isinstance(event.get("author"), str) and event.get("author") else "unknown"
        if invocation not in records:
            order.append(invocation)
            records[invocation] = new_record()
        record = records[invocation]
        record["events"] += 1
        record["authors"][author] = record["authors"].get(author, 0) + 1

        timestamp = number(event.get("timestamp"))
        if timestamp is None:
            record["missing_timestamps"] += 1
        else:
            if record["first_timestamp"] is None or timestamp < record["first_timestamp"]:
                record["first_timestamp"] = timestamp
            if record["last_timestamp"] is None or timestamp > record["last_timestamp"]:
                record["last_timestamp"] = timestamp

        content = event.get("content")
        parts = content.get("parts") if isinstance(content, dict) else None
        if content is not None and (not isinstance(content, dict) or (parts is not None and not isinstance(parts, list))):
            skipped += 1
            parts = None
        if isinstance(parts, list) and len(parts) > MAX_PARTS:
            skipped += 1
            parts = None
        calls, replies, has_text = classify_parts(parts or [])
        partial = event.get("partial") is True
        usage = usage_counts(alias(event, "usage_metadata", "usageMetadata"))
        error_code = alias(event, "error_code", "errorCode")
        if isinstance(error_code, str) and error_code:
            record["model_error_codes"][error_code] = record["model_error_codes"].get(error_code, 0) + 1

        kind = "other"
        if author == "user" and not replies:
            kind = "user"
        elif replies:
            kind = "tool_response"
            record["tool_responses"] += len(replies)
            for reply in replies:
                name = reply.get("name") if isinstance(reply.get("name"), str) else "unknown"
                reply_id = reply.get("id") if isinstance(reply.get("id"), str) else None
                if reply_id is not None:
                    record["pending_call_ids"].discard(reply_id)
                if tool_response_error(reply.get("response")):
                    record["tool_errors_by_name"][name] = record["tool_errors_by_name"].get(name, 0) + 1
        elif partial:
            kind = "partial"
            record["partial_events"] += 1
            if usage is not None:
                record["pending_usage"] = usage
        elif calls or has_text or usage is not None or (isinstance(error_code, str) and error_code):
            kind = "model_call"
            record["model_calls"] += 1
            for call in calls:
                name = call.get("name") if isinstance(call.get("name"), str) else "unknown"
                record["tool_calls"] += 1
                record["tool_calls_by_name"][name] = record["tool_calls_by_name"].get(name, 0) + 1
                call_id = call.get("id") if isinstance(call.get("id"), str) else None
                if call_id is not None:
                    record["pending_call_ids"].add(call_id)
            finish = alias(event, "finish_reason", "finishReason")
            if isinstance(finish, str) and finish:
                record["finish_reasons"][finish] = record["finish_reasons"].get(finish, 0) + 1
            authoritative = usage
            if authoritative is None and record["pending_usage"] is not None:
                authoritative = record["pending_usage"]
                record["usage_from_partial_calls"] += 1
            record["pending_usage"] = None
            model = alias(event, "model_version", "modelVersion")
            record["calls"].append((authoritative, model if isinstance(model, str) else None, index))
            if authoritative is None:
                record["usage_unknown_calls"] += 1
            else:
                add_usage(record["tokens"], authoritative)

        if timestamp is not None and kind != "partial":
            if record["previous_timestamp"] is not None:
                record["steps"].append({"event_index": index, "kind": kind, "author": author,
                                        "seconds_from_previous": round(timestamp - record["previous_timestamp"], 6)})
            record["previous_timestamp"] = timestamp

    rows, totals = [], {"invocations": len(order), "model_calls": 0, "tool_calls": 0, "tool_errors": 0,
                        "input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0,
                        "reasoning_output_tokens": 0, "usage_unknown_calls": 0, "estimated_cost": None}
    for invocation in order:
        row = build_row(invocation, records[invocation], prices)
        rows.append(row)
        for key in ("model_calls", "tool_calls", "usage_unknown_calls"):
            totals[key] += row[key]
        totals["tool_errors"] += row["tool_errors"]
        for key in ("input_tokens", "output_tokens", "cached_input_tokens", "reasoning_output_tokens"):
            totals[key] += row["usage"][key]
        if row["estimated_cost"] is not None and row["estimated_cost"]["amount"] is not None:
            totals["estimated_cost"] = round((totals["estimated_cost"] or 0.0) + row["estimated_cost"]["amount"], 8)
    return {
        "verdict": "PARTIAL" if skipped else "INSPECTED",
        "events": len(events),
        "skipped_malformed_items": skipped,
        "invocations": rows,
        "totals": totals,
        "usage_counting_rule": USAGE_RULE,
        "cost_basis": None if prices is None else {"currency": prices["currency"], "source": "user_supplied_price_table"},
        "scope": "saved_session_estimate_only",
        "network_calls": 0,
        "writes": 0,
    }


def add_usage(tokens, counts):
    tokens["input"] += (counts["prompt"] or 0) + (counts["tool_use"] or 0)
    tokens["output"] += (counts["candidates"] or 0) + (counts["thoughts"] or 0)
    tokens["cached"] += counts["cached"] or 0
    tokens["reasoning"] += counts["thoughts"] or 0
    tokens["tool_use"] += counts["tool_use"] or 0
    tokens["reported_total"] += counts["total"] or 0


def build_row(invocation, record, prices):
    flags = []
    if record["usage_unknown_calls"]:
        flags.append("usage_missing_on_%d_model_calls" % record["usage_unknown_calls"])
    if record["usage_from_partial_calls"]:
        flags.append("usage_taken_from_newest_partial_on_%d_calls" % record["usage_from_partial_calls"])
    if record["partial_events"]:
        flags.append("partial_events_present")
    if record["missing_timestamps"]:
        flags.append("timestamps_missing")
    if record["tool_errors_by_name"]:
        flags.append("tool_errors")
    if record["model_error_codes"]:
        flags.append("model_error_codes")
    if record["pending_call_ids"]:
        flags.append("orphan_function_calls")
    cost = None
    if prices is not None:
        amount, unpriced, cost_flags = 0.0, 0, set()
        for usage, model, _ in record["calls"]:
            if usage is None:
                unpriced += 1
                continue
            call_totals = {"input": (usage["prompt"] or 0) + (usage["tool_use"] or 0),
                           "output": (usage["candidates"] or 0) + (usage["thoughts"] or 0),
                           "cached": usage["cached"] or 0}
            value, flag = price_call(prices, model, call_totals)
            if flag:
                cost_flags.add(flag)
            if value is None:
                unpriced += 1
            else:
                amount += value
        priced = len(record["calls"]) - unpriced
        cost = {"amount": round(amount, 8) if priced else None, "currency": prices["currency"],
                "priced_calls": priced, "unpriced_calls": unpriced}
        flags.extend(sorted(cost_flags))
    wall = None
    if record["first_timestamp"] is not None and record["last_timestamp"] is not None:
        wall = round(record["last_timestamp"] - record["first_timestamp"], 6)
    longest = sorted(record["steps"], key=lambda step: (-step["seconds_from_previous"], step["event_index"]))[:LONGEST_STEPS]
    tokens = record["tokens"]
    return {
        "invocation_id": invocation,
        "events": record["events"],
        "events_by_author": dict(sorted(record["authors"].items())),
        "model_calls": record["model_calls"],
        "partial_events": record["partial_events"],
        "tool_calls": record["tool_calls"],
        "tool_responses": record["tool_responses"],
        "tool_calls_by_name": dict(sorted(record["tool_calls_by_name"].items())),
        "tool_errors": sum(record["tool_errors_by_name"].values()),
        "tool_errors_by_name": dict(sorted(record["tool_errors_by_name"].items())),
        "finish_reasons": dict(sorted(record["finish_reasons"].items())),
        "model_error_codes": dict(sorted(record["model_error_codes"].items())),
        "usage": {
            "input_tokens": tokens["input"], "output_tokens": tokens["output"],
            "cached_input_tokens": tokens["cached"], "reasoning_output_tokens": tokens["reasoning"],
            "tool_use_prompt_tokens": tokens["tool_use"], "reported_total_tokens": tokens["reported_total"],
            "derived_total_tokens": tokens["input"] + tokens["output"],
        },
        "usage_unknown_calls": record["usage_unknown_calls"],
        "wall_seconds": wall,
        "steps": record["steps"],
        "longest_steps": longest,
        "estimated_cost": cost,
        "flags": flags,
    }


def to_csv(result):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for row in result["invocations"]:
        cost = row["estimated_cost"]
        writer.writerow([
            row["invocation_id"], row["events"], row["model_calls"], row["partial_events"],
            row["tool_calls"], row["tool_responses"], row["tool_errors"],
            sum(row["model_error_codes"].values()), row["usage"]["input_tokens"],
            row["usage"]["output_tokens"], row["usage"]["cached_input_tokens"],
            row["usage"]["reasoning_output_tokens"], row["usage_unknown_calls"],
            "" if row["wall_seconds"] is None else row["wall_seconds"],
            "" if cost is None or cost["amount"] is None else cost["amount"],
            ";".join(row["flags"]),
        ])
    return buffer.getvalue()


def main(argv=None):
    parser = Parser(description=__doc__, epilog=(
        "Input: a saved session export (JSON object with an events list, a JSON "
        "event array, or JSONL events), up to 16 MiB/5000 events. Prices: a JSON "
        "object {\"currency\": \"USD\", \"per_million\": {\"<model_version>\": "
        "{\"input\": n, \"output\": n, \"cached_input\": n}, \"default\": {...}}}; "
        "no prices are built in. Exit 0: inspected; 1: partial or malformed "
        "input; 2: invalid arguments. Output contains counts, identifiers, tool "
        "names, finish reasons and error codes only."))
    parser.add_argument("--session", required=True, help="Saved session export path.")
    parser.add_argument("--prices", help="Optional price table JSON (see epilog).")
    parser.add_argument("--format", choices=("json", "csv"), default="json",
                        help="Output format (default json).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Explicit synonym for the always read-only inspection.")
    args = parser.parse_args(argv)
    try:
        prices = load_prices(read_bytes(args.prices, MAX_PRICE_BYTES)) if args.prices else None
    except (InvalidInput, RecursionError):
        print(json.dumps({"verdict": "MALFORMED", "reason": "invalid_price_table",
                          "network_calls": 0, "writes": 0}))
        return 1
    try:
        events, source_format = load_events(read_bytes(args.session, MAX_BYTES))
        result = inspect_events(events, prices)
    except (InvalidInput, RecursionError, OverflowError):
        print(json.dumps({"verdict": "MALFORMED", "reason": "invalid_or_unsupported_input",
                          "network_calls": 0, "writes": 0}))
        return 1
    result["source_format"] = source_format
    if args.format == "csv":
        sys.stdout.write(to_csv(result))
    else:
        print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "INSPECTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
