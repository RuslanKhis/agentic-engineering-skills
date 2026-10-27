"""Staged widget emission.

Tools stage a small JSON spec per widget id in session state; the single
after_agent_callback (`emit_staged_widgets`) is the only caller of
`render_ui_widget`. A spec is staged under its widget id, so two tools that
stage the same id in one turn ship one widget (the last one wins). The
per-widget `emitted` flag is the dedupe record and also the state change that
makes ADK produce an event for the callback.
"""
from __future__ import annotations

import json
from pathlib import Path

from app import widgets

STATE_KEY = "staged_widgets"
CATALOGUE = Path(__file__).resolve().parents[1] / "help" / "products.json"
ORDER = [widgets.CARDS_ID, widgets.TABLE_ID]


def load_products() -> list[dict]:
    return json.loads(CATALOGUE.read_text(encoding="utf-8"))


def _put(state, widget_id: str, spec: dict) -> None:
    staged = dict(state.get(STATE_KEY) or {})
    staged[widget_id] = {**spec, "emitted": False}
    state[STATE_KEY] = staged  # reassign so the state delta is recorded


def stage_cards(state, skus: list[str], currency: str) -> None:
    _put(state, widgets.CARDS_ID, {"kind": "cards", "skus": list(skus), "currency": currency})


def stage_table(state, columns: list[str], rows: list[dict]) -> None:
    _put(state, widgets.TABLE_ID, {"kind": "table", "columns": list(columns), "rows": rows})


def restage_cards_for_currency(state, currency: str) -> None:
    """Re-render the cards on screen in a new currency; no-op if already in it."""
    record = (state.get(STATE_KEY) or {}).get(widgets.CARDS_ID)
    if record and record.get("currency") != currency:
        stage_cards(state, record["skus"], currency)


def _payload(spec: dict) -> dict:
    if spec["kind"] == "table":
        return widgets.comparison_table(spec["columns"], spec["rows"])
    by_sku = {p["sku"]: p for p in load_products()}
    products = [by_sku[s] for s in spec["skus"] if s in by_sku]
    return widgets.product_cards(products, spec["currency"])


def emit_staged_widgets(callback_context):
    """after_agent_callback: render every unemitted staged widget once, in ORDER."""
    staged = dict(callback_context.state.get(STATE_KEY) or {})
    pending = [i for i in ORDER + sorted(set(staged) - set(ORDER))
               if i in staged and not staged[i].get("emitted")]
    for widget_id in pending:
        callback_context.render_ui_widget(widgets.to_ui_widget(widget_id, _payload(staged[widget_id])))
        staged[widget_id] = {**staged[widget_id], "emitted": True}
    if pending:
        callback_context.state[STATE_KEY] = staged
    return None
