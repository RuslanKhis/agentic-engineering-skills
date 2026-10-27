"""Notes on the support ticket for the email being handled."""
from __future__ import annotations

from app import services
from app.tools import guards


def add_ticket_note(message_id: str, note: str, tool_context) -> dict:
    """Add an internal note to the ticket opened for an email read in this conversation.

    Args:
        message_id: The inbound email's message ID, as read with fetch_email.
        note: What was done, one or two sentences.

    Returns:
        {"status": "ok"} or {"status": "error", "message": ...}.
    """
    if message_id not in tool_context.state.get(guards.FETCHED_IDS, []):
        return {"status": "error", "message": "Read the email with fetch_email first."}
    store = services.get().store
    with store.conn:
        store.conn.execute("CREATE TABLE IF NOT EXISTS ticket_notes (message_id TEXT, note TEXT)")
        store.conn.execute("INSERT INTO ticket_notes VALUES (?, ?)",
                           (message_id, note[:guards.MAX_NOTE_CHARS]))
    return {"status": "ok"}
