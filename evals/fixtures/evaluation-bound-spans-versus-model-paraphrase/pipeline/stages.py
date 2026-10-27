"""Writer, review and export stages."""
from __future__ import annotations

import json

from pipeline import prompts, schemas
from pipeline.citations import quote_matches
from pipeline.model import ChatModel
from pipeline.sources import Span, representation
from pipeline.support import reason_supported


class StageFailed(Exception):
    def __init__(self, stage: str, errors: list[str]):
        super().__init__(f"{stage}: " + "; ".join(errors))
        self.stage = stage
        self.errors = errors


def check_citations(draft: dict, spans: list[Span]) -> list[str]:
    errors = []
    for cit in draft["citations"]:
        if not quote_matches(cit["quote"], cit.get("span_ids") or [cit["span_id"]], spans):
            errors.append(f"quote not found in {cit['span_id']}: {cit['quote'][:60]!r}")
    for reason in draft["reasons"]:
        if not reason_supported(reason, spans):
            errors.append(f"reason {reason['id']} is not supported")
    return errors


def run_writer(model: ChatModel, case: dict, spans: list[Span], max_chars: int) -> tuple[dict, dict]:
    instruction = prompts.WRITER_INSTRUCTION.format(address=case["address"], proposal=case["proposal"],
                                                   sources=representation(spans, max_chars))
    draft, usage = model.complete_json(instruction, schemas.DRAFT_SCHEMA, "draft")
    errors = schemas.validate_draft(draft, {s.span_id for s in spans}) or check_citations(draft, spans)
    if errors:
        raise StageFailed("writer", errors)
    return draft, usage


def run_review(model: ChatModel, draft: dict, spans: list[Span], max_chars: int) -> tuple[dict, dict]:
    instruction = prompts.REVIEW_INSTRUCTION.format(draft=json.dumps(draft, indent=1),
                                                    sources=representation(spans, max_chars))
    review, usage = model.complete_json(instruction, schemas.REVIEW_SCHEMA, "review")
    errors = schemas.validate_review(review, draft)
    if errors:
        raise StageFailed("review", errors)
    return review, usage


def export(case: dict, draft: dict, review: dict) -> dict:
    if review["verdict"] != "accept":
        raise StageFailed("export", ["review did not accept the draft"])
    return {"case_id": case["case_id"], "decision": draft["decision"],
            "reasons": [r["text"] for r in draft["reasons"]],
            "conditions": [c["text"] for c in draft["conditions"]],
            "gaps": draft["gaps"]}
