"""Offline retrieval recall on the labelled development cases. No model calls.

Usage: python -m evals.retrieval_recall
Prints, per case, the labelled policies, the retrieved ones and any missed; then the totals.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.retrieval import select_policies
from pipeline.sources import load_case, load_policies

ROOT = Path(__file__).resolve().parents[1]


def measure() -> dict:
    labels = json.loads((ROOT / "labels" / "dev-labels.json").read_text())["cases"]
    policies = load_policies()
    rows, hit, total = [], 0, 0
    for case_id, label in sorted(labels.items()):
        _, trace = select_policies(load_case(ROOT / "cases" / "dev" / case_id), policies)
        want = set(label["policies"])
        missed = sorted(want - set(trace["retrieved"]))
        hit += len(want) - len(missed)
        total += len(want)
        rows.append({"case": case_id, "labelled": sorted(want), "retrieved": trace["retrieved"], "missed": missed})
    return {"rows": rows, "recalled": hit, "labelled": total}


if __name__ == "__main__":
    result = measure()
    for row in result["rows"]:
        print(row)
    print(f"policy recall: {result['recalled']}/{result['labelled']}")
