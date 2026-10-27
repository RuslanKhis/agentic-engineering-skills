"""Support tickets from the helpdesk table."""
from __future__ import annotations

from app import services


def read_ticket(ticket_id: str) -> dict:
    """Read a support ticket: the customer's message and the order it concerns.

    Args:
        ticket_id: The ticket ID, e.g. "T-5521".

    Returns:
        {"status": "ok", "ticket": {ticket_id, customer_id, order_id, subject, body}} or {"status": "not_found"}.
    """
    store = services.get().store
    store.conn.execute("CREATE TABLE IF NOT EXISTS tickets (ticket_id TEXT PRIMARY KEY, customer_id TEXT, "
                       "order_id TEXT, subject TEXT, body TEXT)")
    row = store.conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    return {"status": "ok", "ticket": dict(row)} if row else {"status": "not_found"}
