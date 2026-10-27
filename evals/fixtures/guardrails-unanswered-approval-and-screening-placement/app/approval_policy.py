"""Which refunds wait for the customer's explicit confirmation."""
from __future__ import annotations

APPROVAL_THRESHOLD_CENTS = 5_000


def refund_needs_approval(amount_cents=0, order_id: str = "", **_) -> bool:
    """require_confirmation callable for issue_refund: refunds above the threshold wait."""
    return amount_cents > APPROVAL_THRESHOLD_CENTS
