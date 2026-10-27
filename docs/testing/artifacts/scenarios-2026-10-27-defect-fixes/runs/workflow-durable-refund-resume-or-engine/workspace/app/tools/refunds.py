"""Refunds through the payments provider."""
from __future__ import annotations

import hashlib

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
    # ADK re-runs this function when a paused invocation is resumed (and again if the resume is
    # repeated), with the same function-call id. Derive everything from that id so a replay
    # is the same refund, not a new one.
    call_id = getattr(tool_context, "function_call_id", None)
    if not call_id:
        return {"status": "error", "message": "Refund could not be tied to a request; not issued."}
    key = hashlib.sha256(
        f"{tool_context.user_id}|{order['order_id']}|{amount_cents}|{call_id}".encode()).hexdigest()
    refund_id = f"rf_{key[:12]}"
    if svc.store.get_refund(refund_id) is not None:
        return {"status": "refunded", "refund_id": refund_id, "amount_cents": amount_cents}
    try:
        result = svc.payments.create_refund(order["order_id"], amount_cents, reason, idempotency_key=key)
    except PaymentsError as exc:
        return {"status": "error", "message": str(exc)}
    svc.store.record_refund(refund_id, order["order_id"], amount_cents, result.get("id"))
    return {"status": "refunded", "refund_id": refund_id, "amount_cents": amount_cents}
