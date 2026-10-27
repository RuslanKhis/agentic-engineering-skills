"""How much do our two judges agree? Prints exact-match rate and Cohen's kappa between judge A and B."""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scores(path):
    with open(path) as f:
        return {row["trace_id"]: row["score"] for row in csv.DictReader(f)}


def cohen_kappa(a, b):
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (observed - expected) / (1 - expected)


def main():
    a = scores(ROOT / "judges" / "scores-judge-a.csv")
    b = scores(ROOT / "judges" / "scores-judge-b.csv")
    ids = sorted(a)
    pairs = [(a[i] or "0", b.get(i) or "0") for i in ids]
    xa, xb = zip(*pairs)
    print(f"exact match: {sum(x == y for x, y in pairs) / len(pairs):.2f}")
    print(f"kappa: {cohen_kappa(xa, xb):.2f}")


if __name__ == "__main__":
    main()
