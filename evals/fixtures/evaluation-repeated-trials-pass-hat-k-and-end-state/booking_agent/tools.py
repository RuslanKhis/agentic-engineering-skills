"""Booking tools. backend is set by agent.py or the tests."""
from __future__ import annotations

from booking_agent.backend import Backend

backend = Backend()


def search_slots(clinic: str, day: str) -> dict:
    """Free appointment slots at a clinic ("Harbour" or "Quay") on a day (YYYY-MM-DD)."""
    return {"status": "ok", "slots": [{"slot_id": k, **v} for k, v in backend.slots.items()
                                      if v["clinic"] == clinic and v["day"] == day and v["free"]]}


def get_my_bookings(tool_context) -> dict:
    """The signed-in patient's current bookings."""
    return {"status": "ok", "bookings": [{"booking_id": k, **v} for k, v in backend.bookings.items()
                                         if v["patient_id"] == tool_context.user_id and v["status"] == "booked"]}


def book_slot(slot_id: str, tool_context) -> dict:
    """Book a free slot for the signed-in patient."""
    try:
        return {"status": "booked", **backend.book(slot_id, tool_context.user_id)}
    except (KeyError, ValueError) as exc:
        return {"status": "error", "message": str(exc)}


def cancel_booking(booking_id: str, tool_context) -> dict:
    """Cancel one of the signed-in patient's bookings."""
    booking = backend.bookings.get(booking_id)
    if booking is None or booking["patient_id"] != tool_context.user_id:
        return {"status": "error", "message": "no such booking"}
    backend.cancel(booking_id)
    return {"status": "cancelled", "booking_id": booking_id}
