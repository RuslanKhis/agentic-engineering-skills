"""Reading inbound support emails and sending replies."""
from __future__ import annotations

from app import services


def fetch_email(message_id: str) -> dict:
    """Read one inbound support email by its message ID.

    Returns:
        {"status": "ok", "from": ..., "subject": ..., "body": ...}.
    """
    msg = services.get().mail.get_message(message_id)
    return {"status": "ok", "from": msg.get("from", ""), "subject": msg.get("subject", ""),
            "body": msg.get("body", "")}


def send_email(to: str, subject: str, body: str) -> dict:
    """Send an email reply.

    Args:
        to: Recipient email address.
        subject: Subject line.
        body: Plain-text body.

    Returns:
        {"status": "sent", "id": ...}.
    """
    result = services.get().mail.send(to, subject, body)
    return {"status": "sent", "id": result.get("id")}
