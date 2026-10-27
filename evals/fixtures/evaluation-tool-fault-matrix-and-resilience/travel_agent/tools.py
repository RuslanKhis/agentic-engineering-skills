"""Tools for the travel agent. The API client is set by agent.py or the tests."""
from __future__ import annotations

from travel_agent.flight_api import FlightApi, FlightApiError

api: FlightApi | None = None
mailer = None


def search_flights(origin: str, destination: str, date: str) -> dict:
    """Find flights. origin and destination are IATA codes (e.g. "LHR"); date is YYYY-MM-DD.

    Returns {"status": "ok", "flights": [{"flight_id", "departs", "arrives", "price_eur"}]}
    or {"status": "error", "message": ...}.
    """
    try:
        return {"status": "ok", "flights": api.search(origin, destination, date)}
    except FlightApiError as exc:
        return {"status": "error", "message": str(exc)}


def book_flight(flight_id: str, passenger: str, idempotency_key: str) -> dict:
    """Book one seat. Pass the same idempotency_key when retrying the same booking.

    Returns {"status": "booked", "booking_id": ...} or {"status": "error", "message": ...}.
    """
    try:
        body = api.book(flight_id, passenger, idempotency_key)
    except FlightApiError as exc:
        return {"status": "error", "message": str(exc)}
    return {"status": "booked", "booking_id": body["booking_id"]}


def send_confirmation(booking_id: str, email: str) -> dict:
    """Email the booking confirmation to the traveller."""
    mailer.send(email, f"Booking {booking_id} confirmed")
    return {"status": "sent"}
