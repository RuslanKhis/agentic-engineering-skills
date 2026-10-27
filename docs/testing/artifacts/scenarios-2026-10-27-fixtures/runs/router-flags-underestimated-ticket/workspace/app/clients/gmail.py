"""Read-only Gmail REST client. Only GET requests; the caller supplies the user's access token."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.http import Transport

BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me"


@dataclass
class GmailClient:
    transport: Transport
    base_url: str = BASE_URL

    def search(self, access_token: str, query: str, limit: int = 5) -> list[dict]:
        resp = self.transport.request("GET", f"{self.base_url}/messages?maxResults={limit}&q={_quote(query)}",
                                      headers=_auth(access_token))
        _check(resp)
        return resp.body.get("messages", [])

    def get_message(self, access_token: str, message_id: str) -> dict:
        resp = self.transport.request(
            "GET", f"{self.base_url}/messages/{_quote(message_id)}?format=metadata"
                   "&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date",
            headers=_auth(access_token))
        _check(resp)
        return resp.body


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _quote(value: str) -> str:
    from urllib.parse import quote
    return quote(value, safe="")


def _check(resp) -> None:
    if resp.status_code != 200:
        raise RuntimeError(f"gmail returned {resp.status_code}")
