"""Booking tools. No google.adk imports, so the unit tests load them without the SDK."""
from __future__ import annotations

from dataclasses import dataclass, field
import itertools

TRADES = {"plumber", "electrician", "locksmith"}


@dataclass
class Bookings:
    visits: dict = field(default_factory=dict)
    _ids: itertools.count = field(default_factory=lambda: itertools.count(1001))

    def book(self, customer_id: str, trade: str, address: str, day: str) -> dict:
        visit_id = f"V{next(self._ids)}"
        self.visits[visit_id] = {"customer_id": customer_id, "trade": trade, "address": address, "day": day}
        return {"visit_id": visit_id, **self.visits[visit_id]}


BOOKINGS = Bookings()


def book_visit(trade: str, address: str, day: str, tool_context) -> dict:
    """Book a tradesperson visit for the signed-in customer.

    Args:
        trade: One of plumber, electrician, locksmith.
        address: The full street address for the visit, confirmed with the customer.
        day: Requested day as YYYY-MM-DD.
    """
    if trade not in TRADES:
        return {"status": "error", "message": f"We book {', '.join(sorted(TRADES))} visits."}
    if not address.strip():
        return {"status": "error", "message": "Ask the customer for the visit address."}
    return {"status": "booked", **BOOKINGS.book(tool_context.user_id, trade, address.strip(), day)}


def my_visits(tool_context) -> dict:
    """List the signed-in customer's booked visits."""
    return {"status": "ok", "visits": [dict(visit_id=k, **v) for k, v in BOOKINGS.visits.items()
                                       if v["customer_id"] == tool_context.user_id]}
