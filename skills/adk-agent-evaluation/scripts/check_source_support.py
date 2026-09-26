#!/usr/bin/env python3
"""Score authored source-support judgments; no semantic inference or model calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ASSETS = Path(__file__).resolve().parents[1] / "assets"
LABELS = {
    "source_identity": {"valid", "invalid"},
    "span_completeness": {"complete", "incomplete", "unresolved"},
    "applicability": {"applicable", "not_applicable", "unresolved"},
    "contrary_evidence": {"none", "contradiction", "unresolved"},
    "support": {"supported", "unsupported", "contradicted", "unresolved"},
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def index_judgments(data: dict, expected_ids: set[str]) -> dict:
    """Require complete, unambiguous coverage before computing agreement."""
    if not isinstance(data, dict) or not isinstance(data.get("judgments"), list):
        raise ValueError("expected a judgments list")
    indexed = {}
    for row in data["judgments"]:
        if not isinstance(row, dict):
            raise ValueError("judgment must be an object")
        cid = row.get("case_id")
        if not isinstance(cid, str) or cid not in expected_ids or cid in indexed:
            raise ValueError("unknown or duplicate case identity")
        for dimension, allowed in LABELS.items():
            value = row.get(dimension)
            if not isinstance(value, str) or value not in allowed:
                raise ValueError("missing or invalid dimension label")
        if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
            raise ValueError("a brief rationale is required")
        indexed[cid] = row
    if set(indexed) != expected_ids:
        raise ValueError("missing case judgments")
    return indexed


def score(expected: dict, candidate: dict) -> dict:
    """Agreement with authored expectations, not independent proof of truth."""
    ids = set(expected)
    if set(candidate) != ids:
        raise ValueError("candidate coverage differs from expectations")
    mismatches = {
        field: sorted(cid for cid in ids if expected[cid][field] != candidate[cid][field])
        for field in LABELS
    }
    incorrect = set().union(*map(set, mismatches.values()))
    return {
        "case_count": len(ids),
        "exact_matches": len(ids) - len(incorrect),
        "false_accepts": sorted(cid for cid in ids
                                if candidate[cid]["support"] == "supported"
                                and expected[cid]["support"] != "supported"),
        "false_rejects": sorted(cid for cid in ids
                                if candidate[cid]["support"] != "supported"
                                and expected[cid]["support"] == "supported"),
        "mismatches_by_dimension": mismatches,
    }


def weak_judgments(fixture: dict, mode: str) -> dict:
    """Deliberately inadequate controls; never use these as a support judge."""
    rows = []
    for case in fixture["cases"]:
        selections = case["selected_evidence"]
        source_ids_valid = all(item["source_id"] in fixture["sources"] for item in selections)
        quotations_valid = source_ids_valid and all(
            item["quote"] in fixture["sources"][item["source_id"]]["text"]
            for item in selections
        )
        if mode == "id_only":
            accepted = source_ids_valid
        elif mode == "literal_substring":
            accepted = quotations_valid and any(
                case["observation"] in item["quote"] for item in selections
            )
        elif mode == "reject_all":
            accepted = False
        else:
            raise ValueError("unknown control")
        rows.append({
            "case_id": case["case_id"],
            "source_identity": "valid" if quotations_valid else "invalid",
            "span_completeness": "complete",
            "applicability": "applicable",
            "contrary_evidence": "none",
            "support": "supported" if accepted else "unsupported",
            "rationale": "Intentionally weak control: " + mode,
        })
    return {"judgments": rows}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="run offline negative controls")
    mode.add_argument("--judgments", type=Path, help="judge output JSON, without expected labels")
    args = parser.parse_args(argv)
    try:
        fixture = read_json(ASSETS / "source-support-cases.json")
        ids = {case["case_id"] for case in fixture["cases"]}
        if not ids or len(ids) != len(fixture["cases"]):
            raise ValueError("empty fixture or duplicate case identities")
        expected_file = read_json(ASSETS / "source-support-expectations.json")
        expected = index_judgments(expected_file, ids)
        if args.demo:
            results = {"label_replay_scorer_self_check": score(expected, expected)}
            for control in ("id_only", "literal_substring", "reject_all"):
                candidate = index_judgments(weak_judgments(fixture, control), ids)
                results[control] = score(expected, candidate)
            print(json.dumps({"review_status": expected_file["review_status"],
                              "results": results}, indent=2))
            exposed = (results["id_only"]["false_accepts"]
                       and results["literal_substring"]["false_accepts"]
                       and results["literal_substring"]["false_rejects"]
                       and results["reject_all"]["false_rejects"])
            return 0 if exposed else 1
        candidate = index_judgments(read_json(args.judgments), ids)
        result = score(expected, candidate)
        print(json.dumps({"review_status": expected_file["review_status"],
                          "result": result}, indent=2))
        return 0 if result["exact_matches"] == len(ids) else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # Source material and arbitrary file paths are deliberately not echoed.
        print("Invalid calibration input: " + type(exc).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
