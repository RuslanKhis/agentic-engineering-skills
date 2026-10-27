"""Refunds through the payments provider."""
from __future__ import annotations

import uuid

from app import services
from app.clients.payments import PaymentsError


def issue_refund(order_id: str, amount_cents: int, reason: str, tool_context) -> dict:
    """Refund part or all of one of the signed-in customer's orders.

    Args:
        order_id: The order to refund, e.g. "HO-10442".
        amount_cents: Amount to refund in cents; at most the order total.
        reason: One short sentence the customer gave, stored with the refund.

    Returns:
        {"status": "refunded", "refund_id": ...} or {"status": "error", "message": ...}.
    """
    svc = services.get()
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if amount_cents <= 0 or amount_cents > order["total_cents"]:
        return {"status": "error", "message": "Amount must be between 1 cent and the order total."}
    if amount_cents > svc.max_refund_cents:
        return {"status": "error", "message": "Refunds above the limit need a supervisor."}
    try:
        result = svc.payments.create_refund(order["order_id"], amount_cents, reason)
    except PaymentsError as exc:
        return {"status": "error", "message": str(exc)}
    refund_id = f"rf_{uuid.uuid4().hex[:12]}"
    svc.store.record_refund(refund_id, order["order_id"], amount_cents, result.get("id"))
    return {"status": "refunded", "refund_id": refund_id, "amount_cents": amount_cents}
