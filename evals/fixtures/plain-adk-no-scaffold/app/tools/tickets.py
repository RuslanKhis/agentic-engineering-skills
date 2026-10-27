"""Open support tickets for the signed-in customer, from the helpdesk."""
from __future__ import annotations

from app import services


def list_open_tickets(tool_context) -> dict:
    """List the signed-in customer's open support tickets, newest first.

    Returns:
        {"status": "ok", "tickets": [{"ticket_id", "subject", "opened_on", "state"}]}.
    """
    tickets = services.get().helpdesk.open_tickets(tool_context.user_id)
    return {"status": "ok", "tickets": tickets[:10]}
