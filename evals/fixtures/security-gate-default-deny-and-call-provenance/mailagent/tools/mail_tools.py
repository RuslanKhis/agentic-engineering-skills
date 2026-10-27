"""Mail and file tools. Backends are injected; nothing here imports google.adk."""
from __future__ import annotations

from typing import Any

BACKENDS: dict[str, Any] = {}


def search_mail(query: str) -> dict:
    """Search the user's mailbox. Returns {"status": "ok", "threads": [{thread_id, from, subject, snippet}]}."""
    return {"status": "ok", "threads": BACKENDS["mail"].search(query)}


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email from the user's account. Returns {"status": "sent"}."""
    BACKENDS["mail"].send(to, subject, body)
    return {"status": "sent"}


def delete_file(file_id: str) -> dict:
    """Delete a file from the user's drive (moves it to the bin for 30 days). Returns {"status": "deleted"}."""
    BACKENDS["files"].delete(file_id)
    return {"status": "deleted"}


def archive_thread(thread_id: str) -> dict:
    """Archive a mail thread. Returns {"status": "archived"}."""
    BACKENDS["mail"].archive(thread_id)
    return {"status": "archived"}
