"""Tools for the research agent. No google.adk imports."""
from __future__ import annotations

import uuid

REPORTS = {
    "rpt-eu-bikes-2026": {"title": "EU e-bike market 2026", "price_eur": 1900},
    "rpt-outdoor-retail-q3": {"title": "Outdoor retail Q3 benchmark", "price_eur": 850},
}
REQUESTS: list[dict] = []


def search_reports(topic: str) -> dict:
    """Search the catalogue of paid analyst reports by topic keywords."""
    words = topic.lower().split()
    hits = [{"report_id": k, **v} for k, v in REPORTS.items() if any(w in v["title"].lower() for w in words)]
    return {"status": "ok", "reports": hits}


def submit_procurement_request(report_id: str, justification: str) -> dict:
    """Open a procurement request to buy one paid report. Needs the user's approval."""
    if report_id not in REPORTS:
        return {"status": "error", "message": f"Unknown report {report_id}."}
    request = {"request_id": f"pr-{uuid.uuid4().hex[:8]}", "report_id": report_id,
               "justification": justification, "amount_eur": REPORTS[report_id]["price_eur"]}
    REQUESTS.append(request)
    return {"status": "submitted", **request}
