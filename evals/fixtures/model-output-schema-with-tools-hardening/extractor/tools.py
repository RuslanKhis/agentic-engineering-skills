"""Lookup tools for the extractor. No google.adk imports, so they test without the SDK."""
from __future__ import annotations

from extractor.reference import POLICIES, REPAIRERS


def lookup_policy(policy_number: str) -> dict:
    """Check a motor policy number such as "MP-118204" and return its status and insured vehicle.

    Returns:
        {"status": "ok", "policy_status": "active" | "lapsed", "vehicle": ...}
        or {"status": "not_found"} when no policy has that number.
    """
    policy = POLICIES.get(policy_number.strip().upper())
    if policy is None:
        return {"status": "not_found"}
    return {"status": "ok", "policy_status": policy["status"], "vehicle": policy["vehicle"]}


def lookup_repairer(name: str) -> dict:
    """Find an approved repairer by (part of) its trading name.

    Returns:
        {"status": "ok", "matches": [{"repairer_id", "name", "town"}]}; matches may be empty.
    """
    needle = name.strip().lower()
    return {"status": "ok", "matches": [r for r in REPAIRERS if needle and needle in r["name"].lower()]}
