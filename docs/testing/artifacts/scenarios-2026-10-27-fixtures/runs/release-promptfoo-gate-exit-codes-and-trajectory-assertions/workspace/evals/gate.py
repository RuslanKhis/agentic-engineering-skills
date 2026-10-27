"""Reads Promptfoo's results JSON and the `promptfoo eval` exit code; prints one verdict.

Exit codes of this script (the nightly job maps them, never `promptfoo eval`'s own code):
  0 PASS         every expected row present, no error rows, every assertion passed, baseline measured
  1 BLOCK        at least one assertion failed (or promptfoo exited 100)
  2 NOT RUN      the evidence cannot be trusted: no/garbled file, wrong row count, error rows,
                 missing assertion types, promptfoo exit code other than 0 or 100
  3 PROVISIONAL  everything passed but the thresholds are not yet measured (see expectations)
NOT RUN outranks BLOCK: with error rows the counts are not a measurement.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PASS, BLOCK, NOT_RUN, PROVISIONAL = 0, 1, 2, 3
PROMPTFOO_FAILED_TESTS = 100


def _rows(doc: dict) -> list[dict] | None:
    results = doc.get("results") if isinstance(doc, dict) else None
    rows = results.get("results") if isinstance(results, dict) else None
    return rows if isinstance(rows, list) else None


def _case(row: dict) -> str:
    test = row.get("testCase") or {}
    return str(test.get("description") or row.get("description") or "")


def _types(row: dict) -> set[str]:
    comps = (row.get("gradingResult") or {}).get("componentResults") or []
    out = set()
    for comp in comps:
        kind = (comp.get("assertion") or {}).get("type")
        if kind:
            out.add(kind[4:] if kind.startswith("not-") else kind)
    return out


def evaluate(doc: dict, expectations: dict, exit_code: int) -> tuple[int, list[str]]:
    not_run: list[str] = []
    blocks: list[str] = []

    if exit_code not in (0, PROMPTFOO_FAILED_TESTS):
        not_run.append(f"promptfoo exited {exit_code} (harness error)")
    rows = _rows(doc)
    if rows is None:
        not_run.append("results JSON has no results.results list")
        return NOT_RUN, not_run

    repeat = expectations["repeat"]
    cases = expectations["cases"]
    want_rows = len(cases) * repeat
    if not cases or want_rows == 0:
        not_run.append("expectations list no cases")
    if len(rows) != want_rows:
        not_run.append(f"expected {want_rows} rows ({len(cases)} cases x repeat {repeat}), found {len(rows)}")

    per_case = Counter(_case(r) for r in rows)
    for name, spec in cases.items():
        if per_case.get(name, 0) != repeat:
            not_run.append(f"case {name!r}: {per_case.get(name, 0)} rows, expected {repeat}")
    for name in per_case:
        if name not in cases:
            not_run.append(f"case {name!r} is not in the expectations file")

    for row in rows:
        name = _case(row)
        if row.get("error") or row.get("failureReason") == 2:
            not_run.append(f"case {name!r}: error row: {str(row.get('error'))[:120]}")
            continue
        need = set(cases.get(name, {}).get("required_assertions", []))
        missing = need - _types(row)
        if missing:
            not_run.append(f"case {name!r}: assertion types not graded: {sorted(missing)}")
        if not row.get("success"):
            blocks.append(f"case {name!r}: {(row.get('gradingResult') or {}).get('reason', 'failed')[:160]}")

    if exit_code == PROMPTFOO_FAILED_TESTS and not blocks and not not_run:
        blocks.append("promptfoo exited 100 but no failing row is visible in the JSON")
    if exit_code == 0 and blocks:
        blocks.append("promptfoo exited 0 although rows failed (PROMPTFOO_PASS_RATE_THRESHOLD below 100?)")

    if not_run:
        return NOT_RUN, [f"NOT RUN: {m}" for m in not_run] + [f"BLOCK: {m}" for m in blocks]
    if blocks:
        return BLOCK, [f"BLOCK: {m}" for m in blocks]
    if not expectations.get("baseline_measured_on"):
        return PROVISIONAL, ["PROVISIONAL: all rows passed but no baseline campaign has set the thresholds"]
    return PASS, [f"PASS: {len(rows)} rows, baseline measured {expectations['baseline_measured_on']}"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", required=True, type=Path)
    ap.add_argument("--expectations", required=True, type=Path)
    ap.add_argument("--promptfoo-exit", required=True, type=int)
    args = ap.parse_args(argv)
    try:
        expectations = json.loads(args.expectations.read_text())
        doc = json.loads(args.results.read_text())
    except (OSError, ValueError) as exc:
        print(f"NOT RUN: cannot read inputs: {exc}")
        return NOT_RUN
    code, lines = evaluate(doc, expectations, args.promptfoo_exit)
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
