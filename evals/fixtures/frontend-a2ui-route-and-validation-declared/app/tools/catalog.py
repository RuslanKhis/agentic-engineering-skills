"""Product search and comparison over the local catalogue file."""
from __future__ import annotations

import json
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parents[2] / "help" / "products.json"


def _products() -> list[dict]:
    return json.loads(CATALOGUE.read_text(encoding="utf-8"))


def search_products(query: str, max_price_cents: int = 0) -> dict:
    """Find products whose name or tags match the query.

    Args:
        query: Keywords, e.g. "waterproof jacket".
        max_price_cents: Upper price limit in cents; 0 means no limit.

    Returns:
        {"status": "ok", "products": [{"sku", "name", "price_cents", "image_url", "rating"}]} (at most 6).
    """
    terms = [t for t in query.lower().split() if t]
    hits = []
    for p in _products():
        text = (p["name"] + " " + " ".join(p["tags"])).lower()
        if all(t in text for t in terms) and (not max_price_cents or p["price_cents"] <= max_price_cents):
            hits.append({k: p[k] for k in ("sku", "name", "price_cents", "image_url", "rating")})
    return {"status": "ok", "products": hits[:6]}


def compare_products(skus: list[str]) -> dict:
    """Compare two to four products side by side.

    Args:
        skus: Product SKUs from search_products, e.g. ["JK-210", "JK-340"].

    Returns:
        {"status": "ok", "columns": [...], "rows": [{"sku", "name", ...attributes}]} or
        {"status": "error", "message": ...}.
    """
    if not 2 <= len(skus) <= 4:
        return {"status": "error", "message": "Compare between two and four products."}
    by_sku = {p["sku"]: p for p in _products()}
    missing = [s for s in skus if s not in by_sku]
    if missing:
        return {"status": "error", "message": f"Unknown products: {', '.join(missing)}"}
    columns = ["name", "price_cents", "weight_g", "waterproof_mm", "rating"]
    return {"status": "ok", "columns": columns,
            "rows": [{"sku": s, **{c: by_sku[s].get(c) for c in columns}} for s in skus]}
