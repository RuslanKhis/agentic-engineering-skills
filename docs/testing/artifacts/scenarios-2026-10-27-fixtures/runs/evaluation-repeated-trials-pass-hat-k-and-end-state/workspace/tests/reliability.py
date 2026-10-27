"""Reliability figure for the nightly gate: unbiased pass^k over repeated trials per case.

Input is one JSON object per trial (JSONL), written by the runner, with at least `case_id`,
`trial_id`, `outcome` ("pass" | "fail" | "infra_error"). Standard library only.

    python -m tests.reliability trials.jsonl --cases cases.txt --k 3 --threshold 0.85

Exit 0 pass, 1 fail, 3 not run (missing/short evidence). CI must treat 1 and 3 as red.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict

SCORED = ("pass", "fail")
KNOWN = SCORED + ("infra_error",)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """Unbiased P(all k trials pass) from c passes in n: C(c,k)/C(n,k). Refuses k > n."""
    if k < 1:
        raise ValueError("k must be >= 1")
    if n < k:
        raise ValueError(f"{n} scored trials is fewer than k={k}")
    return math.comb(c, k) / math.comb(n, k)


def per_case(records: list[dict], k: int) -> dict[str, dict]:
    rows = defaultdict(list)
    for r in records:
        rows[r["case_id"]].append(r)
    out = {}
    for case_id, trials in rows.items():
        scored = [t for t in trials if t["outcome"] in SCORED]
        passes = sum(t["outcome"] == "pass" for t in scored)
        out[case_id] = {
            "scored": len(scored), "passes": passes,
            "infra_error": sum(t["outcome"] == "infra_error" for t in trials),
            # infra errors stay out of the denominator but are reported
            "score": pass_hat_k(len(scored), passes, k) if len(scored) >= k else math.nan,
        }
    return out


def scenario_of(case_id: str) -> str:
    """'booking-14-cancel' -> 'cancel': variants of one scenario share the intent suffix."""
    return case_id.split("-", 2)[2]


def evaluate(records: list[dict], expected_cases: list[str], k: int, threshold: float) -> dict:
    problems = []
    bad = sorted({str(r.get("outcome")) for r in records} - set(KNOWN))
    if bad:
        problems.append(f"unknown outcome values: {bad}")
    if not records:
        problems.append("no trial records")
    seen = {r["case_id"] for r in records}
    if missing := sorted(set(expected_cases) - seen):
        problems.append(f"{len(missing)} expected cases have no trials: {missing[:5]}")
    if extra := sorted(seen - set(expected_cases)):
        problems.append(f"trial records for unexpected cases: {extra[:5]}")
    cases = per_case([r for r in records if r["case_id"] in expected_cases], k)
    short = sorted(c for c, v in cases.items() if math.isnan(v["score"]))
    if short:
        problems.append(f"{len(short)} cases have fewer than k={k} scored trials: {short[:5]}")
    result = {"k": k, "threshold": threshold, "cases": len(expected_cases), "problems": problems,
              "infra_errors": sum(v["infra_error"] for v in cases.values())}
    if problems:
        return {**result, "verdict": "NOT RUN", "pass_hat_k": None}
    value = sum(v["score"] for v in cases.values()) / len(expected_cases)
    by_scenario = defaultdict(list)
    for c, v in cases.items():
        by_scenario[scenario_of(c)].append(v)
    result.update(
        pass_hat_k=value,
        # diagnostic, not the gate: a scenario passes only when every variant passed every trial
        scenario_all_pass={s: all(v["passes"] == v["scored"] for v in vs) for s, vs in by_scenario.items()},
        scenario_pass_hat_k={s: sum(v["score"] for v in vs) / len(vs) for s, vs in by_scenario.items()},
        verdict="PASS" if value >= threshold else "FAIL")
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("trials")
    p.add_argument("--cases", required=True, help="file with one expected case_id per line")
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--threshold", type=float, required=True)
    a = p.parse_args(argv)
    try:
        with open(a.trials) as f:
            records = [json.loads(line) for line in f if line.strip()]
        with open(a.cases) as f:
            expected = [line.strip() for line in f if line.strip()]
        result = evaluate(records, expected, a.k, a.threshold)
    except (OSError, ValueError, KeyError) as exc:  # a missing file or bad row is NOT RUN, never a pass
        print(json.dumps({"verdict": "NOT RUN", "problems": [f"{type(exc).__name__}: {exc}"]}))
        return 3
    print(json.dumps(result, indent=1))
    return {"PASS": 0, "FAIL": 1, "NOT RUN": 3}[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
