"""The writer's and reviewer's output contracts, checked in code (stdlib only)."""
from __future__ import annotations

DECISIONS = ("approve", "approve_with_conditions", "refuse")
SUPPORT = ("supported", "unsupported", "contradicted")
SCHEMA_VERSION = "draft-v7"

# Standard planning conditions; the writer picks one id per condition and the server owns the text.
# draft-v6 put the text (with a line break) in the enum, and the gateway rejected it with a 400.
CONDITION_TEMPLATES = {
    "COND-PLANS": "The development shall be carried out in accordance with the approved plans.\nReason: for the avoidance of doubt.",
    "COND-GLAZING": "The first-floor side window shall be obscure-glazed and non-opening below 1.7 m.\nReason: to protect neighbouring privacy.",
    "COND-AMS": "No work shall start until an arboricultural method statement has been approved.\nReason: to protect the tree under Policy ENV3.",
}

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
                       "required": ["id", "template_id", "reason_id"],
                       "properties": {"id": {"type": "string"},
                                      "template_id": {"type": "string", "enum": list(CONDITION_TEMPLATES)},
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


def missing_continuations(cited: list[str], spans: list) -> list[str]:
    """Span ids a citation set leaves out although the cited sentence runs on into them.

    Source lines wrap mid-sentence. A line that does not end a sentence and is followed by a line
    starting in lower case continues into it; citing only the first line is the batch 2 failure
    (LP-H4@2024:p31:7 without :8). Spans themselves are never changed.
    """
    by_id = {s.span_id: s for s in spans}
    have = set(cited)
    missing: list[str] = []
    for span_id in cited:
        span = by_id.get(span_id)
        while span is not None and span.text.rstrip()[-1:] not in ".?!:":
            nxt = next((x for x in spans if (x.doc_id, x.version, x.page) == (span.doc_id, span.version, span.page)
                        and x.line > span.line), None)
            if nxt is None or not nxt.text[:1].islower():
                break
            if nxt.span_id not in have and nxt.span_id not in missing:
                missing.append(nxt.span_id)
            span = nxt
    return missing


def validate_draft(draft: object, known_spans: set[str], spans: list | None = None) -> list[str]:
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
        if spans is not None:
            for span_id in missing_continuations(reason.get("citations", []), spans):
                errors.append(f"reason {reason.get('id')} cites a sentence that continues in {span_id}")
    for cond in draft["conditions"]:
        if cond.get("reason_id") not in reason_ids:
            errors.append(f"condition {cond.get('id')} has no reason")
        if cond.get("template_id") not in CONDITION_TEMPLATES:
            errors.append(f"condition {cond.get('id')} uses an unknown template")
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
