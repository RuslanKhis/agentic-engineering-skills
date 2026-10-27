"""Client for the flight API. transport(method, path, json) -> (status, body)."""
from __future__ import annotations


class FlightApiError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(f"{status}: {message}")
        self.status = status


class FlightApi:
    def __init__(self, transport):
        self.transport = transport

    def search(self, origin: str, destination: str, date: str) -> list[dict]:
        status, body = self.transport("GET", "/flights", {"from": origin, "to": destination, "date": date})
        if status != 200:
            raise FlightApiError(status, body.get("error", ""))
        return body["flights"]

    def book(self, flight_id: str, passenger: str, idempotency_key: str) -> dict:
        status, body = self.transport("POST", "/bookings", {"flight_id": flight_id, "passenger": passenger,
                                                            "idempotency_key": idempotency_key})
        if status not in (200, 201):
            raise FlightApiError(status, body.get("error", ""))
        return body
