"""Score saved recall outputs against the memory gold set (offline, no model calls).

A case passes when every expected phrase appears in the recalled memories and
no forbidden phrase does. Prints per-ability pass counts.
usage: python eval/score_recall.py GOLD.jsonl OUTPUTS.jsonl
"""
from __future__ import annotations

from collections import Counter
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def score(gold, outputs):
    by_id = {o["id"]: " ".join(o["recalled"]).lower() for o in outputs}
    results = []
    for case in gold:
        text = by_id.get(case["id"], "")
        ok = all(e.lower() in text for e in case["expected"]) and not any(
            f.lower() in text for f in case["forbidden"])
        results.append({"id": case["id"], "ability": case["ability"], "pass": ok})
    return results


def main(argv):
    results = score(load(argv[1]), load(argv[2]))
    passed, total = Counter(), Counter()
    for r in results:
        total[r["ability"]] += 1
        passed[r["ability"]] += r["pass"]
    for ability in sorted(total):
        print(f"{ability}: {passed[ability]}/{total[ability]}")
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
