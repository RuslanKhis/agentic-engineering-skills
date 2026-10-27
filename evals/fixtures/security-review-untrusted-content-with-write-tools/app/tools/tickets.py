"""Notes on the support ticket for the email being handled."""
from __future__ import annotations

from app import services


def add_ticket_note(message_id: str, note: str) -> dict:
    """Add an internal note to the ticket opened for an inbound email.

    Args:
        message_id: The inbound email's message ID.
        note: What was done, one or two sentences.

    Returns:
        {"status": "ok"}.
    """
    store = services.get().store
    with store.conn:
        store.conn.execute("CREATE TABLE IF NOT EXISTS ticket_notes (message_id TEXT, note TEXT)")
        store.conn.execute("INSERT INTO ticket_notes VALUES (?, ?)", (message_id, note))
    return {"status": "ok"}
