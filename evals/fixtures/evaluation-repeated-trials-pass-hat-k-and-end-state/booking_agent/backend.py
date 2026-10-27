"""In-memory clinic backend: slots and bookings."""
from __future__ import annotations

import copy


class Backend:
    def __init__(self, slots: dict[str, dict] | None = None):
        self.slots = slots or {
            "S-0901": {"clinic": "Harbour", "day": "2026-11-03", "time": "09:00", "free": True},
            "S-0902": {"clinic": "Harbour", "day": "2026-11-03", "time": "10:00", "free": True},
            "S-0903": {"clinic": "Quay", "day": "2026-11-04", "time": "14:00", "free": True},
            "S-0904": {"clinic": "Quay", "day": "2026-11-05", "time": "16:00", "free": False},
        }
        self.bookings: dict[str, dict] = {}

    def snapshot(self) -> dict:
        return copy.deepcopy({"slots": self.slots, "bookings": self.bookings})

    def book(self, slot_id: str, patient_id: str) -> dict:
        slot = self.slots[slot_id]
        if not slot["free"]:
            raise ValueError("slot taken")
        slot["free"] = False
        booking_id = f"B-{len(self.bookings) + 1:03d}"
        self.bookings[booking_id] = {"slot_id": slot_id, "patient_id": patient_id, "status": "booked"}
        return {"booking_id": booking_id, **self.bookings[booking_id]}

    def cancel(self, booking_id: str) -> None:
        booking = self.bookings[booking_id]
        booking["status"] = "cancelled"
        self.slots[booking["slot_id"]]["free"] = True
