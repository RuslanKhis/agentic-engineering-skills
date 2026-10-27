"""Shopping tools: each stages its widget; the after-agent callback emits it."""
from __future__ import annotations

from app import staging

_products = staging.load_products


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
    staging.stage_cards(tool_context.state, [p["sku"] for p in hits], currency)
    return {"status": "ok", "skus": [p["sku"] for p in hits], "count": len(hits)}


def show_last_results(tool_context) -> dict:
    """Show the cards from the most recent search again, without searching.

    Use when the customer asks to see the previous results again.

    Returns:
        {"status": "ok", "skus": [...]} or {"status": "error", "message": ...}.
    """
    last = tool_context.state.get("last_search")
    if not last:
        return {"status": "error", "message": "There is no earlier search to show."}
    currency = tool_context.state.get("user:currency", "GBP")
    staging.stage_cards(tool_context.state, last["skus"], currency)
    return {"status": "ok", "skus": last["skus"]}


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
    staging.stage_cards(tool_context.state, [p["sku"] for p in picks], currency)
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
    staging.stage_table(tool_context.state, columns, rows)
    return {"status": "ok", "skus": skus}
