"""Resume a run from its saved writer checkpoint: review and export only."""
from __future__ import annotations

from pipeline import stages
from pipeline.checkpoints import CheckpointStore
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies


def resume_review(case_dir, previous_run_id: str, run_id: str, reviewer: ChatModel, store: CheckpointStore,
                  max_chars: int) -> dict:
    case = load_case(case_dir)
    spans = case_spans(case, load_policies())
    draft = store.load(previous_run_id, "writer")["payload"]
    review, usage = stages.run_review(reviewer, draft, spans, max_chars)
    store.save(run_id, "review", review, {"usage": usage, "continues": previous_run_id})
    result = stages.export(case, draft, review)
    store.save(run_id, "export", result, {"continues": previous_run_id})
    return result
