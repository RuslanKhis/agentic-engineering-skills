"""Public-response oracle: checks what the account manager would read, not the SQL.

A case passes only when the agent's rows have the exact expected values, the expected number of
rows and, for ranked questions, the expected order.
"""
from __future__ import annotations


def _norm(value):
    if isinstance(value, float):
        return round(value, 2)
    return value


def check(case: dict, rows: list[dict]) -> dict:
    expected = case["expected_rows"]
    columns = case["columns"]
    got = [tuple(_norm(r.get(c)) for c in columns) for r in rows]
    want = [tuple(_norm(r[c]) for c in columns) for r in expected]
    problems = []
    if len(got) != len(want):
        problems.append(f"cardinality {len(got)} != {len(want)}")
    if case.get("ordered"):
        if got != want:
            problems.append("values or ranking order differ")
    elif sorted(got) != sorted(want):
        problems.append("values differ")
    return {"case": case["id"], "passed": not problems, "problems": problems}
