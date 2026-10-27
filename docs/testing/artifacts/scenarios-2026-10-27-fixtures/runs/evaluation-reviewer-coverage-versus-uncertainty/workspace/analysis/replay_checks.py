"""Offline replay of pipeline/coverage_check.py on saved drafts. Read-only; no provider calls.

Usage: python -I analysis/replay_checks.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline import coverage_check as cc  # noqa: E402
from pipeline.sources import case_spans, load_case, load_policies  # noqa: E402

CASES = [("PA-2026-0177", "PA-2026-0177-r2", "rejected"), ("PA-2026-0152", "PA-2026-0152-r1", "accepted")]

for case_id, run, outcome in CASES:
    case = load_case(ROOT / "cases" / "dev" / case_id)
    draft = json.loads((ROOT / "runs" / run / "writer.json").read_text())["payload"]
    saved = json.loads((ROOT / "runs" / run / "review.json").read_text())["payload"]
    ids = {s.span_id for s in case_spans(case, load_policies())}
    cited = {c for r in draft["reasons"] for c in r["citations"]} | {c["span_id"] for c in draft["citations"]}
    print(f"== {run} ({outcome}) ==")
    print("documents in case:   ", sorted(d["doc_id"] for d in case["documents"]))
    print("documents cited:     ", sorted(cc.documents_cited(draft)))
    print("unknown span ids:    ", sorted(cited - ids))
    print("applicable policies: ", sorted(cc.applicable_policies(case)))
    print("replayed findings:   ", cc.review_findings(draft, case))
    print("saved findings:      ", saved["findings"])
    print()
