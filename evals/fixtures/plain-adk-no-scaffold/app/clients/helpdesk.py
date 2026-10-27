"""Client for the helpdesk's ticket API."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport


class HelpdeskError(Exception):
    pass


@dataclass
class HelpdeskClient:
    base_url: str
    transport: Transport

    def open_tickets(self, customer_id: str) -> list[dict]:
        resp = self.transport.request("GET", f"{self.base_url}/customers/{customer_id}/tickets?state=open",
                                      timeout=5.0)
        if resp.status_code >= 400:
            raise HelpdeskError(f"helpdesk returned {resp.status_code}")
        return resp.body.get("tickets", [])
