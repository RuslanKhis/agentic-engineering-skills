"""Mail and Drive tools. Clients are injected; nothing here imports google.adk."""
from __future__ import annotations

from typing import Any

CLIENTS: dict[str, Any] = {}


def search_mail(query: str) -> dict:
    """Search the staff member's mailbox. Returns {"status": "ok", "messages": [{id, from, subject, snippet}]}."""
    return {"status": "ok", "messages": CLIENTS["gmail"].search(query)}


def send_mail(to: str, subject: str, body: str) -> dict:
    """Send an email from the staff member's mailbox. Returns {"status": "sent"}."""
    CLIENTS["gmail"].send(to, subject, body)
    return {"status": "sent"}


def read_drive_file(file_id: str) -> dict:
    """Read a Drive file's text. Returns {"status": "ok", "name", "text"}."""
    return {"status": "ok", **CLIENTS["drive"].read(file_id)}


def share_drive_file(file_id: str, email: str, role: str = "reader") -> dict:
    """Share a Drive file. Returns {"status": "shared"}."""
    CLIENTS["drive"].share(file_id, email, role)
    return {"status": "shared"}
