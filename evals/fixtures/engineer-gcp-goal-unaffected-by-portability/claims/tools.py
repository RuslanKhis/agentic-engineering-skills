"""Claim tools over a repository interface; Firestore in production, a dict in tests."""
from __future__ import annotations

from typing import Protocol


class ClaimRepository(Protocol):
    def get(self, claim_id: str) -> dict | None: ...
    def add_note(self, claim_id: str, note: str) -> None: ...


class DictClaims:
    def __init__(self, claims: dict[str, dict]):
        self.claims = claims

    def get(self, claim_id):
        return self.claims.get(claim_id)

    def add_note(self, claim_id, note):
        self.claims[claim_id].setdefault("notes", []).append(note)


_repo: ClaimRepository | None = None


def use_repository(repo: ClaimRepository) -> None:
    global _repo
    _repo = repo


def claim_status(claim_id: str, tool_context) -> dict:
    """Status, stage and next step of one of the policyholder's claims.

    Args:
        claim_id: Claim reference such as "CL-20931".
    """
    claim = _repo.get(claim_id)
    if claim is None or claim["policyholder_id"] != tool_context.user_id:
        return {"status": "not_found"}
    return {"status": "ok", "claim_id": claim_id, "stage": claim["stage"], "next_step": claim["next_step"]}


def add_claim_note(claim_id: str, note: str, tool_context) -> dict:
    """Add the policyholder's note (new damage, a contractor quote) to their claim."""
    claim = _repo.get(claim_id)
    if claim is None or claim["policyholder_id"] != tool_context.user_id:
        return {"status": "not_found"}
    _repo.add_note(claim_id, note[:2000])
    return {"status": "noted"}
