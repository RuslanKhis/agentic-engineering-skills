"""Small corrections after a writer warning, without re-running the whole case.

A writer result that validates but carries warnings (pipeline/warnings.py) goes back to the
writer once with the warnings listed; the corrected draft is saved in a new run and may change
only the warned quotes. The saved review is carried into that run with its verdict and findings
intact; it is not an acceptance of the new draft.
"""
from __future__ import annotations

import json
import shutil

from pipeline import schemas
from pipeline.checkpoints import CheckpointStore
from pipeline.model import ChatModel
from pipeline.sources import Span, representation
from pipeline.stages import StageFailed
from pipeline.warnings import draft_warnings

CORRECTION_INSTRUCTION = """\
The draft planning decision below passed validation but has warnings. Fix only the warnings, by
correcting the quoted text. Leave the decision, reasons, conditions, citations, conflicts and
gaps otherwise exactly as they are. Return the full draft as JSON matching the schema.

Warnings:
{warnings}

Draft:
{draft}

Sources:
{sources}
"""


def scope_errors(old: dict, new: dict, warnings: list[dict]) -> list[str]:
    """A warning-only correction may change the quote text of warned citations and nothing else."""
    errors = [f"{key} changed" for key in ("decision", "reasons", "conditions", "conflicts", "gaps")
              if old[key] != new[key]]
    warned = {w["span_id"] for w in warnings}
    old_cits, new_cits = old["citations"], new["citations"]
    if [c["span_id"] for c in old_cits] != [c["span_id"] for c in new_cits]:
        errors.append("citations added, dropped or reordered")
    else:
        errors += [f"citation {o['span_id']} changed without a warning"
                   for o, n in zip(old_cits, new_cits) if o != n and o["span_id"] not in warned]
    return errors


def correct_warnings(run_id: str, new_run_id: str, store: CheckpointStore, writer: ChatModel,
                     spans: list[Span], max_chars: int = 60_000) -> dict:
    """Write the corrected draft to a new run; the original run is left as it is."""
    if new_run_id == run_id:
        raise ValueError("the corrected draft goes to a new run directory")
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
    if not errors:
        errors = scope_errors(draft, corrected, warnings)
    if errors:
        raise StageFailed("correction", errors)
    source = store.root / run_id / "source.json"
    if source.exists():
        (store.root / new_run_id).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, store.root / new_run_id / "source.json")
    store.save(new_run_id, "writer", corrected,
               {"attempt": "a2-correction", "draft_revision": "r2",
                "corrects": {"run_id": run_id, "draft_revision": record["meta"].get("draft_revision"),
                             "attempt": record["meta"].get("attempt")},
                "corrected_warnings": warnings, "usage": usage,
                "warnings": draft_warnings(corrected, spans)})
    return corrected


def repair_review(run_id: str, new_run_id: str, store: CheckpointStore, spans: list[Span]) -> dict:
    """Carry the saved review into the new run unchanged: verdict, claims and every finding stay.

    Findings about a quote the correction fixed are listed in meta as resolved, not deleted. The
    review still describes draft r1; r2 needs its own review before export.
    """
    record = store.load(run_id, "review")
    review = record["payload"]
    corrected = store.load(new_run_id, "writer")
    still_warned = {w["span_id"] for w in draft_warnings(corrected["payload"], spans)}
    fixed = {w["span_id"] for w in corrected["meta"]["corrected_warnings"]} - still_warned
    resolved = [f for f in review["findings"]
                if "verbatim" in f.lower() and any(span_id in f for span_id in fixed)]
    store.save(new_run_id, "review", review,
               {**record["meta"], "carried_from": {"run_id": run_id, "draft_revision": "r1"},
                "resolved_findings": resolved,
                "needs_fresh_review_of": "r2"})
    return review
