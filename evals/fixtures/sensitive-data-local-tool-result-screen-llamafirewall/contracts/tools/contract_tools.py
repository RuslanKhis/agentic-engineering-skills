"""Tools. Backends are injected so tests use fakes; nothing here imports google.adk."""
from __future__ import annotations

from typing import Any

BACKENDS: dict[str, Any] = {}


def fetch_url(url: str) -> dict:
    """Fetch a public web page and return its text (first 20,000 characters).

    Returns {"status": "ok", "url", "text"} or {"status": "error", "message"}.
    """
    try:
        text = BACKENDS["web"].get(url)
    except Exception as exc:
        return {"status": "error", "message": f"could not fetch {url}: {type(exc).__name__}"}
    return {"status": "ok", "url": url, "text": text[:20_000]}


def read_contract(contract_id: str) -> dict:
    """Read a contract from the matter store.

    Returns {"status": "ok", "contract_id", "title", "text"} or {"status": "not_found"}.
    """
    doc = BACKENDS["matters"].get(contract_id)
    if doc is None:
        return {"status": "not_found"}
    return {"status": "ok", "contract_id": contract_id, **doc}


def send_email(to: str, subject: str, body: str) -> dict:
    """Send a summary email. Returns {"status": "sent"}."""
    BACKENDS["mail"].send(to, subject, body)
    return {"status": "sent"}
