"""Client for the shared support mailbox."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport


@dataclass
class MailClient:
    base_url: str
    transport: Transport

    def get_message(self, message_id: str) -> dict:
        resp = self.transport.request("GET", f"{self.base_url}/messages/{message_id}")
        return resp.body

    def send(self, to: str, subject: str, body: str) -> dict:
        resp = self.transport.request("POST", f"{self.base_url}/send",
                                      json={"to": to, "subject": subject, "body": body})
        return resp.body
