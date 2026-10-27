"""Carry a case on from the stages already saved in the checkpoint store.

Used by the served route so a case interrupted after a paid stage does not pay
for that stage again. A stage that already has a checkpoint is loaded instead of
being run.
"""
from __future__ import annotations

from pathlib import Path

from pipeline import stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.constraints import site_constraints
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies

STAGES = ("source", "constraints", "writer", "review", "export")


def resume_case(case_dir: Path, run_id: str, settings: Settings, writer: ChatModel, reviewer: ChatModel,
                store: CheckpointStore) -> dict:
    case = load_case(case_dir)
    spans = case_spans(case, load_policies())
    results: dict[str, dict] = {}

    def saved(stage: str) -> dict | None:
        record = store.load(run_id, stage)
        return record["payload"] if record else None

    results["source"] = saved("source") or {"span_ids": [s.span_id for s in spans]}
    results["constraints"] = saved("constraints") or site_constraints(case["address"])
    if saved("constraints") is None:
        store.save(run_id, "constraints", results["constraints"], {})

    draft = saved("writer")
    if draft is None:
        draft, usage = stages.run_writer(writer, case, spans, settings.max_source_chars)
        store.save(run_id, "writer", draft, {"usage": usage})
    results["writer"] = draft

    review = saved("review")
    if review is None:
        review, usage = stages.run_review(reviewer, draft, spans, settings.max_source_chars)
        store.save(run_id, "review", review, {"usage": usage})
    results["review"] = review

    return publish(case, run_id, store)


def publish(case: dict, run_id: str, store: CheckpointStore) -> dict:
    """Export the newest draft for the case with its saved review."""
    draft = latest_draft(case["case_id"]) or store.load(run_id, "writer")["payload"]
    review = store.load(run_id, "review")["payload"]
    result = stages.export(case, draft, review)
    result["constraints"] = store.load(run_id, "constraints")["payload"]["constraints"]
    store.save(run_id, "export", result, {})
    return result


def latest_draft(case_id: str, drafts_dir: Path = Path("drafts")) -> dict | None:
    """Officers can amend a draft in the case-management screen; amendments land in drafts/."""
    folder = drafts_dir / case_id
    revisions = sorted(folder.glob("r*.json")) if folder.is_dir() else []
    if not revisions:
        return None
    import json
    return json.loads(revisions[-1].read_text(encoding="utf-8"))["draft"]
