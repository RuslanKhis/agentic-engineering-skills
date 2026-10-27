"""Draft launch gate: execution accuracy over the eval cases.

Runs each question through the agent, executes the returned SQL and compares the result with the
gold rows as sets. Launch passes when execution accuracy is at least GATE_EX.
"""
from __future__ import annotations

import json
from pathlib import Path

GATE_EX = 0.85
CASES = Path(__file__).with_name("cases.json")


def execution_match(predicted_rows: list[dict], gold_rows: list[dict]) -> bool:
    pred = {tuple(sorted(r.items())) for r in predicted_rows}
    gold = {tuple(sorted(r.items())) for r in gold_rows}
    return pred == gold


def execution_accuracy(results: dict[str, list[dict]]) -> float:
    cases = json.loads(CASES.read_text())
    hits = sum(execution_match(results.get(c["id"], []), c["expected_rows"]) for c in cases)
    return hits / len(cases)


def gate(results: dict[str, list[dict]]) -> bool:
    return execution_accuracy(results) >= GATE_EX
