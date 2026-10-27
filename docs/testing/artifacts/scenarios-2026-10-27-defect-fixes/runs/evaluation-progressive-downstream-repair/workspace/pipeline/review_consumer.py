"""Turns a saved review into the export decision."""
from __future__ import annotations


class ReviewRejected(Exception):
    pass


def accept_review(review: dict, draft: dict) -> None:
    """Raise unless the review accepts the draft and every claim it checked is grounded in the draft.

    A claim is grounded in the spans its own reason cites. The draft's top-level `citations` are
    the quoted subset and are not the full set of spans a reason relies on.
    """
    if review["verdict"] != "accept":
        raise ReviewRejected("review did not accept the draft")
    cited_by_reason = {r["id"]: set(r.get("citations", [])) for r in draft["reasons"]}
    for claim in review["claims"]:
        if claim["reason_id"] not in cited_by_reason:
            raise ReviewRejected(f"review checks unknown reason {claim['reason_id']}")
        if claim["support"] != "supported":
            raise ReviewRejected(f"reason {claim['reason_id']} is {claim['support']}")
        cited = cited_by_reason[claim["reason_id"]]
        stray = [s for s in claim["span_ids"] if s not in cited]
        if stray:
            raise ReviewRejected(f"review cites spans the draft does not cite: {stray}")
