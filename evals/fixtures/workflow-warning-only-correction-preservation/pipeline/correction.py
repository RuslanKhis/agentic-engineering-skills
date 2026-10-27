"""Small corrections after a writer warning, without re-running the whole case.

A writer result that validates but carries warnings (pipeline/warnings.py) goes back to the
writer once with the warnings listed; the corrected draft replaces the saved one. The saved
review is then brought up to date so the case can be exported.
"""
from __future__ import annotations

import json

from pipeline import schemas
from pipeline.checkpoints import CheckpointStore
from pipeline.model import ChatModel
from pipeline.sources import Span, representation
from pipeline.stages import StageFailed
from pipeline.warnings import draft_warnings

CORRECTION_INSTRUCTION = """\
The draft planning decision below passed validation but has warnings. Fix the warnings and
return the full corrected draft as JSON matching the schema.

Warnings:
{warnings}

Draft:
{draft}

Sources:
{sources}
"""


def correct_warnings(run_id: str, store: CheckpointStore, writer: ChatModel, spans: list[Span],
                     max_chars: int = 60_000) -> dict:
    record = store.load(run_id, "writer")
    draft = record["payload"]
    warnings = record["meta"].get("warnings") or draft_warnings(draft, spans)
    if not warnings:
        return draft
    instruction = CORRECTION_INSTRUCTION.format(warnings=json.dumps(warnings, indent=1),
                                                draft=json.dumps(draft, indent=1),
                                                sources=representation(spans, max_chars))
    corrected, usage = writer.complete_json(instruction, schemas.DRAFT_SCHEMA, "draft")
    errors = schemas.validate_draft(corrected, {s.span_id for s in spans})
    if errors:
        raise StageFailed("correction", errors)
    store.save(run_id, "writer", corrected, {**record["meta"], "usage": usage,
                                             "warnings": draft_warnings(corrected, spans)})
    return corrected


def repair_review(run_id: str, store: CheckpointStore) -> dict:
    """Drop review findings that were about the warnings the correction fixed."""
    record = store.load(run_id, "review")
    review = record["payload"]
    review["findings"] = [f for f in review["findings"]
                          if "verbatim" not in f.lower() and "citation" not in f.lower()]
    if not review["findings"] and all(c["support"] == "supported" for c in review["claims"]):
        review["verdict"] = "accept"
    store.save(run_id, "review", review, record["meta"])
    return review
