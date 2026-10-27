"""Agent callbacks."""
from __future__ import annotations

import json
from pathlib import Path

from app import widgets

CATALOGUE = Path(__file__).resolve().parents[1] / "help" / "products.json"


def refresh_cards_after_preference_change(callback_context):
    """When the customer changed their currency this turn, re-render the last cards in it."""
    state = callback_context.state
    currency = state.get("user:currency", "GBP")
    if state.get("cards_currency") == currency:
        return None
    last = state.get("last_search") or {}
    by_sku = {p["sku"]: p for p in json.loads(CATALOGUE.read_text(encoding="utf-8"))}
    products = [by_sku[s] for s in last.get("skus", []) if s in by_sku]
    if products:
        callback_context.render_ui_widget(
            widgets.to_ui_widget(widgets.CARDS_ID, widgets.product_cards(products, currency)))
    return None
