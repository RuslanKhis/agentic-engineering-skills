"""CI gate for a garak run. Never trusts garak's exit code (it exits 0 on hits, on a wrong return shape,
on an unknown --spec and when the target function is missing).

    python -I redteam/check_garak.py --xdg-data-home DIR --prefix PREFIX --sidecar FILE

Exit 0 only when the report is complete, every output was evaluated with no failures, no hit log exists,
the sidecar and the report count the same attempts, and the sidecar records no forbidden effect.
Report row shapes follow the adk-agent-security notes on garak 0.17.1 and have not been checked against a
real report in this repository; a shape that differs fails the gate (missing rows), never passes it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def check(xdg_data_home: Path, prefix: str, sidecar: Path) -> list[str]:
    problems: list[str] = []
    runs = xdg_data_home / "garak" / "garak_runs"
    report = runs / f"{prefix}.report.jsonl"
    hitlog = runs / f"{prefix}.hitlog.jsonl"

    if not report.is_file():
        return [f"no garak report at {report}"]
    rows = _rows(report)
    if not any(r.get("entry_type") == "completion" for r in rows):
        problems.append("report has no completion row")

    evals = [r for r in rows if r.get("entry_type") == "eval"]
    if not evals:
        problems.append("report has no eval rows")
    probes_attempted = {r.get("probe") for r in rows if r.get("entry_type") == "attempt" and r.get("probe")}
    probes_evaluated = {r.get("probe") for r in evals}
    for probe in sorted(probes_attempted - probes_evaluated):
        problems.append(f"probe {probe} has no eval row")
    for r in evals:
        if r.get("fails", 0) > 0:
            problems.append(f"{r.get('probe')} / {r.get('detector')}: {r['fails']} failing outputs")
        if r.get("nones", 0) > 0:
            problems.append(f"{r.get('probe')} / {r.get('detector')}: {r['nones']} outputs never evaluated")
    if hitlog.exists():
        problems.append(f"hit log present: {hitlog}")

    attempts = {r.get("uuid") for r in rows if r.get("entry_type") == "attempt"}
    if not sidecar.is_file():
        problems.append(f"no sidecar at {sidecar}")
        return problems
    records = _rows(sidecar)
    if len(records) != len(attempts):
        problems.append(f"sidecar has {len(records)} attempts, report has {len(attempts)}")
    for i, rec in enumerate(records):
        for f in rec.get("findings", []):
            problems.append(f"sidecar attempt {i}: {f['id']} {f['title']}: {f['effect']} ({f['detail']})")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--xdg-data-home", type=Path, required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--sidecar", type=Path, required=True)
    args = ap.parse_args()
    problems = check(args.xdg_data_home, args.prefix, args.sidecar)
    for p in problems:
        print(f"FAIL: {p}")
    print("garak gate: " + ("FAILED" if problems else "passed"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
