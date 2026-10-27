"""Price a saved ADK session export.

Each model response event carries usage_metadata. Input is prompt tokens;
output is candidates plus thoughts tokens. Cost uses the per-million prices in
prices.json for the event's model.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_prices(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))["models"]


def session_usage(session: dict) -> dict:
    totals: dict[str, dict[str, int]] = {}
    for event in session.get("events", []):
        usage = event.get("usage_metadata")
        if not usage:
            continue
        model = event.get("model_version", "unknown")
        row = totals.setdefault(model, {"input": 0, "output": 0})
        row["input"] += usage.get("prompt_token_count", 0)
        row["output"] += usage.get("candidates_token_count", 0) + usage.get("thoughts_token_count", 0)
    return totals


def session_cost(session: dict, prices: dict) -> float:
    cost = 0.0
    for model, row in session_usage(session).items():
        price = prices.get(model)
        if price is None:
            continue
        cost += row["input"] / 1e6 * price["input_per_million"]
        cost += row["output"] / 1e6 * price["output_per_million"]
    return round(cost, 6)


def report(session_dir: str | Path, prices_path: str | Path) -> list[dict]:
    prices = load_prices(prices_path)
    rows = []
    for path in sorted(Path(session_dir).glob("*.json")):
        session = json.loads(path.read_text(encoding="utf-8"))
        rows.append({"session": session["id"], "cost_usd": session_cost(session, prices),
                     "usage": session_usage(session)})
    return rows


if __name__ == "__main__":
    for row in report("sessions", "prices.json"):
        print(json.dumps(row))
