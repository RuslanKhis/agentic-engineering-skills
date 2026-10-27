"""Refund operations: the durable review record and the steps around it. No ADK, no Restate.

The refund tool only submits an operation (state `pending`) and the turn ends. A manager's decision
is a conditional transition on the stored operation; the review workflow then performs the one
payment write from the stored payload with the stored provider key. The model supplies business
inputs only: requester, approver, payload and key all come from code.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

from app import services
from app.clients.payments import PaymentsError


class ReviewRefused(Exception):
    """A decision the caller may not make. `code` is one of: forbidden, not_found, self_approval."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # sorts as text


def base_key(user_id: str, order_id: str, amount_cents: int) -> str:
    """One refund request per customer, order and amount; a repeat finds the same operation."""
    return "rf-" + hashlib.sha256(f"{user_id}|{order_id}|{amount_cents}".encode()).hexdigest()[:32]


def check_request(svc: services.Services, user_id: str, order_id: str, amount_cents: int) -> tuple[dict | None, str]:
    """Return (order, "") when the refund is allowed, else (None, message). Run again at execution."""
    order = svc.store.get_order(order_id.strip().upper())
    if order is None or order["customer_id"] != user_id:
        return None, f"No order {order_id} on this account."
    if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) \
            or amount_cents <= 0 or amount_cents > order["total_cents"]:
        return None, "Amount must be between 1 cent and the order total."
    if amount_cents > svc.max_refund_cents:
        return None, "Refunds above the limit need a supervisor."
    return order, ""


def public(op: dict) -> dict:
    """What the model and the customer may see. `payment_processed` is true only after completion."""
    state = "pending_approval" if op["state"] == "pending" else op["state"]
    return {"status": state, "operation_id": op["op_id"], "order_id": op["order_id"],
            "amount_cents": op["amount_cents"], "payment_processed": op["state"] == "completed"}


def submit(user_id: str, order_id: str, amount_cents: int, reason: str, now: str | None = None) -> dict:
    svc = services.get()
    order, message = check_request(svc, user_id, order_id, amount_cents)
    if order is None:
        return {"status": "error", "message": message, "payment_processed": False}
    now = now or utcnow()
    expires = (datetime.fromisoformat(now.replace("Z", "+00:00")) + timedelta(days=svc.approval_days)) \
        .strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    op, _ = svc.store.create_refund_op(base_key(user_id, order["order_id"], amount_cents), user_id,
                                       order["order_id"], amount_cents, reason, now, expires)
    if op["state"] == "pending":
        # Repeat-safe, so every request for a pending operation re-asserts the workflow: a failure
        # after the record committed is healed by the customer asking again.
        try:
            svc.reviews.start(op["op_id"])
        except Exception:
            return {"status": "error", "payment_processed": False,
                    "message": "The request is saved but could not be queued for approval yet. Try again shortly."}
    return public(op)


def review(op_id: str, approved: bool, approver_id: str, approver_email: str, now: str | None = None) -> dict:
    """A manager's decision. Authority is checked here; the workflow acts only on the stored state."""
    svc = services.get()
    if approver_email.lower() not in svc.manager_emails:
        raise ReviewRefused("forbidden")
    op = svc.store.get_refund_op(op_id)
    if op is None:
        raise ReviewRefused("not_found")
    if approver_id == op["customer_id"]:
        raise ReviewRefused("self_approval")
    op = svc.store.decide_refund_op(op_id, approved, approver_id, now or utcnow())
    if op["state"] in ("approved", "rejected"):
        svc.reviews.wake(op_id)  # repeat-safe, so a repeated decision re-wakes a workflow whose wake was lost
    return public(op)


def status(op_id: str, user_id: str, user_email: str) -> dict | None:
    svc = services.get()
    op = svc.store.get_refund_op(op_id)
    if op is None or (op["customer_id"] != user_id and user_email.lower() not in svc.manager_emails):
        return None  # the same answer for "absent" and "not yours"
    return public(op)


# Steps the workflow journals. Each is safe to run again after a crash.

def seconds_until_expiry(op_id: str, now: str | None = None) -> float:
    op = services.get().store.get_refund_op(op_id)
    parse = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))  # noqa: E731
    return max(0.0, (parse(op["expires_at"]) - parse(now or utcnow())).total_seconds())


def expire(op_id: str, now: str | None = None) -> dict:
    """The timer fired. Wins only while the operation is still pending; an approval that landed
    first stands and is executed."""
    return public(services.get().store.expire_refund_op(op_id, now or utcnow()))


def execute(op_id: str) -> dict:
    """Pay an approved operation: the stored payload, the stored key. Anything not approved or
    already executing is left alone. A transient provider failure raises so the engine retries
    with the same key."""
    svc = services.get()
    op = svc.store.claim_refund_op(op_id)
    if op is None:
        return public(svc.store.get_refund_op(op_id))
    order, _ = check_request(svc, op["customer_id"], op["order_id"], op["amount_cents"])
    if order is None:
        return public(svc.store.finish_refund_op(op_id, "failed"))
    try:
        result = svc.payments.create_refund(op["order_id"], op["amount_cents"], op["reason"],
                                            idempotency_key=op_id)
    except PaymentsError as exc:
        if exc.final:
            return public(svc.store.finish_refund_op(op_id, "failed"))
        raise
    refund_id = "rf_" + hashlib.sha256(op_id.encode()).hexdigest()[:12]  # stable across step retries
    return public(svc.store.finish_refund_op(op_id, "completed", result.get("id"), refund_id))


def mark_outcome_unknown(op_id: str) -> dict:
    """Retries are exhausted with the provider's answer unknown: stop, keep the key, reconcile by hand."""
    return public(services.get().store.finish_refund_op(op_id, "outcome_unknown"))
