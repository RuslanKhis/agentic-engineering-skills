"""The writer's and reviewer's output contracts, checked in code (stdlib only)."""
from __future__ import annotations

DECISIONS = ("approve", "approve_with_conditions", "refuse")
SUPPORT = ("supported", "unsupported", "contradicted")

DRAFT_SCHEMA = {
    "type": "object",
    "required": ["decision", "reasons", "conditions", "citations", "conflicts", "gaps"],
    "properties": {
        "decision": {"type": "string", "enum": list(DECISIONS)},
        "reasons": {"type": "array", "items": {"type": "object",
                    "required": ["id", "text", "citations"],
                    "properties": {"id": {"type": "string"}, "text": {"type": "string"},
                                   "citations": {"type": "array", "items": {"type": "string"}}}}},
        "conditions": {"type": "array", "items": {"type": "object",
                       "required": ["id", "text", "reason_id"],
                       "properties": {"id": {"type": "string"}, "text": {"type": "string"},
                                      "reason_id": {"type": "string"}}}},
        "citations": {"type": "array", "items": {"type": "object",
                      "required": ["span_id", "quote"],
                      "properties": {"span_id": {"type": "string"}, "quote": {"type": "string"}}}},
        "conflicts": {"type": "array", "items": {"type": "string"}},
        "gaps": {"type": "array", "items": {"type": "string"}},
    },
}

REVIEW_SCHEMA = {
    "type": "object",
    "required": ["verdict", "claims", "findings"],
    "properties": {
        "verdict": {"type": "string", "enum": ["accept", "reject"]},
        "claims": {"type": "array", "items": {"type": "object",
                   "required": ["reason_id", "support", "span_ids"],
                   "properties": {"reason_id": {"type": "string"},
                                  "support": {"type": "string", "enum": list(SUPPORT)},
                                  "span_ids": {"type": "array", "items": {"type": "string"}}}}},
        "findings": {"type": "array", "items": {"type": "string"}},
    },
}


def validate_draft(draft: object, known_spans: set[str]) -> list[str]:
    errors = []
    if not isinstance(draft, dict):
        return ["draft is not an object"]
    for key in DRAFT_SCHEMA["required"]:
        if key not in draft:
            errors.append(f"missing {key}")
    if errors:
        return errors
    if draft["decision"] not in DECISIONS:
        errors.append("unknown decision")
    reason_ids = {r.get("id") for r in draft["reasons"]}
    for reason in draft["reasons"]:
        for span_id in reason.get("citations", []):
            if span_id not in known_spans:
                errors.append(f"reason {reason.get('id')} cites unknown span {span_id}")
    for cond in draft["conditions"]:
        if cond.get("reason_id") not in reason_ids:
            errors.append(f"condition {cond.get('id')} has no reason")
    for cit in draft["citations"]:
        if cit.get("span_id") not in known_spans:
            errors.append(f"citation to unknown span {cit.get('span_id')}")
    return errors


def validate_review(review: object, draft: dict) -> list[str]:
    if not isinstance(review, dict):
        return ["review is not an object"]
    errors = [f"missing {k}" for k in REVIEW_SCHEMA["required"] if k not in review]
    if errors:
        return errors
    if review["verdict"] not in ("accept", "reject"):
        errors.append("unknown verdict")
    reasons = {r["id"] for r in draft["reasons"]}
    claimed = {c.get("reason_id") for c in review["claims"]}
    if claimed != reasons:
        errors.append("review does not cover every reason")
    return errors
