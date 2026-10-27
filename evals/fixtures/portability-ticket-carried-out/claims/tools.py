"""Claim tools over Firestore. The caller's ID comes from the verified Identity Platform token."""
from __future__ import annotations

from google.cloud import firestore

_db = None


def _client() -> firestore.Client:
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


def get_claim(claim_id: str, tool_context) -> dict:
    """Return one of the caller's claims: status, type, opened date and notes."""
    snap = _client().collection("claims").document(claim_id).get()
    if not snap.exists or snap.get("owner_id") != tool_context.user_id:
        return {"status": "not_found"}
    data = snap.to_dict()
    return {"status": "ok", "claim": {k: data[k] for k in ("claim_status", "type", "opened", "notes")}}


def add_note(claim_id: str, note: str, tool_context) -> dict:
    """Add the caller's note to one of their open claims."""
    ref = _client().collection("claims").document(claim_id)
    snap = ref.get()
    if not snap.exists or snap.get("owner_id") != tool_context.user_id:
        return {"status": "not_found"}
    ref.update({"notes": firestore.ArrayUnion([note])})
    return {"status": "added"}
