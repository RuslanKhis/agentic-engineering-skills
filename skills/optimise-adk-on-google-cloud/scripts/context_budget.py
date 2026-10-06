#!/usr/bin/env python3
"""Estimate per-invocation context composition from a saved ADK session export.

Reads one JSON file (an object with an ``events`` list, or a bare event list) or
JSONL with one event per line. Reports event counts, function call/response
pairs and orphans, bytes and bytes/4 estimates by part type and author, the
largest tool results, estimated growth per invocation, compaction spans and the
last authoritative usage metadata per invocation. Never calls a model, imports
application code, writes files or prints event text. bytes/4 is an estimate,
not provider usage; ``usage_metadata`` values are the measurement when present.
"""
# Copyright (c) 2026 RuslanKhis. SPDX-License-Identifier: MIT
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat
import sys

MAX_BYTES = 16 * 1024 * 1024
MAX_EVENTS = 5000
MAX_PARTS = 1000
DEFAULT_MAX_RESULT_BYTES = 20000
LARGEST_RESULTS = 3
ESTIMATE_METHOD = "utf8_bytes_div_4_estimate_not_provider_usage"


class InvalidInput(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "context_budget: invalid arguments; values omitted; see --help.\n")


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
        document = None
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


def encoded(value):
    try:
        return len(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8"))
    except (TypeError, ValueError, RecursionError):
        return 0


def nonnegative_int(value):
    return value if type(value) is int and value >= 0 else None


def new_bucket():
    return {"text": 0, "function_call": 0, "function_response": 0, "other": 0}


def inspect_events(events, max_result_bytes):
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        raise InvalidInput()
    if not events:
        raise InvalidInput()
    order = []
    invocations = {}
    skipped = 0
    compactions = []
    timeline = []  # (index, timestamp or None, is_compaction)
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            skipped += 1
            continue
        invocation = alias(event, "invocation_id", "invocationId")
        if not isinstance(invocation, str) or not invocation:
            invocation = "unknown"
        author = event.get("author")
        if not isinstance(author, str) or not author:
            author = "unknown"
        if invocation not in invocations:
            order.append(invocation)
            invocations[invocation] = {
                "events": 0, "authors": {}, "bytes_by_part": new_bucket(),
                "calls": {}, "responses": {}, "results": [],
                "usage": None, "compaction_events": 0, "state_delta_events": 0,
                "call_sequence": [], "response_sequence": [],
            }
        record = invocations[invocation]
        record["events"] += 1
        timestamp = event.get("timestamp")
        timestamp = timestamp if isinstance(timestamp, (int, float)) and type(timestamp) is not bool else None
        actions = event.get("actions")
        compaction = alias(actions, "compaction", "compaction")
        is_compaction = isinstance(compaction, dict)
        if is_compaction:
            record["compaction_events"] += 1
            summary = alias(compaction, "compacted_content", "compactedContent")
            compactions.append({
                "event_index": index,
                "invocation_id": invocation,
                "start_timestamp": alias(compaction, "start_timestamp", "startTimestamp"),
                "end_timestamp": alias(compaction, "end_timestamp", "endTimestamp"),
                "summary_bytes": encoded(summary) if summary is not None else 0,
                "covered_events": 0,
            })
        if isinstance(alias(actions, "state_delta", "stateDelta"), dict) and alias(actions, "state_delta", "stateDelta"):
            record["state_delta_events"] += 1
        timeline.append((index, timestamp, is_compaction))
        usage = alias(event, "usage_metadata", "usageMetadata")
        if isinstance(usage, dict):
            observed = {
                "prompt_token_count": nonnegative_int(alias(usage, "prompt_token_count", "promptTokenCount")),
                "candidates_token_count": nonnegative_int(alias(usage, "candidates_token_count", "candidatesTokenCount")),
                "cached_content_token_count": nonnegative_int(alias(usage, "cached_content_token_count", "cachedContentTokenCount")),
                "event_index": index,
            }
            if any(value is not None for key, value in observed.items() if key != "event_index"):
                record["usage"] = observed
        content = event.get("content")
        if content is None:
            continue
        if not isinstance(content, dict):
            skipped += 1
            continue
        parts = content.get("parts")
        if parts is None:
            parts = []
        if not isinstance(parts, list) or len(parts) > MAX_PARTS:
            skipped += 1
            continue
        event_bytes = 0
        for part in parts:
            if not isinstance(part, dict):
                skipped += 1
                continue
            call = alias(part, "function_call", "functionCall")
            reply = alias(part, "function_response", "functionResponse")
            text = part.get("text")
            if isinstance(call, dict):
                size = encoded({"name": call.get("name"), "args": call.get("args")})
                record["bytes_by_part"]["function_call"] += size
                name = call.get("name") if isinstance(call.get("name"), str) else "unknown"
                call_id = call.get("id") if isinstance(call.get("id"), str) and call.get("id") else None
                record["call_sequence"].append((call_id, name, index))
            elif isinstance(reply, dict):
                size = encoded(reply.get("response"))
                record["bytes_by_part"]["function_response"] += size
                name = reply.get("name") if isinstance(reply.get("name"), str) else "unknown"
                reply_id = reply.get("id") if isinstance(reply.get("id"), str) and reply.get("id") else None
                record["response_sequence"].append((reply_id, name, index))
                record["results"].append({"name": name, "bytes": size, "event_index": index})
            elif isinstance(text, str):
                size = len(text.encode("utf-8"))
                record["bytes_by_part"]["text"] += size
            else:
                size = encoded(part)
                record["bytes_by_part"]["other"] += size
            event_bytes += size
        record["authors"][author] = record["authors"].get(author, 0) + event_bytes

    for span in compactions:
        start, end = span["start_timestamp"], span["end_timestamp"]
        if isinstance(start, (int, float)) and isinstance(end, (int, float)):
            span["covered_events"] = sum(
                1 for _, timestamp, is_compaction in timeline
                if timestamp is not None and not is_compaction and start <= timestamp <= end
            )
        else:
            span["covered_events"] = None

    report_invocations = []
    cumulative = 0
    flagged = []
    for invocation in order:
        record = invocations[invocation]
        pairs, orphan_calls, orphan_responses = pair_tools(record["call_sequence"], record["response_sequence"])
        total = sum(record["bytes_by_part"].values())
        cumulative += total
        largest = sorted(record["results"], key=lambda item: (-item["bytes"], item["event_index"]))[:LARGEST_RESULTS]
        over = [item for item in record["results"] if item["bytes"] > max_result_bytes]
        for item in over:
            flagged.append({"invocation_id": invocation, **item})
        report_invocations.append({
            "invocation_id": invocation,
            "events": record["events"],
            "function_call_pairs": pairs,
            "orphan_function_calls": orphan_calls,
            "orphan_function_responses": orphan_responses,
            "bytes_by_part": record["bytes_by_part"],
            "estimated_tokens_by_part": {key: value // 4 for key, value in record["bytes_by_part"].items()},
            "bytes_by_author": dict(sorted(record["authors"].items())),
            "invocation_bytes": total,
            "invocation_estimated_tokens": total // 4,
            "cumulative_bytes": cumulative,
            "cumulative_estimated_tokens": cumulative // 4,
            "largest_tool_results": largest,
            "tool_results_over_limit": len(over),
            "compaction_events": record["compaction_events"],
            "state_delta_events": record["state_delta_events"],
            "last_usage_metadata": record["usage"],
        })
    growth = [{"invocation_id": item["invocation_id"],
               "cumulative_estimated_tokens": item["cumulative_estimated_tokens"],
               "delta_estimated_tokens": item["invocation_estimated_tokens"]}
              for item in report_invocations]
    return {
        "verdict": "PARTIAL" if skipped else "INSPECTED",
        "events": len(events),
        "skipped_malformed_items": skipped,
        "invocations": report_invocations,
        "growth": growth,
        "compaction": compactions,
        "flagged_tool_results": flagged,
        "max_result_bytes": max_result_bytes,
        "token_estimate_method": ESTIMATE_METHOD,
        "scope": "saved_session_estimate_only",
        "network_calls": 0,
        "writes": 0,
    }


def pair_tools(calls, responses):
    """Pair by id when both sides carry one, otherwise by name in order."""
    pairs = 0
    pending_by_id = {}
    pending_by_name = {}
    orphan_responses = []
    for call_id, name, index in calls:
        if call_id is not None:
            pending_by_id[call_id] = (name, index)
        else:
            pending_by_name.setdefault(name, []).append(index)
    for reply_id, name, index in responses:
        if reply_id is not None and reply_id in pending_by_id:
            pending_by_id.pop(reply_id)
            pairs += 1
        elif reply_id is None and pending_by_name.get(name):
            pending_by_name[name].pop(0)
            pairs += 1
        else:
            orphan_responses.append({"name": name, "event_index": index})
    orphan_calls = [{"name": name, "event_index": index} for name, index in pending_by_id.values()]
    for name, indexes in pending_by_name.items():
        orphan_calls.extend({"name": name, "event_index": index} for index in indexes)
    orphan_calls.sort(key=lambda item: item["event_index"])
    return pairs, orphan_calls, orphan_responses


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("expected a positive integer") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def main(argv=None):
    parser = Parser(description=__doc__, epilog=(
        "Input: a saved session export (JSON object with an events list, a JSON "
        "event array, or JSONL events), up to 16 MiB/5000 events. Exit 0: "
        "inspected; 1: partial or malformed input; 2: invalid arguments. Output "
        "contains counts, byte sizes, tool names and identifiers only."))
    parser.add_argument("--session", required=True, help="Saved session export path.")
    parser.add_argument("--max-result-bytes", type=positive_int, default=DEFAULT_MAX_RESULT_BYTES,
                        help="Flag function responses whose encoded size exceeds this (default 20000).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Explicit synonym for the always read-only inspection.")
    args = parser.parse_args(argv)
    try:
        events, source_format = load_events(read_bytes(args.session, MAX_BYTES))
        result = inspect_events(events, args.max_result_bytes)
    except (InvalidInput, RecursionError, OverflowError):
        print(json.dumps({"verdict": "MALFORMED", "reason": "invalid_or_unsupported_input",
                          "network_calls": 0, "writes": 0}))
        return 1
    result["source_format"] = source_format
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "INSPECTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
