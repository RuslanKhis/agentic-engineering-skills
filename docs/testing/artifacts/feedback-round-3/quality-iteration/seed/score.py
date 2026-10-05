#!/usr/bin/env python3
"""Evaluator-side scorer for the quality-iteration trial seed. Standard library only.

Compares outputs/<case>.json with each case's label and prints one row per
case: decision match, recall of the label's policy IDs among the output's
cited policy IDs, condition count, and whether the output passed schema
validation. It reports observations only; it does not categorise defects or
suggest fixes. Run from this directory: ``python3 score.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def score_case(case: dict, record: dict) -> dict:
    label = case["label"]
    wanted = {pid for reason in label["reasons"] for pid in reason["policy_ids"]}
    if not record.get("schema_valid"):
        return {"case": case["id"], "decision_match": False, "policy_recall": 0.0,
                "cited": [], "conditions": 0, "schema_valid": False}
    out = record["output"]
    cited = {pid for reason in out.get("reasons", []) for pid in reason.get("policy_ids", [])}
    recall = len(wanted & cited) / len(wanted) if wanted else 1.0
    return {"case": case["id"], "decision_match": out.get("decision") == label["decision"],
            "policy_recall": round(recall, 2), "cited": sorted(cited),
            "conditions": len(out.get("conditions", [])), "schema_valid": True}


def main() -> None:
    rows = []
    for path in sorted((HERE / "cases").glob("dev-*.json")):
        case = json.loads(path.read_text())
        out_path = HERE / "outputs" / f"{case['id']}.json"
        record = json.loads(out_path.read_text()) if out_path.exists() else {"schema_valid": False}
        rows.append(score_case(case, record))
    print(f"{'case':8} {'decision':9} {'recall':7} {'conds':6} {'schema':7} cited")
    for r in rows:
        print(f"{r['case']:8} {str(r['decision_match']):9} {r['policy_recall']:<7} {r['conditions']:<6} "
              f"{str(r['schema_valid']):7} {','.join(r['cited'])}")
    matched = sum(r["decision_match"] for r in rows)
    mean_recall = sum(r["policy_recall"] for r in rows) / len(rows)
    print(f"\ndecisions matched {matched}/{len(rows)}; mean policy recall {mean_recall:.2f}; "
          f"schema failures {sum(not r['schema_valid'] for r in rows)}")


if __name__ == "__main__":
    main()
