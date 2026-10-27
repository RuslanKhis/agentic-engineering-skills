"""Shopping tools: each shows its result in the app as a widget."""
from __future__ import annotations

import json
from pathlib import Path

from app import widgets

CATALOGUE = Path(__file__).resolve().parents[2] / "help" / "products.json"


def _products() -> list[dict]:
    return json.loads(CATALOGUE.read_text(encoding="utf-8"))


def search_products(query: str, tool_context) -> dict:
    """Find products matching the query and show them as cards.

    Args:
        query: Keywords, e.g. "waterproof jacket".

    Returns:
        {"status": "ok", "skus": [...], "count": n}.
    """
    terms = [t for t in query.lower().split() if t]
    hits = [p for p in _products()
            if all(t in (p["name"] + " " + " ".join(p["tags"])).lower() for t in terms)][:6]
    tool_context.state["last_search"] = {"query": query, "skus": [p["sku"] for p in hits]}
    currency = tool_context.state.get("user:currency", "GBP")
    tool_context.render_ui_widget(widgets.to_ui_widget(widgets.CARDS_ID, widgets.product_cards(hits, currency)))
    return {"status": "ok", "skus": [p["sku"] for p in hits], "count": len(hits)}


def recommend_products(activity: str, tool_context) -> dict:
    """Recommend up to three products for an activity and show them as cards.

    Args:
        activity: e.g. "hiking", "running", "winter".

    Returns:
        {"status": "ok", "skus": [...]}.
    """
    picks = sorted((p for p in _products() if activity.lower() in p["tags"]),
                   key=lambda p: -p["rating"])[:3]
    currency = tool_context.state.get("user:currency", "GBP")
    tool_context.render_ui_widget(widgets.to_ui_widget(widgets.CARDS_ID, widgets.product_cards(picks, currency)))
    return {"status": "ok", "skus": [p["sku"] for p in picks]}


def compare_products(skus: list[str], tool_context) -> dict:
    """Compare two to four products side by side and show the table.

    Args:
        skus: Product SKUs, e.g. ["JK-210", "JK-340"].

    Returns:
        {"status": "ok", "skus": [...]} or {"status": "error", "message": ...}.
    """
    if not 2 <= len(skus) <= 4:
        return {"status": "error", "message": "Compare between two and four products."}
    by_sku = {p["sku"]: p for p in _products()}
    missing = [s for s in skus if s not in by_sku]
    if missing:
        return {"status": "error", "message": f"Unknown products: {', '.join(missing)}"}
    columns = ["name", "price_cents", "weight_g", "waterproof_mm", "rating"]
    rows = [{"sku": s, **{c: by_sku[s].get(c) for c in columns}} for s in skus]
    tool_context.render_ui_widget(widgets.to_ui_widget(widgets.TABLE_ID, widgets.comparison_table(columns, rows)))
    return {"status": "ok", "skus": skus}
