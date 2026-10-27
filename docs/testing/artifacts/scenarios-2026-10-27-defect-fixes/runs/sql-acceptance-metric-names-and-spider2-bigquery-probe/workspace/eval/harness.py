"""Launch gate and the numbers reported beside it.

Two named metrics, never one called "accuracy":

- ``public_response_accuracy``: share of cases that pass ``eval.oracle.check`` (exact values,
  cardinality, ranking order). This is the launch gate.
- ``bird_style_ex``: BIRD-style execution accuracy, a set comparison of result rows (row order and
  duplicate rows are ignored). Diagnostic only: a reversed ranking or a duplicated row passes it.
  Definition read from bird-bench/mini_dev ``evaluation/evaluation_ex.py``; link, do not vendor.

Rows are the agent's public-response rows, one list per case id.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from eval.oracle import check

GATE_ACCURACY = 0.85
MIN_CASES = 30  # a gate over fewer cases is not evidence; 4 cases move 25 points per miss
CASES = Path(__file__).with_name("cases.json")


def _load_cases() -> list[dict]:
    return json.loads(CASES.read_text())


def execution_match(predicted_rows: list[dict], gold_rows: list[dict]) -> bool:
    """BIRD-style EX for one case: set equality of rows. Looser than the oracle by design."""
    pred = {tuple(sorted(r.items())) for r in predicted_rows}
    gold = {tuple(sorted(r.items())) for r in gold_rows}
    return pred == gold


def bird_style_ex(results: dict[str, list[dict]]) -> float:
    cases = _load_cases()
    return sum(execution_match(results.get(c["id"], []), c["expected_rows"]) for c in cases) / len(cases)


def public_response_accuracy(results: dict[str, list[dict]]) -> float:
    cases = _load_cases()
    return sum(check(c, results.get(c["id"], []))["passed"] for c in cases) / len(cases)


def wilson_interval(hits: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = hits / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def report(results: dict[str, list[dict]]) -> dict:
    cases = _load_cases()
    passed = sum(check(c, results.get(c["id"], []))["passed"] for c in cases)
    low, high = wilson_interval(passed, len(cases))
    return {
        "cases": len(cases),
        "public_response_accuracy": passed / len(cases),
        "public_response_95ci": (round(low, 3), round(high, 3)),
        "bird_style_ex": bird_style_ex(results),
        "failed": [c["id"] for c in cases if not check(c, results.get(c["id"], []))["passed"]],
    }


def gate(results: dict[str, list[dict]]) -> bool:
    if len(_load_cases()) < MIN_CASES:
        return False
    return public_response_accuracy(results) >= GATE_ACCURACY
