"""Refunds with retries over the payments client, recorded in the operation store."""
from __future__ import annotations

from dataclasses import dataclass
import time

from app.clients.http import TransportError, TransportTimeout
from app.clients.payments import PaymentsClient, PaymentsError
from app.operations import OperationStore

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


@dataclass
class RefundResult:
    ok: bool
    provider_refund_id: str | None = None
    error: str | None = None


@dataclass
class RefundAdapter:
    client: PaymentsClient
    operations: OperationStore
    max_attempts: int = 3
    backoff_seconds: float = 0.5
    sleep: callable = time.sleep

    def refund(self, operation_id: str, order_id: str, amount_cents: int, reason: str) -> RefundResult:
        payload = {"order_id": order_id, "amount_cents": amount_cents, "reason": reason}
        op = self.operations.begin(operation_id, order_id, amount_cents, payload)
        if op["state"] == "succeeded":
            return RefundResult(True, op["provider_refund_id"])
        last_error = "not attempted"
        for attempt in range(1, self.max_attempts + 1):
            replay_key = f"{operation_id}-{attempt}"
            try:
                body = self.client.create_refund(order_id, amount_cents, reason, replay_key=replay_key)
            except (TransportTimeout, TransportError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                self.operations.record_attempt(operation_id, last_error)
            except PaymentsError as exc:
                last_error = str(exc)
                self.operations.record_attempt(operation_id, last_error)
                if exc.status_code not in RETRYABLE_STATUS:
                    self.operations.fail(operation_id, last_error)
                    return RefundResult(False, error=last_error)
            else:
                self.operations.record_attempt(operation_id)
                self.operations.succeed(operation_id, body["id"])
                return RefundResult(True, body["id"])
            if attempt < self.max_attempts:
                self.sleep(self.backoff_seconds * attempt)
        self.operations.fail(operation_id, last_error)
        return RefundResult(False, error=last_error)
