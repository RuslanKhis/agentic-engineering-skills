"""Policy qualification route: which route and conditions a policy pack sets for a proposal."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.checkpoints import CheckpointStore
from pipeline.contract import FINDINGS_SCHEMA, check_findings
from pipeline.labels import occurrence_label
from pipeline.model import ChatModel

QUALIFICATION_VERSION = "qual-v2"
# Keeps the qualification prompt small; the pack is only policy text.
MAX_PACK_CHARS = 600

INSTRUCTION = """\
You are qualifying planning policy for an officer. Using only the passages below, state each
finding about the route and conditions that apply, and whether the passages support it
(supported, unsupported or unresolved). Note any qualification that limits a finding.

Question: {question}

Passages:
{passages}
"""


def render_pack(pack: dict) -> str:
    by_id = {p["id"]: p for p in pack["passages"]}
    lines = []
    for pid in pack["selected_pack"]:
        p = by_id[pid]
        if p["text"] is None:
            continue
        lines.append(f"[{occurrence_label(p)}] {p['text']}")
    return "\n".join(lines)[:MAX_PACK_CHARS]


def load_pack(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_qualification(pack: dict, model: ChatModel, store: CheckpointStore, run_id: str) -> dict:
    instruction = INSTRUCTION.format(question=pack["question"], passages=render_pack(pack))
    result, usage = model.complete_json(instruction, FINDINGS_SCHEMA, "findings")
    errors = check_findings(result, pack)
    store.save(run_id, "qualification", result,
               {"usage": usage, "version": QUALIFICATION_VERSION, "errors": errors})
    if errors:
        raise ValueError("; ".join(errors))
    return result
