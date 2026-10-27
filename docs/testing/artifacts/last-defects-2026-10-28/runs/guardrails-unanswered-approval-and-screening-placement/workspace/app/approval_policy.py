"""Which refunds wait for the customer's explicit confirmation, and how long a request stays answerable."""
from __future__ import annotations

APPROVAL_THRESHOLD_CENTS = 5_000
# An unanswered confirmation request is void after this long; a later message cannot approve it.
CONFIRMATION_TTL_SECONDS = 15 * 60

APPROVE, DECLINE, UNCLEAR = "approve", "decline", "unclear"
_YES = {"yes", "y", "yep", "yeah", "confirm", "confirmed", "approve", "ok", "okay", "sure", "go ahead",
        "yes please", "please do", "do it"}
_NO_PREFIXES = ("no", "cancel", "stop", "don't", "dont", "do not", "never mind", "nevermind")


def refund_needs_approval(amount_cents=0, order_id: str = "", **_) -> bool:
    """require_confirmation callable for issue_refund: refunds above the threshold wait."""
    return amount_cents > APPROVAL_THRESHOLD_CENTS


def classify_reply(text: str) -> str:
    """Only an explicit yes approves. Anything that is not clearly yes or no is UNCLEAR."""
    cleaned = text.strip().lower().rstrip(".!").strip()
    if cleaned.startswith(_NO_PREFIXES):
        return DECLINE
    if cleaned in _YES:
        return APPROVE
    return UNCLEAR


def is_expired(requested_at: float, now: float, ttl: float = CONFIRMATION_TTL_SECONDS) -> bool:
    return now - requested_at > ttl


def resolve_pending(text: str, requested_at: float, now: float) -> str:
    """What to do with a customer message while a confirmation is pending.

    Returns "approve" or "decline" (resume the tool with that answer), "expired" (resume with a
    decline, then treat the message as a fresh one) or "ask_again" (do not resume; re-prompt).
    """
    if is_expired(requested_at, now):
        return "expired"
    answer = classify_reply(text)
    return "ask_again" if answer == UNCLEAR else answer
