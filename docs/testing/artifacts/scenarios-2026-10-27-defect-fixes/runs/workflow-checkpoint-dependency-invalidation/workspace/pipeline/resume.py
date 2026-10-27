"""Carry a case on from the stages already saved in the checkpoint store.

Used by the served route so a case interrupted after a paid stage does not pay
for that stage again. A saved stage is loaded only if it still qualifies: its
inputs are the ones the case has now. What each stage consumes:

    source       the case documents and the local-plan policies
    constraints  the site address and the constraint layers (not the documents, not the writer)
    writer       source, writer model, writer prompt version
    review       the effective draft (the writer's, or the officer's latest amendment), source,
                 review model, review prompt version
    export       effective draft, review, constraints (never reused; recomputed, it costs nothing)

A stale stage and everything downstream of it is run again. Retained runs are evidence and are
never edited: when anything has to be written, it goes to a new continuation run directory
(`<run-id>-c1`, `-c2`, ...) that holds copies of the qualified checkpoints and a manifest naming
the parent run and what was kept or invalidated. Diagnostics/ files are never read.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pipeline import prompts, schemas, stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.constraints import site_constraints
from pipeline.ledger import CampaignLedger
from pipeline.model import ChatModel
from pipeline.sources import Span, case_spans, load_case, load_policies, manifest
from pipeline.workflow import RESERVE_USD

STAGES = ("source", "constraints", "writer", "review", "export")
BASE_REVISION = "r1"  # the writer's own draft; officer amendments in drafts/ are r2, r3, ...
DRAFTS_DIR = Path(__file__).resolve().parent.parent / "drafts"


def resume_case(case_dir: Path, run_id: str, settings: Settings, writer: ChatModel, reviewer: ChatModel,
                store: CheckpointStore) -> dict:
    case = load_case(case_dir)
    spans = case_spans(case, load_policies())
    target = prepare_continuation(case, spans, run_id, settings, store)
    for stage in ("source", "constraints", "writer", "review"):
        carry_stage(stage, case, spans, target, settings, store, reviewer if stage == "review" else writer)
    return publish(case, target, store)


def carry_stage(stage: str, case: dict, spans: list[Span], run_id: str, settings: Settings,
                store: CheckpointStore, model: ChatModel | None = None) -> dict:
    """Return the stage result from run_id, running and saving it only if run_id has no checkpoint for it.

    run_id must be the directory prepare_continuation returned, so a checkpoint found there qualifies."""
    record = store.load(run_id, stage)
    if record:
        return record["payload"]
    meta: dict = {}
    if stage == "source":
        payload, meta = {"span_ids": [s.span_id for s in spans]}, {"manifest": manifest(spans)}
    elif stage == "constraints":
        payload = site_constraints(case["address"])
    elif stage == "writer":
        payload, usage = _paid(settings, run_id, "writer",
                               lambda: stages.run_writer(model, case, spans, settings.max_source_chars))
        meta = {"usage": usage, "draft_revision": BASE_REVISION}
    elif stage == "review":
        draft, revision = effective_draft(case, store.load(run_id, "writer")["payload"])
        errors = schemas.validate_draft(draft, {s.span_id for s in spans})
        if errors:
            raise stages.StageFailed("writer", errors)
        payload, usage = _paid(settings, run_id, "review",
                               lambda: stages.run_review(model, draft, spans, settings.max_source_chars))
        meta = {"usage": usage, "draft_revision": revision, "draft_sha256": _sha(draft)}
    else:
        raise ValueError(f"carry_stage does not run {stage}")
    store.save(run_id, stage, payload, meta)
    return payload


def prepare_continuation(case: dict, spans: list[Span], run_id: str, settings: Settings,
                         store: CheckpointStore) -> str:
    """Pick the run directory this resume writes to, creating a continuation run if needed.

    Returns run_id itself only when it does not exist yet, or when it is complete and nothing
    would be written. Otherwise a continuation: a retained run is never added to or changed."""
    base = _latest_run(store, run_id)
    if not (store.root / base).exists():
        _write_manifest(store, run_id, None, case, spans, settings, {}, {})
        return run_id
    kept, missing, stale = qualify(case, spans, base, settings, store)
    if not missing and not stale and _published(case, base, store):
        return base
    if base != run_id and not stale:
        return base  # our own earlier continuation, still valid: carry on in it, no new directory
    n = int(base.rsplit("-c", 1)[1]) + 1 if base != run_id else 1
    target = f"{run_id}-c{n}"
    for stage, record in kept.items():
        store.save(target, stage, record["payload"], {**record["meta"], "reused_from": base})
    _write_manifest(store, target, base, case, spans, settings, kept, {**missing, **stale})
    return target


def qualify(case: dict, spans: list[Span], run_id: str, settings: Settings,
            store: CheckpointStore) -> tuple[dict[str, dict], dict[str, str], dict[str, str]]:
    """Return (records still valid, stages with no record -> why, saved stages that no longer qualify -> why)."""
    kept: dict[str, dict] = {}
    missing: dict[str, str] = {}
    stale: dict[str, str] = {}
    span_ids = {s.span_id for s in spans}
    saved_manifest = _read_manifest(store, run_id)

    def check(stage: str, test) -> None:
        record = store.load(run_id, stage)
        if record is None:
            missing[stage] = "no checkpoint"
            return
        reason = test(record)
        if reason:
            stale[stage] = reason
        else:
            kept[stage] = record

    check("source", lambda r: None if r["meta"].get("manifest") == manifest(spans)
          else "source documents or policies changed since this run")
    check("constraints", lambda r: None if r["payload"] == site_constraints(case["address"])
          else "address or constraint layers changed")

    def writer_test(record: dict) -> str | None:
        if "source" not in kept:
            return "depends on a stale or missing source"
        if saved_manifest.get("writer", {}).get("prompt") != prompts.WRITER_VERSION:
            return "writer prompt version differs or the run has no manifest"
        if saved_manifest["writer"].get("model") != settings.writer_model:
            return "writer model differs"
        if schemas.validate_draft(record["payload"], span_ids):
            return "draft no longer validates against the current spans"
        return None

    check("writer", writer_test)

    def review_test(record: dict) -> str | None:
        if "writer" not in kept:
            return "depends on a stale or missing writer draft"
        draft, revision = effective_draft(case, kept["writer"]["payload"])
        if record["meta"].get("draft_revision", BASE_REVISION) != revision:
            return f"reviewed draft {record['meta'].get('draft_revision', BASE_REVISION)}, current draft is {revision}"
        if record["meta"].get("draft_sha256", _sha(draft)) != _sha(draft):
            return "draft content changed under the same revision"
        if saved_manifest.get("review", {}).get("prompt") != prompts.REVIEW_VERSION:
            return "review prompt version differs or the run has no manifest"
        if saved_manifest["review"].get("model") != settings.review_model:
            return "review model differs"
        if schemas.validate_draft(draft, span_ids) or schemas.validate_review(record["payload"], draft):
            return "review does not cover the current draft"
        return None

    if "writer" in kept:
        check("review", review_test)
    else:
        (stale if store.load(run_id, "review") else missing)["review"] = "depends on a stale or missing writer draft"
    return kept, missing, stale


def publish(case: dict, run_id: str, store: CheckpointStore) -> dict:
    """Export the newest draft for the case with its saved review, if that review is of that draft."""
    writer = store.load(run_id, "writer")["payload"]
    review = store.load(run_id, "review")
    draft, revision = effective_draft(case, writer)
    reviewed = review["meta"].get("draft_revision", BASE_REVISION)
    if reviewed != revision:
        raise stages.StageFailed("export", [f"review is of draft {reviewed}; the current draft is {revision}"])
    result = stages.export(case, draft, review["payload"])
    result["constraints"] = store.load(run_id, "constraints")["payload"]["constraints"]
    saved = store.load(run_id, "export")
    if not saved or saved["payload"] != result:
        store.save(run_id, "export", result, {})
    return result


def effective_draft(case: dict, writer_draft: dict) -> tuple[dict, str]:
    """The draft a review and an export are about: the officer's latest amendment, else the writer's."""
    amended = latest_amendment(case["case_id"])
    if amended:
        return amended["draft"], amended["revision"]
    return writer_draft, BASE_REVISION


def latest_draft(case_id: str, drafts_dir: Path = DRAFTS_DIR) -> dict | None:
    """Officers can amend a draft in the case-management screen; amendments land in drafts/."""
    amended = latest_amendment(case_id, drafts_dir)
    return amended["draft"] if amended else None


def latest_amendment(case_id: str, drafts_dir: Path = DRAFTS_DIR) -> dict | None:
    folder = drafts_dir / case_id
    revisions = sorted(folder.glob("r*.json"), key=lambda p: int(p.stem[1:])) if folder.is_dir() else []
    return json.loads(revisions[-1].read_text(encoding="utf-8")) if revisions else None


def _published(case: dict, run_id: str, store: CheckpointStore) -> bool:
    """True if run_id holds an export identical to what exporting its saved stages gives now."""
    saved = store.load(run_id, "export")
    if not saved:
        return False
    review = store.load(run_id, "review")
    draft, revision = effective_draft(case, store.load(run_id, "writer")["payload"])
    if review["meta"].get("draft_revision", BASE_REVISION) != revision:
        return False
    try:
        result = stages.export(case, draft, review["payload"])
    except stages.StageFailed:
        return False
    result["constraints"] = store.load(run_id, "constraints")["payload"]["constraints"]
    return saved["payload"] == result


def _latest_run(store: CheckpointStore, run_id: str) -> str:
    """run_id, or its newest continuation (<run_id>-cN) if one exists."""
    found = [int(p.name.rsplit("-c", 1)[1]) for p in store.root.glob(f"{run_id}-c*")
             if p.is_dir() and p.name.rsplit("-c", 1)[1].isdigit()]
    return f"{run_id}-c{max(found)}" if found else run_id


def _read_manifest(store: CheckpointStore, run_id: str) -> dict:
    path = store.root / run_id / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write_manifest(store: CheckpointStore, run_id: str, parent: str | None, case: dict, spans: list[Span],
                    settings: Settings, kept: dict, invalidated: dict) -> None:
    record = {"run_id": run_id, "case_id": case["case_id"], "source": manifest(spans),
              "writer": {"model": settings.writer_model, "prompt": prompts.WRITER_VERSION},
              "review": {"model": settings.review_model, "prompt": prompts.REVIEW_VERSION}}
    if parent:
        record["continues"] = parent
        record["qualified"] = sorted(kept)
        record["invalidated"] = invalidated
    store.write_manifest(run_id, record)


def _paid(settings: Settings, run_id: str, stage: str, call) -> tuple[dict, dict]:
    ledger = CampaignLedger(settings.ledger_path)
    ledger.reserve(run_id, stage, RESERVE_USD[stage])
    result, usage = call()
    ledger.settle(run_id, stage, usage.get("cost_usd", RESERVE_USD[stage]))
    return result, usage


def _sha(draft: dict) -> str:
    return hashlib.sha256(json.dumps(draft, sort_keys=True).encode()).hexdigest()
