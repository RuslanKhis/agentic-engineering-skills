"""Tools for the triage agent. No google.adk imports."""
from __future__ import annotations

CATEGORIES = {"battery", "motor", "frame", "display", "other"}


def lookup_product(serial: str) -> dict:
    """Look up a product by serial number, e.g. "EB-2291-0042"."""
    if not serial.startswith("EB-"):
        return {"status": "not_found", "message": f"No product {serial}."}
    return {"status": "ok", "model": "Trail 5", "warranty_until": "2027-03-31"}


def record_triage(claim_id: str, category: str, urgency: int) -> dict:
    """Record the triage decision for a claim. urgency is 1 (low) to 3 (high)."""
    if category not in CATEGORIES or urgency not in (1, 2, 3):
        return {"status": "error", "message": "category or urgency out of range"}
    return {"status": "recorded", "claim_id": claim_id}
