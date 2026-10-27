"""Tools for the travel desk agent; no google.adk imports."""
from __future__ import annotations

POLICY = {
    "4.1": "Economy class for flights under six hours; premium economy above six hours.",
    "4.3": "Rail is preferred to air for journeys under four hours.",
    "6.2": "Hotels up to GBP 180 per night in London and GBP 140 elsewhere.",
}


def search_travel_policy(question: str) -> dict:
    """Find travel-policy sections that mention words from the question."""
    words = {w.lower().strip("?.,") for w in question.split() if len(w) > 3}
    hits = [{"section": k, "text": v} for k, v in POLICY.items() if words & {w.lower().strip(".,;") for w in v.split()}]
    return {"status": "ok", "sections": hits}


def draft_booking_request(traveller_name: str, route: str, depart: str, return_date: str,
                          passport_expiry: str) -> dict:
    """Draft a booking request for the travel team to approve. Books nothing."""
    return {"status": "drafted", "request": {"traveller": traveller_name, "route": route, "depart": depart,
                                             "return": return_date, "passport_expiry": passport_expiry}}
