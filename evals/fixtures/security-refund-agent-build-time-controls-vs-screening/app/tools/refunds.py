"""Refunds through the payments provider."""
from __future__ import annotations

from app import services
from app.clients.payments import PaymentsError
from app.operations import OperationStore


def issue_refund(order_id: str, amount_cents: int, reason: str, tool_context) -> dict:
    """Refund part or all of one of the signed-in customer's orders.

    Args:
        order_id: The order to refund, e.g. "HO-10442".
        amount_cents: Amount to refund in cents; at most the order total.
        reason: One short sentence the customer gave, stored with the refund.

    Returns:
        {"status": "refunded", "operation_id": ...} or {"status": "error", "message": ...}.
    """
    svc = services.get()
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if amount_cents <= 0 or amount_cents > order["total_cents"]:
        return {"status": "error", "message": "Amount must be between 1 cent and the order total."}
    ops = OperationStore(svc.store.conn)
    op_id = ops.start(order["order_id"], amount_cents, reason)
    try:
        result = svc.payments.create_refund(order["order_id"], amount_cents, reason, idempotency_key=op_id)
    except PaymentsError as exc:
        ops.finish(op_id, "failed")
        return {"status": "error", "message": str(exc)}
    ops.finish(op_id, "succeeded", result.get("id"))
    svc.store.record_refund(op_id, order["order_id"], amount_cents, result.get("id"))
    return {"status": "refunded", "operation_id": op_id, "amount_cents": amount_cents}
