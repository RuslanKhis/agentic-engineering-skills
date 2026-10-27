"""The question route: select a pack, group it into units, draft, review.

    extract (offline job, records.jsonl)
      -> select_pack   retriever v1.3 (BM25 over records, top 40, score order)
      -> group         review_app.grouping (units)
      -> write         LlmAgent "writer", gemini-3.5-flash, prompts/writer.md v7
      -> review        LlmAgent "reviewer", gemini-3.5-flash, prompts/reviewer.md v4

Every stage's output is saved through review_app.storage.EnvelopeStore with the
producer version and the IDs of the envelopes it read. The ADK agents live in
review_app/agents.py (not importable without google-adk).
"""
from __future__ import annotations

from review_app.grouping import GROUPER_VERSION, group_for_pack


def group_stage(run_id: str, records: dict, pack_envelope: dict, pack_envelope_id: str) -> dict:
    units = group_for_pack(records, pack_envelope["payload"]["record_ids"])
    return {"run_id": run_id, "stage": "group", "producer": {"grouper": GROUPER_VERSION},
            "inputs": [pack_envelope_id], "payload": {"units": units}}
