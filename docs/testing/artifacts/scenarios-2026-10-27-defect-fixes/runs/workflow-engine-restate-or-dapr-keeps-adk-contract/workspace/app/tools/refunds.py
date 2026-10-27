"""Refund requests. The model can only submit one; payment happens after a manager approves."""
from __future__ import annotations

from app import services
from app.approvals import RefundRequest, refund_key


def request_refund(order_id: str, amount_cents: int, reason: str, tool_context) -> dict:
    """Ask for part or all of one of the signed-in customer's orders to be refunded.

    The refund is paid only after a manager approves it, which can take days. Calling this ends
    the customer's part: tell them it is waiting for approval and that they need not start again.

    Args:
        order_id: The order to refund, e.g. "HO-10442".
        amount_cents: Amount to refund in cents; at most the order total.
        reason: One short sentence the customer gave, stored with the refund.

    Returns:
        {"status": "pending_approval", "operation_id": ...}, or {"status": "error", "message": ...}.
    """
    svc = services.get()
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if amount_cents <= 0 or amount_cents > order["total_cents"]:
        return {"status": "error", "message": "Amount must be between 1 cent and the order total."}
    if amount_cents > svc.max_refund_cents:
        return {"status": "error", "message": "Refunds above the limit need a supervisor."}
    if svc.approvals is None:
        return {"status": "error", "message": "Refund approvals are unavailable; a colleague will follow up."}
    request = RefundRequest(
        operation_id=refund_key(tool_context.user_id, order["order_id"], amount_cents),
        user_id=tool_context.user_id, order_id=order["order_id"], amount_cents=amount_cents,
        reason=reason, ttl_days=svc.approval_ttl_days)
    status = svc.approvals.submit(request)  # idempotent on operation_id
    if status in ("declined", "expired", "rejected", "invalid"):
        return {"status": "error", "operation_id": request.operation_id,
                "message": f"An earlier identical request ended as {status}; a colleague must review it."}
    if status == "refunded":
        return {"status": "refunded", "operation_id": request.operation_id}
    return {"status": "pending_approval", "operation_id": request.operation_id}
