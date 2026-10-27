"""Refunds through the payments provider.

A refund is two steps: propose_refund records what the customer is being offered and returns a
summary for them to confirm; issue_refund carries out the pending proposal once.
"""
from __future__ import annotations

import uuid

from app import services
from app.clients.payments import PaymentsError

PENDING = "pending_refund"


def propose_refund(order_id: str, amount_cents: int, reason: str, tool_context) -> dict:
    """Prepare a refund for the customer to confirm. Nothing is paid until issue_refund runs.

    Args:
        order_id: The order to refund, e.g. "HO-10442".
        amount_cents: Amount to refund in cents; at most the order total.
        reason: One short sentence the customer gave.

    Returns:
        {"status": "awaiting_confirmation", "summary": ...} or {"status": "error", "message": ...}.
    """
    svc = services.get()
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "error", "message": f"No order {order_id} on this account."}
    if amount_cents <= 0 or amount_cents > order["total_cents"]:
        return {"status": "error", "message": "Amount must be between 1 cent and the order total."}
    if amount_cents > svc.max_refund_cents:
        return {"status": "error", "message": "Refunds above the limit need a supervisor."}
    tool_context.state[PENDING] = {"order_id": order["order_id"], "amount_cents": amount_cents,
                                   "reason": reason, "request_id": uuid.uuid4().hex}
    return {"status": "awaiting_confirmation",
            "summary": f"Refund {amount_cents / 100:.2f} EUR on {order['order_id']}. Shall I go ahead?"}


def issue_refund(tool_context) -> dict:
    """Carry out the refund the customer has just confirmed. Call only after they say yes.

    Returns:
        {"status": "refunded", "refund_id": ...}, {"status": "nothing_pending"} or
        {"status": "error", "message": ...}.
    """
    pending = tool_context.state.get(PENDING)
    if not pending:
        return {"status": "nothing_pending", "message": "There is no refund waiting for confirmation."}
    tool_context.state[PENDING] = None
    svc = services.get()
    try:
        result = svc.payments.create_refund(pending["order_id"], pending["amount_cents"], pending["reason"])
    except PaymentsError as exc:
        return {"status": "error", "message": str(exc)}
    refund_id = f"rf_{uuid.uuid4().hex[:12]}"
    svc.store.record_refund(refund_id, pending["order_id"], pending["amount_cents"], result.get("id"))
    return {"status": "refunded", "refund_id": refund_id, "amount_cents": pending["amount_cents"]}
