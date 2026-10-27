"""Helpdesk tools. No google.adk imports so the unit tests run without the SDK."""
from __future__ import annotations

import itertools

KB = [
    {"id": "IT-012", "title": "Connect to the VPN", "body": "Install GlobalConnect from the Software Centre and sign in with your staff account."},
    {"id": "IT-031", "title": "Laptop will not start", "body": "Hold the power button for 15 seconds, then connect the charger for 10 minutes."},
    {"id": "IT-044", "title": "Locked account", "body": "Accounts unlock after 30 minutes; the service desk can unlock one sooner after a call-back."},
]

TICKETS: dict[str, dict] = {}
_ids = itertools.count(5001)


def search_kb(query: str) -> dict:
    """Search IT knowledge-base articles by keywords; returns up to three articles."""
    words = {w for w in query.lower().split() if len(w) > 2}
    hits = [a for a in KB if words & set((a["title"] + " " + a["body"]).lower().split())]
    return {"status": "ok", "articles": hits[:3]}


def my_tickets(tool_context) -> dict:
    """List the caller's open tickets."""
    return {"status": "ok", "tickets": [dict(id=k, **v) for k, v in TICKETS.items()
                                        if v["staff_id"] == tool_context.user_id and v["state"] == "open"]}


def raise_ticket(summary: str, category: str, tool_context) -> dict:
    """Raise a ticket for the caller.

    Args:
        summary: One or two sentences describing the problem.
        category: One of hardware, account, network, software.
    """
    if category not in {"hardware", "account", "network", "software"}:
        return {"status": "error", "message": "category must be hardware, account, network or software"}
    ticket_id = f"INC{next(_ids)}"
    TICKETS[ticket_id] = {"staff_id": tool_context.user_id, "summary": summary, "category": category,
                          "state": "open"}
    return {"status": "raised", "id": ticket_id}
