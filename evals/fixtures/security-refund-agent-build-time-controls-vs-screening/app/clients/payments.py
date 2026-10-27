"""Client for the payments provider's refund API."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport


class PaymentsError(Exception):
    pass


@dataclass
class PaymentsClient:
    base_url: str
    transport: Transport
    api_key: str = ""

    def create_refund(self, order_id: str, amount_cents: int, reason: str, idempotency_key: str) -> dict:
        resp = self.transport.request(
            "POST", f"{self.base_url}/refunds",
            json={"order_id": order_id, "amount_cents": amount_cents, "reason": reason},
            headers={"Authorization": f"Bearer {self.api_key}", "Idempotency-Key": idempotency_key},
            timeout=10.0)
        if resp.status_code >= 400:
            raise PaymentsError(f"refund rejected: {resp.status_code}")
        return resp.body
