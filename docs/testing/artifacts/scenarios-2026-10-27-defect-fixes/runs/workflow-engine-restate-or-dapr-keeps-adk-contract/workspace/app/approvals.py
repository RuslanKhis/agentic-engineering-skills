"""Durable refund approval: the request, the decision checks, the workflow and its payment activity.

The chat turn only submits a RefundRequest and ends. A Dapr workflow keyed by the operation id waits
for a manager's decision (or expiry), then runs the payment activity. Nothing here imports dapr or
google.adk: the workflow is a plain generator driven by a context object, and app/dapr_runtime.py
registers it. The refund key is the payments idempotency key, so the activity can run more than once
(Dapr retries, or a crash after the provider accepted the write) and the provider refunds once.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import timedelta
from typing import Any, Protocol

from app import services
from app.clients.payments import PaymentsError

DECISION_EVENT = "manager_decision"
WORKFLOW_NAME = "refund_approval"
# Dapr RetryPolicy for the payment activity; app/dapr_runtime.py sets it when it registers.
ACTIVITY_RETRY: Any = None


class UnknownOperation(LookupError):
    pass


class OperationClosed(RuntimeError):
    """The approval already finished (decided, expired or failed)."""


def refund_key(user_id: str, order_id: str, amount_cents: int) -> str:
    """One refund per customer, order and amount: a repeat sends the same key."""
    return "rf-" + hashlib.sha256(f"{user_id}|{order_id}|{amount_cents}".encode()).hexdigest()[:32]


def refund_id_for(key: str) -> str:
    return "rf_" + key[3:15]


@dataclass(frozen=True)
class RefundRequest:
    operation_id: str  # == refund_key: workflow instance id and payments idempotency key
    user_id: str  # the verified customer, copied from the principal by the tool
    order_id: str
    amount_cents: int
    reason: str
    ttl_days: int = 14

    @property
    def digest(self) -> str:
        """What a manager approves; the decision must carry it back."""
        body = json.dumps([self.operation_id, self.user_id, self.order_id, self.amount_cents, self.reason])
        return hashlib.sha256(body.encode()).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RefundRequest":
        return cls(**data)


class ApprovalGateway(Protocol):
    def submit(self, request: RefundRequest) -> str:
        """Start (or find) the approval for request.operation_id; returns its status."""

    def decide(self, operation_id: str, reviewer_id: str, approved: bool, digest: str) -> None: ...

    def status(self, operation_id: str) -> dict[str, Any] | None: ...


def check_decision(request: RefundRequest, decision: dict[str, Any]) -> str | None:
    """None when the decision may stand, else why it is ignored. The endpoint has already checked
    that the reviewer is a manager; the workflow re-checks what it can see from its own input."""
    if decision.get("digest") != request.digest:
        return "digest_mismatch"
    reviewer = decision.get("reviewer_id")
    if not reviewer:
        return "no_reviewer"
    if reviewer == request.user_id:
        return "self_approval"
    if not isinstance(decision.get("approved"), bool):
        return "malformed"
    return None


def refund_approval_workflow(ctx, payload: dict[str, Any]):
    """Orchestrator. Deterministic: time from ctx, no I/O, effects only through the activity."""
    request = RefundRequest.from_dict(payload)
    deadline = ctx.current_utc_datetime + timedelta(days=request.ttl_days)
    expiry = ctx.create_timer(deadline)  # created once; every wait below races the same deadline
    while True:
        event = ctx.wait_for_external_event(DECISION_EVENT)
        winner = yield ctx.when_any([event, expiry])
        if winner == expiry:
            return {"status": "expired", "operation_id": request.operation_id}
        decision = event.get_result()
        if check_decision(request, decision) is not None:
            continue  # a bad event neither approves nor kills the request
        if not decision["approved"]:
            return {"status": "declined", "operation_id": request.operation_id,
                    "reviewer_id": decision["reviewer_id"]}
        outcome = yield ctx.call_activity(execute_refund_activity, input=payload,
                                          retry_policy=ACTIVITY_RETRY)
        outcome["operation_id"] = request.operation_id
        outcome["reviewer_id"] = decision["reviewer_id"]
        return outcome


def execute_refund_activity(_ctx, payload: dict[str, Any]) -> dict[str, Any]:
    """Dapr activity entry point. Raises on a retryable provider failure so Dapr retries."""
    return execute_refund(RefundRequest.from_dict(payload))


def execute_refund(request: RefundRequest) -> dict[str, Any]:
    """Re-check the preconditions at payment time, then pay once through the idempotency key.

    Returns {"status": "refunded" | "invalid" | "rejected", ...}. A retryable provider failure
    (5xx, 408, 429, or a transport error) propagates so the caller retries with the same key.
    """
    svc = services.get()
    order = svc.store.get_order(request.order_id)
    if order is None or order["customer_id"] != request.user_id:
        return {"status": "invalid", "message": "order no longer on this account"}
    if not 0 < request.amount_cents <= order["total_cents"] or request.amount_cents > svc.max_refund_cents:
        return {"status": "invalid", "message": "amount no longer allowed"}
    refund_id = refund_id_for(request.operation_id)
    try:
        result = svc.payments.create_refund(request.order_id, request.amount_cents, request.reason,
                                            idempotency_key=request.operation_id)
    except PaymentsError as exc:
        if exc.retryable:
            raise
        return {"status": "rejected", "message": str(exc)}
    svc.store.record_refund(refund_id, request.order_id, request.amount_cents, result.get("id"))
    return {"status": "refunded", "refund_id": refund_id, "amount_cents": request.amount_cents}
