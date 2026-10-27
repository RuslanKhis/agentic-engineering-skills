"""Claim lookups against the claims register export. No ADK import here."""
from __future__ import annotations

CLAIMS = {
    "CL-2026-0412": {"policy": "HP-88120", "status": "open", "type": "water damage", "reserve_eur": 4200},
    "CL-2026-0417": {"policy": "HP-77031", "status": "awaiting documents", "type": "theft", "reserve_eur": 1800},
    "CL-2026-0433": {"policy": "HP-88120", "status": "closed", "type": "glass", "reserve_eur": 0},
}


def get_claim(claim_id: str) -> dict:
    """Look up one claim by its ID, e.g. "CL-2026-0412".

    Returns:
        {"status": "ok", "claim": {...}} or {"status": "not_found"}.
    """
    claim = CLAIMS.get(claim_id.strip().upper())
    if claim is None:
        return {"status": "not_found"}
    return {"status": "ok", "claim": {"claim_id": claim_id.strip().upper(), **claim}}


def missing_documents(claim_id: str) -> dict:
    """List the documents a claim is still waiting for."""
    claim = CLAIMS.get(claim_id.strip().upper())
    if claim is None:
        return {"status": "not_found"}
    needed = ["police report"] if claim["type"] == "theft" and claim["status"] == "awaiting documents" else []
    return {"status": "ok", "missing": needed}
