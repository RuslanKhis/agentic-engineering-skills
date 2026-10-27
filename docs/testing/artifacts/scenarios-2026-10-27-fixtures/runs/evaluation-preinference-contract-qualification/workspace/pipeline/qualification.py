"""Policy qualification route: which route and conditions a policy pack sets for a proposal."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.checkpoints import CheckpointStore
from pipeline.contract import FINDINGS_SCHEMA, check_findings
from pipeline.labels import occurrence_label
from pipeline.model import ChatModel

QUALIFICATION_VERSION = "qual-v2"
# Size guard on the rendered passages. A pack over the limit is refused before any send;
# it is never cut, because a cut silently drops continuations and footnotes.
MAX_PACK_CHARS = 4000


class PackTooLarge(ValueError):
    pass


INSTRUCTION = """\
You are qualifying planning policy for an officer. Using only the passages below, state each
finding about the route and conditions that apply, and whether the passages support it
(supported, unsupported or unresolved). Note any qualification that limits a finding.

Every passage starts with its label in square brackets. Each finding must list in "labels" the
exact labels of the passages it relies on. If a passage you cite continues on another passage,
or depends on a footnote or table header, cite those passages too or give their labels in
"qualifications". Cite every passage that bears on the question. A passage marked as having no
text is unresolved evidence: do not draw a conclusion from it.

Question: {question}

Passages:
{passages}
"""


def render_pack(pack: dict, max_chars: int = MAX_PACK_CHARS) -> str:
    by_id = {p["id"]: p for p in pack["passages"]}
    lines = []
    for pid in pack["selected_pack"]:
        p = by_id[pid]
        if p["text"] is None:
            lines.append(f"[{occurrence_label(p)}] (no text available for this {p['kind']})")
            continue
        lines.append(f"[{occurrence_label(p)}] {p['text']}")
    text = "\n".join(lines)
    if len(text) > max_chars:
        raise PackTooLarge(f"rendered pack is {len(text)} characters; limit {max_chars}")
    return text


def preflight(pack: dict) -> list[str]:
    """Problems that make the pack impossible to qualify; checked before any paid send."""
    selected = set(pack["selected_pack"])
    known = {p["id"] for p in pack["passages"]}
    errors = [f"required passage {r} is not in the selected pack" for r in pack["required"]
              if r not in selected]
    for p in pack["passages"]:
        if p["id"] in selected:
            errors += [f"{p['id']} requires {r}, which is not in the selected pack"
                       for r in p.get("requires", []) if r not in selected or r not in known]
    return errors


def load_pack(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_qualification(pack: dict, model: ChatModel, store: CheckpointStore, run_id: str) -> dict:
    problems = preflight(pack)
    if problems:
        raise ValueError("; ".join(problems))
    instruction = INSTRUCTION.format(question=pack["question"], passages=render_pack(pack))
    result, usage = model.complete_json(instruction, FINDINGS_SCHEMA, "findings")
    errors = check_findings(result, pack, strict=True)
    store.save(run_id, "qualification", result,
               {"usage": usage, "version": QUALIFICATION_VERSION, "errors": errors})
    if errors:
        raise ValueError("; ".join(errors))
    return result
