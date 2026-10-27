"""Refund requests. A manager approves each one; the payment is made later by the review workflow."""
from __future__ import annotations

from app import refund_ops


def request_refund(order_id: str, amount_cents: int, reason: str, tool_context) -> dict:
    """Ask for a refund on one of the signed-in customer's orders. This only submits the request
    for a manager's approval; no money moves here.

    Args:
        order_id: The order to refund, e.g. "HO-10442".
        amount_cents: Amount to refund in cents; at most the order total.
        reason: One short sentence the customer gave, stored with the request.

    Returns:
        {"status": "pending_approval", "payment_processed": false, ...} when queued;
        "completed" (payment_processed true) only when an earlier identical request was already paid;
        {"status": "error", "message": ...} when the request is refused.
    """
    return refund_ops.submit(tool_context.user_id, order_id, amount_cents, reason)
