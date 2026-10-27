"""Client for the orders team's API (cancellations)."""
from __future__ import annotations

import re
from dataclasses import dataclass

from app.clients.http import Transport

_ORDER_ID = re.compile(r"HO-\d{1,10}")


class OrdersError(Exception):
    """The API refused the request; the order was not changed."""


class OrderAlreadyShipped(OrdersError):
    pass


class OrderOutcomeUnknown(OrdersError):
    """The request may or may not have been applied (timeout, 5xx, unreadable answer)."""


@dataclass
class OrdersClient:
    base_url: str
    transport: Transport
    api_token: str = ""

    def cancel_order(self, order_id: str) -> dict:
        """One attempt, no retries: the API's replay behaviour for cancel is not documented."""
        if not _ORDER_ID.fullmatch(order_id):
            raise OrdersError(f"malformed order id {order_id!r}")
        try:
            resp = self.transport.request(
                "POST", f"{self.base_url}/orders/{order_id}/cancel",
                headers={"Authorization": f"Bearer {self.api_token}"}, timeout=10.0)
        except Exception as exc:  # timeout or connection loss after sending: outcome unknown
            raise OrderOutcomeUnknown("no answer from the orders API") from exc
        if resp.status_code == 409:
            raise OrderAlreadyShipped("order has already shipped")
        if resp.status_code >= 500:
            raise OrderOutcomeUnknown(f"orders API error {resp.status_code}")
        if resp.status_code >= 400:
            raise OrdersError(f"cancellation rejected: {resp.status_code}")
        body = resp.body
        if (body.get("status") != "cancelled" or body.get("order_id") != order_id
                or not body.get("cancellation_id")):
            raise OrderOutcomeUnknown("unexpected answer from the orders API")
        return body
