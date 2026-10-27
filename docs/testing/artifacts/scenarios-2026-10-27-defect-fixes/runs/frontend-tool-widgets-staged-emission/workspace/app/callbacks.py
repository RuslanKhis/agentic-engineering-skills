"""Agent callbacks."""
from __future__ import annotations

from app import staging


def refresh_cards_after_preference_change(callback_context):
    """Re-stage the cards in the customer's current currency, then emit everything staged.

    This is the only place that renders widgets (see app/staging.py).
    """
    currency = callback_context.state.get("user:currency", "GBP")
    staging.restage_cards_for_currency(callback_context.state, currency)
    return staging.emit_staged_widgets(callback_context)
