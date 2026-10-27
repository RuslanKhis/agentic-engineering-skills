"""Assemble the officer-facing draft from the writer's output and the upstream stage notes.

Each upstream step (retrieval, reconciliation, draft) reports the questions it could not
settle; they are all carried into the draft's gaps, prefixed with the step that raised them,
so the officer can see where each came from.
"""
from __future__ import annotations

STAGES = ("retrieval", "reconciliation", "draft")


def assemble(draft: dict, stage_notes: dict[str, list[str]]) -> dict:
    gaps = []
    for stage in STAGES:
        for note in stage_notes.get(stage, []):
            gaps.append(f"{stage}: {note}")
    return {**draft, "gaps": gaps}
