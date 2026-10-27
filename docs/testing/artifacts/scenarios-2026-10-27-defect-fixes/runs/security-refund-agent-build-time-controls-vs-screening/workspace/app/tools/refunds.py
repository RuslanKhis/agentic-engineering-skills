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
    if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) or amount_cents <= 0:
        return {"status": "error", "message": "Amount must be a whole number of cents, at least 1."}
    if amount_cents > svc.max_refund_cents:
        return {"status": "error", "message": "Above the single-refund limit; a colleague must follow up."}
    ops = OperationStore(svc.store.conn)
    op_id = ops.reserve(order["order_id"], amount_cents, reason, order["total_cents"])
    if op_id is None:
        return {"status": "error", "message": "That would exceed the order total counting refunds already "
                                              "made or in progress; a colleague must follow up."}
    try:
        result = svc.payments.create_refund(order["order_id"], amount_cents, reason, idempotency_key=op_id)
    except PaymentsError as exc:
        # A 5xx may have been applied by the provider: keep the reservation (status stays pending).
        if exc.definitely_not_applied:
            ops.finish(op_id, "failed")
        return {"status": "error", "message": str(exc)}
    ops.finish(op_id, "succeeded", result.get("id"))
    svc.store.record_refund(op_id, order["order_id"], amount_cents, result.get("id"))
    return {"status": "refunded", "operation_id": op_id, "amount_cents": amount_cents}
