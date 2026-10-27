"""Deterministic escalation rules. No google.adk imports, so tests can load them directly."""
from __future__ import annotations

TRAVEL_CATEGORIES = frozenset({"flights", "rail", "hotel", "car hire"})
ESCALATION_THRESHOLD_EUR = 500.0


def mandatory_escalation_reason(claim: dict) -> str | None:
    """Why company rules force this claim to finance review, or None if they don't."""
    category = str(claim.get("category", "")).strip().lower()
    if category in TRAVEL_CATEGORIES:
        return f"Travel category ({category}) requires finance review"
    if float(claim.get("total_eur", 0)) > ESCALATION_THRESHOLD_EUR:
        return f"Total over {ESCALATION_THRESHOLD_EUR:.0f} EUR requires finance review"
    return None
