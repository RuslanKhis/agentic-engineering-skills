"""Compare span attribute keys seen in an export with what dashboards query and what the GenAI conventions define.

Pure stdlib; reads files only. Input is a JSON list of spans, each ``{"name": str, "attributes": {key: value}}``
(export a day of spans from the vendor backend, or from an in-memory exporter in a test).
"""
from __future__ import annotations

import json
import re
import sys

# Keys the conventions removed; dashboards must not depend on them.
REMOVED_KEYS = {"gen_ai.system": "gen_ai.provider.name"}
_DASHBOARD_KEY = re.compile(r"\b(?:gen_ai|gcp\.vertex\.agent)\.[a-z0-9_.]+")


def dashboard_keys(dashboard: dict) -> dict[str, set[str]]:
    return {p["title"]: set(_DASHBOARD_KEY.findall(p["query"])) for p in dashboard.get("panels", [])}


def check(dashboard: dict, spans: list[dict]) -> list[str]:
    """Return human-readable warnings; an empty list means no drift detected."""
    seen: dict[str, int] = {}
    for span in spans:
        for key in span.get("attributes", {}):
            seen[key] = seen.get(key, 0) + 1
    warnings = []
    for title, keys in dashboard_keys(dashboard).items():
        for key in sorted(keys):
            if key in REMOVED_KEYS:
                warnings.append(f"panel '{title}': {key} was removed from the conventions; use {REMOVED_KEYS[key]}")
            if seen and key not in seen:
                warnings.append(f"panel '{title}': {key} not present on any exported span")
    return warnings


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: semconv_drift.py DASHBOARD.json SPANS.json", file=sys.stderr)
        return 2
    with open(argv[1]) as f:
        dashboard = json.load(f)
    with open(argv[2]) as f:
        spans = json.load(f)
    warnings = check(dashboard, spans)
    for w in warnings:
        print("WARN", w)
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
