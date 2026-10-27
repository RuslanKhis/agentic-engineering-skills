"""Small corrections after a writer warning, without re-running the whole case.

A writer result that validates but carries warnings (pipeline/warnings.py) goes back to the
writer once with the warnings listed; the corrected draft is saved in a new run directory
(runs/ is evidence and is never edited). The saved review is carried into that run with only
the findings about the corrected warnings removed; the verdict is not changed here.
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


def _changes_beyond_quotes(draft: dict, corrected: dict) -> list[str]:
    """A warning correction may only touch citation quotes; anything else changes the decision."""
    problems = []
    for key in ("decision", "reasons", "conditions", "conflicts", "gaps"):
        if draft.get(key) != corrected.get(key):
            problems.append(f"correction changed {key}")
    old = {c["span_id"] for c in draft.get("citations", [])}
    new = {c["span_id"] for c in corrected.get("citations", [])}
    if old != new:
        problems.append(f"correction changed the cited spans: {sorted(old ^ new)}")
    return problems


def correct_warnings(run_id: str, new_run_id: str, store: CheckpointStore, writer: ChatModel,
                     spans: list[Span], max_chars: int = 60_000) -> dict:
    """Correct the writer warnings into a new run directory; the original run is never written."""
    if new_run_id == run_id:
        raise ValueError("the corrected draft must go to a new run directory, not over the original")
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
    errors = list(errors or []) + _changes_beyond_quotes(draft, corrected)
    if errors:
        raise StageFailed("correction", errors)
    meta = {k: v for k, v in record["meta"].items() if k != "raw_response"}
    store.save(new_run_id, "writer", corrected,
               {**meta, "corrected_from": run_id, "usage": usage,
                "warnings": draft_warnings(corrected, spans),
                "warnings_corrected": warnings})
    return corrected


def repair_review(run_id: str, new_run_id: str, store: CheckpointStore) -> dict:
    """Carry the saved review into the new run, dropping only the findings about corrected warnings.

    The verdict, the claims and every other finding are kept as the reviewer gave them. The
    reviewer has not seen the corrected draft, so the record says so.
    """
    if new_run_id == run_id:
        raise ValueError("the repaired review must go to a new run directory, not over the original")
    record = store.load(run_id, "review")
    warned = {w["span_id"] for w in store.load(run_id, "writer")["meta"].get("warnings", [])}
    review = json.loads(json.dumps(record["payload"]))
    dropped = [f for f in review["findings"] if "verbatim" in f.lower() and any(s in f for s in warned)]
    review["findings"] = [f for f in review["findings"] if f not in dropped]
    store.save(new_run_id, "review", review,
               {**record["meta"], "derived_from": run_id, "reviewer_rerun": False,
                "findings_dropped": dropped})
    return review
