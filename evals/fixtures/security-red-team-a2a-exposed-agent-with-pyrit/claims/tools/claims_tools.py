"""Claim tools. The backends are injected so tests use fakes."""
from __future__ import annotations

from typing import Any

BACKENDS: dict[str, Any] = {}


def read_document(document_id: str) -> dict:
    """Read the text of a document the claimant uploaded.

    Returns {"status": "ok", "text": ...} or {"status": "not_found"}.
    """
    text = BACKENDS["documents"].get(document_id)
    return {"status": "ok", "text": text} if text is not None else {"status": "not_found"}


def file_payout(claim_id: str, amount_cents: int, payee_account: str) -> dict:
    """File a payout on an approved claim.

    Args:
        claim_id: The claim, e.g. "CLM-30418".
        amount_cents: Amount in cents.
        payee_account: The IBAN on file for the claimant.
    """
    return {"status": "filed", "payout_id": BACKENDS["payouts"].file(claim_id, amount_cents, payee_account)}


def send_email(to: str, subject: str, body: str) -> dict:
    """Email the claimant or an adjuster. Returns {"status": "sent"}."""
    BACKENDS["mail"].send(to, subject, body)
    return {"status": "sent"}
