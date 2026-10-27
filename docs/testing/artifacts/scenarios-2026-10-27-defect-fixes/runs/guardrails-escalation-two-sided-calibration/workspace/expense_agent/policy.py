"""Escalation rules that are policy, not judgement. No google.adk imports."""
from __future__ import annotations

import math

TRAVEL_CATEGORIES = frozenset({"flights", "rail", "hotel", "car hire"})
OVER_LIMIT_EUR = 500


def forced_escalation_reason(claim: dict) -> str | None:
    """Why code must route this claim to finance review, or None if the model may decide.

    Fails closed: a category or total that cannot be read forces review.
    """
    category = claim.get("category")
    if not isinstance(category, str) or not category.strip():
        return "category missing or unreadable"
    if category.strip().lower() in TRAVEL_CATEGORIES:
        return "travel category requires finance review"
    total = claim.get("total_eur")
    if isinstance(total, bool) or not isinstance(total, (int, float)) or not math.isfinite(total):
        return "total missing or unreadable"
    if total > OVER_LIMIT_EUR:
        return "total over 500 EUR requires finance review"
    return None
