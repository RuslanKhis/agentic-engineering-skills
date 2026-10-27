"""Restate ingress client: starts the review workflow for an operation and wakes it on a decision.

Both calls are keyed by the operation id and safe to repeat. Restate's ingress has no caller
authentication of its own: keep it reachable only from this service (NetworkPolicy), and note that
the workflow trusts the stored operation, never anything carried by a wake-up.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport

WORKFLOW = "RefundReview"


class ReviewEngineError(Exception):
    pass


@dataclass
class RestateReviews:
    ingress_url: str
    transport: Transport

    def _post(self, path: str, op_id: str) -> None:
        resp = self.transport.request(
            "POST", f"{self.ingress_url.rstrip('/')}/{WORKFLOW}/{op_id}/{path}",
            json={"op_id": op_id} if path == "run/send" else None,
            headers={"Idempotency-Key": f"{path}:{op_id}"}, timeout=5.0)
        if resp.status_code >= 400:
            raise ReviewEngineError(f"restate {path} answered {resp.status_code}")

    def start(self, op_id: str) -> None:
        self._post("run/send", op_id)

    def wake(self, op_id: str) -> None:
        self._post("decided/send", op_id)


class UnconfiguredReviews:
    """Production selects Restate or fails: refunds are never queued into nothing."""

    def start(self, op_id: str) -> None:
        raise ReviewEngineError("RESTATE_INGRESS_URL is not set")

    wake = start
