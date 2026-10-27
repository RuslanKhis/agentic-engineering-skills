"""Client for the payments provider's refund API (see docs/providers/payments-api.md)."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Response, Transport


class PaymentsError(Exception):
    def __init__(self, status_code: int, body: dict):
        super().__init__(f"refund rejected: {status_code}")
        self.status_code = status_code
        self.body = body


@dataclass
class PaymentsClient:
    base_url: str
    transport: Transport
    api_key: str = ""

    def _headers(self, replay_key: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if replay_key:
            headers["Replay-Key"] = replay_key
        return headers

    def create_refund(self, order_id: str, amount_cents: int, reason: str, replay_key: str) -> dict:
        resp: Response = self.transport.request(
            "POST", f"{self.base_url}/refunds",
            json={"order_id": order_id, "amount_cents": amount_cents, "reason": reason},
            headers=self._headers(replay_key), timeout=8.0)
        if resp.status_code >= 400:
            raise PaymentsError(resp.status_code, resp.body)
        return resp.body

    def find_refund(self, replay_key: str) -> dict | None:
        resp = self.transport.request("GET", f"{self.base_url}/refunds?replay_key={replay_key}",
                                      headers=self._headers(), timeout=5.0)
        if resp.status_code == 404:
            return None
        if resp.status_code >= 400:
            raise PaymentsError(resp.status_code, resp.body)
        return resp.body
