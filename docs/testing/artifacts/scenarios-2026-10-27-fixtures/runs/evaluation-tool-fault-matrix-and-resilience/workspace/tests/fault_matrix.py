"""The fault matrix: every tool x {error, slow, empty, corrupt}, one fault per case, plus a no-fault twin.

Injection bypasses the tool body, so under a fault on book_flight nothing is stored, and under a
fault on send_confirmation the booking exists but no email does.
"""
from __future__ import annotations

from tests.resilience_score import SENTINEL, Case, Fault

ERROR = {"error_code": 503, "error_message": "Service Unavailable"}

INJECTED = {
    "search_flights": {
        "error": ERROR, "slow": ERROR,
        "empty": {"status": "ok", "flights": []},
        "corrupt": {"status": "ok", "flights": [{"flight_id": "AF1681", "departs": SENTINEL,
                                                 "arrives": "15:05", "price_eur": SENTINEL}]},
    },
    "book_flight": {
        "error": ERROR, "slow": ERROR,
        "empty": {"status": "booked"},                       # no booking_id
        "corrupt": {"status": "booked", "booking_id": SENTINEL},
    },
    "send_confirmation": {
        "error": ERROR, "slow": ERROR,
        "empty": {"status": "queued"},
        "corrupt": {"status": "sent", "booking_id": SENTINEL},   # contradicts the booking just made
    },
}

# (stored bookings, sent emails) the case allows under a fault on that tool
EFFECTS = {"search_flights": ((0, 0), (0, 0)), "book_flight": ((0, 0), (0, 0)),
           "send_confirmation": ((1, 1), (0, 0))}

TWIN = Case("twin", None, bookings=(1, 1), emails=(1, 1), must_disclose=False)


def matrix() -> list[Case]:
    cases = []
    for tool, kinds in INJECTED.items():
        bookings, emails = EFFECTS[tool]
        for kind, injected in kinds.items():
            cases.append(Case(f"{tool}:{kind}", Fault(tool, kind, injected), bookings, emails, must_disclose=True))
    return cases
