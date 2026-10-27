"""Dapr Workflow binding for the refund approval. The only module that imports dapr.

Written against dapr-ext-workflow for Dapr 1.15 from the SDK's documented API; it has not been
imported or run in this repository yet (no network to install it). Its logic is thin on purpose:
the workflow and activity bodies live in app/approvals.py and are tested there.
"""
from __future__ import annotations

import json
from datetime import timedelta
from typing import Any

from app import approvals
from app.approvals import OperationClosed, RefundRequest, UnknownOperation

_RUNNING = {"RUNNING", "PENDING", "SUSPENDED"}


def _status_name(state) -> str:
    return getattr(state.runtime_status, "name", str(state.runtime_status)).removeprefix("WORKFLOW_STATUS_")


class DaprApprovalGateway:
    def __init__(self) -> None:
        from dapr.ext.workflow import DaprWorkflowClient, RetryPolicy, WorkflowRuntime

        self._client = DaprWorkflowClient()
        self.runtime = WorkflowRuntime()
        # Retryable provider failures re-run the activity with the same idempotency key.
        approvals.ACTIVITY_RETRY = RetryPolicy(
            first_retry_interval=timedelta(seconds=5), max_number_of_attempts=8,
            backoff_coefficient=2.0, max_retry_interval=timedelta(minutes=10),
            retry_timeout=timedelta(hours=6))
        self.runtime.register_workflow(approvals.refund_approval_workflow, name=approvals.WORKFLOW_NAME)
        self.runtime.register_activity(approvals.execute_refund_activity, name="execute_refund")

    def start(self) -> None:
        self.runtime.start()

    def stop(self) -> None:
        self.runtime.shutdown()

    def _state(self, operation_id: str):
        return self._client.get_workflow_state(operation_id, fetch_payloads=True)

    def submit(self, request: RefundRequest) -> str:
        if self._state(request.operation_id) is None:
            try:
                self._client.schedule_new_workflow(
                    workflow=approvals.refund_approval_workflow, input=request.to_dict(),
                    instance_id=request.operation_id)
            except Exception:
                if self._state(request.operation_id) is None:  # not a concurrent duplicate
                    raise
        return (self.status(request.operation_id) or {}).get("status", "pending")

    def decide(self, operation_id: str, reviewer_id: str, approved: bool, digest: str) -> None:
        state = self._state(operation_id)
        if state is None:
            raise UnknownOperation(operation_id)
        if _status_name(state) not in _RUNNING:
            raise OperationClosed(operation_id)
        self._client.raise_workflow_event(
            instance_id=operation_id, event_name=approvals.DECISION_EVENT,
            data={"reviewer_id": reviewer_id, "approved": approved, "digest": digest})

    def status(self, operation_id: str) -> dict[str, Any] | None:
        state = self._state(operation_id)
        if state is None:
            return None
        payload = json.loads(state.serialized_input) if getattr(state, "serialized_input", None) else None
        info: dict[str, Any] = {"operation_id": operation_id}
        if payload:
            info["request"] = payload
            info["digest"] = RefundRequest.from_dict(payload).digest
        name = _status_name(state)
        if name in _RUNNING:
            info["status"] = "pending"
        elif name == "COMPLETED" and getattr(state, "serialized_output", None):
            info.update(json.loads(state.serialized_output))
        else:
            info["status"] = "failed"
        return info
