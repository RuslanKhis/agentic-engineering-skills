#!/usr/bin/env python3
"""Report the context cost of tool results from recorded ADK events.

Reads a JSON file (a list of events, or an object with an `events` list) or
JSONL (one event per line). For every part with `function_response` /
`functionResponse` it measures the serialised response; for every
`function_call` / `functionCall` it counts the call. Only tool names, counts
and sizes are printed; response content never is. Token figures are a
bytes/4 estimate, labelled as such.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path


def positive(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def load_events(path, issues):
    """Return a list of candidate events; malformed input is reported, never raised."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        issues.append({"reason": "unreadable_file"})
        return []
    try:
        document = json.loads(text)
    except ValueError:
        document = None
    if document is not None:
        if isinstance(document, list):
            return document
        if isinstance(document, dict):
            events = document.get("events")
            if isinstance(events, list):
                return events
            return [document]
        issues.append({"reason": "unsupported_json_shape"})
        return []
    events = []
    bad_lines = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except ValueError:
            bad_lines += 1
            continue
        if isinstance(item, list):
            events.extend(item)
        else:
            events.append(item)
    if bad_lines:
        issues.append({"reason": "malformed_jsonl_lines", "count": bad_lines})
    if not events and not bad_lines:
        issues.append({"reason": "no_events_parsed"})
    return events


def parts_of(event):
    content = event.get("content")
    if not isinstance(content, dict):
        return []
    parts = content.get("parts")
    return parts if isinstance(parts, list) else []


def pick(part, snake, camel):
    value = part.get(snake)
    if value is None:
        value = part.get(camel)
    return value if isinstance(value, dict) else None


def serialised_size(value):
    try:
        encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    except (TypeError, ValueError):
        encoded = repr(value).encode("utf-8")
    return len(encoded), hashlib.sha256(encoded).hexdigest()[:16]


def percentile(values, fraction):
    if not values:
        return 0
    ordered = sorted(values)
    rank = max(1, math.ceil(fraction * len(ordered)))
    return ordered[rank - 1]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Prints tool names, counts and sizes only. Token counts are bytes/4 estimates.")
    parser.add_argument("--events", required=True, help="JSON or JSONL file of ADK events")
    parser.add_argument("--max-bytes", type=positive, default=20000,
                        help="flag a single serialised response above this many bytes (default: 20000)")
    args = parser.parse_args()
    path = Path(args.events)
    if path.is_symlink() or not path.is_file():
        parser.error("events must be an existing regular file, not a symlink")
    issues = []
    events = load_events(path, issues)
    per_tool = {}
    skipped_events = 0
    flags = []
    status_values = {}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            skipped_events += 1
            continue
        for part in parts_of(event):
            if not isinstance(part, dict):
                skipped_events += 1
                continue
            call = pick(part, "function_call", "functionCall")
            if call is not None:
                name = str(call.get("name") or "<unnamed>")
                row = per_tool.setdefault(name, {"calls": 0, "responses": 0, "response_bytes": [],
                                                 "args_bytes": [], "hashes": {}})
                row["calls"] += 1
                row["args_bytes"].append(serialised_size(call.get("args", {}))[0])
            response = pick(part, "function_response", "functionResponse")
            if response is not None:
                name = str(response.get("name") or "<unnamed>")
                row = per_tool.setdefault(name, {"calls": 0, "responses": 0, "response_bytes": [],
                                                 "args_bytes": [], "hashes": {}})
                payload = response.get("response")
                size, digest = serialised_size(payload)
                row["responses"] += 1
                row["response_bytes"].append(size)
                row["hashes"][digest] = row["hashes"].get(digest, 0) + 1
                if isinstance(payload, dict):
                    status = payload.get("status")
                    if isinstance(status, str):
                        status_values.setdefault(name, {})
                        status_values[name][status] = status_values[name].get(status, 0) + 1
                if size > args.max_bytes:
                    flags.append({"tool": name, "event_index": index, "bytes": size,
                                  "flag": "response_exceeds_max_bytes"})
    tools = []
    total_bytes = 0
    for name in sorted(per_tool):
        row = per_tool[name]
        sizes = row["response_bytes"]
        total = sum(sizes)
        total_bytes += total
        repeated = sum(count - 1 for count in row["hashes"].values() if count > 1)
        if repeated:
            flags.append({"tool": name, "flag": "repeated_identical_response", "occurrences": repeated})
        tools.append({"tool": name, "calls": row["calls"], "responses": len(sizes),
                      "response_bytes_total": total,
                      "response_bytes_max": max(sizes) if sizes else 0,
                      "response_bytes_p95": percentile(sizes, 0.95),
                      "response_bytes_mean": round(total / len(sizes)) if sizes else 0,
                      "approx_tokens_total": total // 4,
                      "approx_tokens_max": (max(sizes) // 4) if sizes else 0,
                      "args_bytes_total": sum(row["args_bytes"]),
                      "repeated_identical_responses": repeated,
                      "over_max_bytes": sum(1 for s in sizes if s > args.max_bytes),
                      "status_values": dict(sorted(status_values.get(name, {}).items()))})
    flags.sort(key=lambda item: json.dumps(item, sort_keys=True))
    issues.sort(key=lambda item: json.dumps(item, sort_keys=True))
    partial = bool(issues) or skipped_events > 0
    report = {"schema_version": 1, "read_only": True, "partial": partial,
              "events_seen": len(events), "events_skipped": skipped_events,
              "max_bytes": args.max_bytes, "token_estimate": "bytes_divided_by_4",
              "response_bytes_total": total_bytes, "approx_tokens_total": total_bytes // 4,
              "tools": tools, "flags": flags, "issues": issues}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if partial else 0


if __name__ == "__main__":
    raise SystemExit(main())
