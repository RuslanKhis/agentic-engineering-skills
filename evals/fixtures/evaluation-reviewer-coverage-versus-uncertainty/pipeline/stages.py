"""Writer, review and export stages."""
from __future__ import annotations

import json

from pipeline import prompts, schemas
from pipeline.coverage_check import review_findings
from pipeline.model import ChatModel
from pipeline.sources import Span, representation


class StageFailed(Exception):
    def __init__(self, stage: str, errors: list[str]):
        super().__init__(f"{stage}: " + "; ".join(errors))
        self.stage = stage
        self.errors = errors


def run_writer(model: ChatModel, case: dict, spans: list[Span], max_chars: int) -> tuple[dict, dict]:
    instruction = prompts.WRITER_INSTRUCTION.format(address=case["address"], proposal=case["proposal"],
                                                   sources=representation(spans, max_chars))
    draft, usage = model.complete_json(instruction, schemas.DRAFT_SCHEMA, "draft")
    errors = schemas.validate_draft(draft, {s.span_id for s in spans})
    if errors:
        raise StageFailed("writer", errors)
    return draft, usage


def run_review(model: ChatModel, draft: dict, spans: list[Span], max_chars: int,
               case: dict | None = None) -> tuple[dict, dict]:
    checks = review_findings(draft, case) if case else []
    instruction = prompts.REVIEW_INSTRUCTION.format(draft=json.dumps(draft, indent=1),
                                                    sources=representation(spans, max_chars))
    if checks:
        instruction += "\nAutomatic checks found:\n" + "\n".join(f"- {c}" for c in checks)
    review, usage = model.complete_json(instruction, schemas.REVIEW_SCHEMA, "review")
    errors = schemas.validate_review(review, draft)
    if errors:
        raise StageFailed("review", errors)
    if checks:
        review["findings"] = checks + review["findings"]
        review["verdict"] = "reject"
    return review, usage


def export(case: dict, draft: dict, review: dict) -> dict:
    if review["verdict"] != "accept":
        raise StageFailed("export", ["review did not accept the draft"])
    return {"case_id": case["case_id"], "decision": draft["decision"],
            "reasons": [r["text"] for r in draft["reasons"]],
            "conditions": [c["text"] for c in draft["conditions"]],
            "gaps": draft["gaps"]}
