"""The agent's two tools. No google.adk imports, so tests can load them directly."""
from __future__ import annotations

from expense_agent.rules import mandatory_escalation_reason
from expense_agent.store import ClaimStore

_store: ClaimStore | None = None


def configure(store: ClaimStore) -> None:
    global _store
    _store = store


def decide_claim(claim_id: str, decision: str, reason: str) -> dict:
    """Approve or reject a claim yourself.

    Args:
        claim_id: The claim being triaged.
        decision: "approve" or "reject".
        reason: One sentence the employee will see.
    """
    if decision not in ("approve", "reject"):
        return {"status": "error", "message": "decision must be approve or reject"}
    claim = _store.get(claim_id)
    if claim is None:
        return {"status": "error", "message": "unknown claim"}
    if claim["lane"]:
        return {"status": "error", "message": "claim already triaged"}
    required = mandatory_escalation_reason(claim)
    if required:
        return {"status": "error", "message": f"{required}; use escalate_claim"}
    _store.set_outcome(claim_id, "decided", decision, reason)
    return {"status": "ok", "claim_id": claim_id, "decision": decision}


def escalate_claim(claim_id: str, reason: str) -> dict:
    """Send the claim to the finance review queue for a person to decide.

    Args:
        claim_id: The claim being triaged.
        reason: Why a person needs to look at it.
    """
    claim = _store.get(claim_id)
    if claim is None:
        return {"status": "error", "message": "unknown claim"}
    if claim["lane"]:
        return {"status": "error", "message": "claim already triaged"}
    _store.set_outcome(claim_id, "finance_review", None, reason)
    return {"status": "ok", "claim_id": claim_id, "lane": "finance_review"}
