"""Booking changes through the provider API."""
from __future__ import annotations

import time
import uuid
from typing import Callable

# send(payload) -> (status_code, body); raises TimeoutError when the provider does not answer.
Sender = Callable[[dict], tuple[int, dict]]

_send: Sender | None = None
ATTEMPTS = 3


def set_sender(send: Sender) -> None:
    global _send
    _send = send


def change_booking(booking_ref: str, changes: dict, tool_context) -> dict:
    """Change a booking (dates, seat or hotel nights) after the traveller has confirmed.

    Args:
        booking_ref: The provider's booking reference, e.g. "TW-5HQ2KX".
        changes: The new values, e.g. {"return_date": "2026-11-14"}.

    Returns:
        {"status": "changed", "confirmation": ...} or {"status": "failed", "message": ...}.
    """
    payload = {"booking_ref": booking_ref, "changes": changes,
               "tenant_id": tool_context.state.get("tenant_id")}
    for attempt in range(ATTEMPTS):
        payload["operation_id"] = str(uuid.uuid4())
        try:
            status, body = _send(payload)
        except TimeoutError:
            time.sleep(2)
            continue
        if status == 200:
            return {"status": "changed", "confirmation": body.get("confirmation")}
        return {"status": "failed", "message": body.get("error", f"provider returned {status}")}
    return {"status": "failed", "message": "the booking system did not answer"}
