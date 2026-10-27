"""Which refunds wait for the customer's explicit confirmation, and how long a request stays answerable."""
from __future__ import annotations

APPROVAL_THRESHOLD_CENTS = 5_000
# A confirmation request not answered within this window is cancelled, never executed.
APPROVAL_TTL_SECONDS = 15 * 60

_YES = {"yes", "y", "confirm", "confirmed", "approve", "approved", "ok", "okay", "go ahead", "yes please"}
_NO = {"no", "n", "cancel", "stop", "deny", "decline", "don't", "do not"}


def refund_needs_approval(amount_cents=0, order_id: str = "", **_) -> bool:
    """require_confirmation callable for issue_refund: refunds above the threshold wait."""
    return amount_cents > APPROVAL_THRESHOLD_CENTS


def approval_expired(requested_at: float, now: float, ttl_seconds: int = APPROVAL_TTL_SECONDS) -> bool:
    return now - requested_at > ttl_seconds


def interpret_reply(text: str) -> bool | None:
    """True = explicit yes, False = explicit no, None = anything else (never treated as consent)."""
    cleaned = text.strip().lower().rstrip(".! ")
    if cleaned in _YES:
        return True
    if cleaned in _NO or cleaned.startswith(("no ", "no,", "cancel", "stop")):
        return False
    return None
