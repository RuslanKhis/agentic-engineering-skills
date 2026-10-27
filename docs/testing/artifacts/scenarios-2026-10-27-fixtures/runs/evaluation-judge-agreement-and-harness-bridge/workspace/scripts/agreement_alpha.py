#!/usr/bin/env python3
"""Krippendorff's alpha (nominal, ordinal, interval) for the judge/human rating CSVs. Standard library only.

    python3 scripts/agreement_alpha.py --selftest
    python3 scripts/agreement_alpha.py labels/human-ratings.csv judges/scores-judge-a.csv judges/scores-judge-b.csv

Each CSV has trace_id and a rating column (rating or score). Names are the file stems.
A trace rated by fewer than two sources in a comparison is dropped and counted.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import random
import sys
from collections import Counter
from pathlib import Path


def alpha(units, level="ordinal"):
    """units: list of lists of ratings (None already removed)."""
    units = [u for u in units if len(u) >= 2]
    coinc = Counter()
    for u in units:
        m = len(u)
        for a, b in itertools.permutations(range(m), 2):
            coinc[(u[a], u[b])] += 1 / (m - 1)
    vals = sorted({v for u in units for v in u})
    n_c = {c: sum(coinc[(c, k)] for k in vals) for c in vals}
    n = sum(n_c.values())
    if n <= 1:
        return None

    def dist(c, k):
        if c == k:
            return 0.0
        if level == "nominal":
            return 1.0
        if level == "interval":
            return float(c - k) ** 2
        lo, hi = sorted((c, k))
        s = sum(n_c[g] for g in vals if lo <= g <= hi) - (n_c[c] + n_c[k]) / 2
        return s * s

    d_o = sum(coinc[(c, k)] * dist(c, k) for c in vals for k in vals) / n
    d_e = sum(n_c[c] * n_c[k] * dist(c, k) for c in vals for k in vals) / (n * (n - 1))
    return None if d_e == 0 else 1 - d_o / d_e


def selftest():
    # Krippendorff (2011) worked example: 4 observers, 12 units; nominal .743, ordinal .815, interval .849.
    rows = {
        "A": [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
        "B": [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
        "C": [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
        "D": [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None],
    }
    units = [[r[i] for r in rows.values() if r[i] is not None] for i in range(12)]
    want = {"nominal": 0.743, "ordinal": 0.815, "interval": 0.849}
    ok = True
    for lv, w in want.items():
        got = alpha(units, lv)
        print(f"selftest {lv}: {got:.3f} (published {w})")
        ok &= abs(got - w) < 0.0015
    return ok


def load(path):
    out, dups = {}, 0
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            col = "rating" if "rating" in r else "score"
            v = (r.get(col) or "").strip()
            if not v:
                continue
            if r["trace_id"] in out:
                dups += 1
            out[r["trace_id"]] = int(v)
    return out, dups


def boot_ci(pairs, level, reps=2000, seed=0):
    rng = random.Random(seed)
    res = []
    for _ in range(reps):
        s = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        a = alpha([list(p) for p in s], level)
        if a is not None:
            res.append(a)
    res.sort()
    return res[int(.025 * len(res))], res[int(.975 * len(res)) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--accept-at", type=int, default=4, help="rating >= this counts as acceptable")
    a = ap.parse_args()
    if a.selftest:
        return 0 if selftest() else 1
    data = {}
    for p in a.files:
        d, dups = load(p)
        data[Path(p).stem] = d
        print(f"{Path(p).stem}: {len(d)} rated, {dups} duplicate ids")
    names = list(data)
    for x, y in itertools.combinations(names, 2):
        ids = sorted(set(data[x]) & set(data[y]))
        pairs = [(data[x][i], data[y][i]) for i in ids]
        print(f"\n== {x} vs {y}: {len(pairs)} traces in common "
              f"({len(set(data[x]) | set(data[y])) - len(pairs)} dropped)")
        exact = sum(p == q for p, q in pairs) / len(pairs)
        within1 = sum(abs(p - q) <= 1 for p, q in pairs) / len(pairs)
        bias = sum(q - p for p, q in pairs) / len(pairs)
        print(f"exact {exact:.2f}  within-1 {within1:.2f}  mean({y})-mean({x}) {bias:+.2f}")
        for lv in ("nominal", "ordinal", "interval"):
            lo, hi = boot_ci(pairs, lv)
            print(f"alpha[{lv}] {alpha([list(p) for p in pairs], lv):.3f}  95% bootstrap CI [{lo:.2f}, {hi:.2f}]")
        t = a.accept_at
        both = Counter((p >= t, q >= t) for p, q in pairs)
        print(f"accept threshold >= {t}: {x} accepts/{y} rejects {both[(True, False)]}, "
              f"{x} rejects/{y} accepts {both[(False, True)]}")
        print("confusion (rows " + x + ", cols " + y + "):")
        print("     " + " ".join(f"{c:>3}" for c in range(1, 6)))
        for r in range(1, 6):
            print(f"  {r}: " + " ".join(f"{sum(1 for p, q in pairs if p == r and q == c):>3}" for c in range(1, 6)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
