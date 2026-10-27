"""Assemble the officer-facing draft from the writer's output and the upstream stage notes.

Each upstream step (retrieval, reconciliation, draft) reports the questions it could not
settle; they are all carried into the draft's gaps, prefixed with the step that raised them,
so the officer can see where each came from.
"""
from __future__ import annotations

from pipeline.safeguards import dedupe_notes


def assemble(draft: dict, stage_notes: dict[str, list[str]]) -> dict:
    # A note repeated by later steps is kept once, labelled with the step that raised it first.
    return {**draft, "gaps": dedupe_notes(stage_notes)}
