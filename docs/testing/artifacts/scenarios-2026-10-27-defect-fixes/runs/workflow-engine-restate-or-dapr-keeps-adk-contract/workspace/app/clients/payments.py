"""Client for the payments provider's refund API.

The provider de-duplicates on the Idempotency-Key header for 7 days: a repeat of the same key
returns the original refund instead of creating a new one.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport


class PaymentsError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    @property
    def retryable(self) -> bool:
        """A 5xx, 408 or 429 may succeed on a repeat with the same key; other 4xx will not."""
        code = self.status_code
        return code is None or code >= 500 or code in (408, 429)


@dataclass
class PaymentsClient:
    base_url: str
    transport: Transport
    api_key: str = ""

    def create_refund(self, order_id: str, amount_cents: int, reason: str,
                      idempotency_key: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        resp = self.transport.request(
            "POST", f"{self.base_url}/refunds",
            json={"order_id": order_id, "amount_cents": amount_cents, "reason": reason},
            headers=headers, timeout=10.0)
        if resp.status_code >= 400:
            raise PaymentsError(f"refund rejected: {resp.status_code}", resp.status_code)
        return resp.body
