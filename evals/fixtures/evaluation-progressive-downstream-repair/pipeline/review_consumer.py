"""Turns a saved review into the export decision."""
from __future__ import annotations


class ReviewRejected(Exception):
    pass


def accept_review(review: dict, draft: dict) -> None:
    """Raise unless the review accepts the draft and every claim it checked is grounded in the draft."""
    if review["verdict"] != "accept":
        raise ReviewRejected("review did not accept the draft")
    cited = {c["span_id"] for c in draft["citations"]}
    reasons = {r["id"] for r in draft["reasons"]}
    for claim in review["claims"]:
        if claim["reason_id"] not in reasons:
            raise ReviewRejected(f"review checks unknown reason {claim['reason_id']}")
        if claim["support"] != "supported":
            raise ReviewRejected(f"reason {claim['reason_id']} is {claim['support']}")
        stray = [s for s in claim["span_ids"] if s not in cited]
        if stray:
            raise ReviewRejected(f"review cites spans the draft does not cite: {stray}")
