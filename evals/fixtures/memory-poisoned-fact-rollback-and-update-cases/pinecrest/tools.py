"""Delivery tools; no google.adk imports."""
from __future__ import annotations

SLOTS = {"2026-11-02": ["08:00-10:00", "18:00-20:00"], "2026-11-03": ["10:00-12:00"]}
ORDERS = {"PG-88120": {"customer_id": "c-311", "status": "picking", "slot": "2026-11-02 18:00-20:00"}}


def book_slot(day: str, window: str, address: str, tool_context) -> dict:
    """Book a delivery slot for the signed-in customer at the address they confirmed."""
    if window not in SLOTS.get(day, []):
        return {"status": "unavailable", "open": SLOTS.get(day, [])}
    SLOTS[day].remove(window)
    return {"status": "booked", "day": day, "window": window, "address": address,
            "customer_id": tool_context.user_id}


def order_status(order_id: str, tool_context) -> dict:
    """Status of one of the signed-in customer's orders."""
    order = ORDERS.get(order_id)
    if order is None or order["customer_id"] != tool_context.user_id:
        return {"status": "not_found"}
    return {"status": "ok", **order}
