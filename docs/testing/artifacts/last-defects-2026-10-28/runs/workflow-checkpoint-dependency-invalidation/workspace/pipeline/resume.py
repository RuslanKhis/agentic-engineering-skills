"""Carry a case on from the stages already saved in the checkpoint store.

Used by the served route so a case interrupted after a paid stage does not pay
for that stage again. A saved stage is loaded only if what it depended on is
unchanged: the source documents, the prompt version, the model settings and, for
a review, the exact draft it reviewed. Anything that fails that check is run
again, along with the stages downstream of it.

Saved runs are evidence and are never written to. New records go to a
continuation directory (<run>-c1, -c2, ...) whose manifest names the parent run,
what was reused and why anything was rejected. Files under diagnostics/ are
never read.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pipeline import prompts, schemas, stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.constraints import load_layers, site_constraints
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies, manifest as source_manifest
from pipeline.stages import StageFailed

STAGES = ("source", "constraints", "writer", "review", "export")


def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def read_manifest(store: CheckpointStore, run_id: str) -> dict:
    path = store.root / run_id / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def lineage(store: CheckpointStore, run_id: str) -> list[str]:
    """The run and its continuations, newest first."""
    n = 0
    while (store.root / f"{run_id}-c{n + 1}").is_dir():
        n += 1
    return [f"{run_id}-c{i}" for i in range(n, 0, -1)] + [run_id]


def source_identity(spans) -> dict:
    return {**source_manifest(spans), "documents": list(dict.fromkeys(f"{s.doc_id}@{s.version}" for s in spans))}


class Resumption:
    """Qualifies saved stages for one case and runs the ones that cannot be reused."""

    def __init__(self, case_dir: Path, run_id: str, settings: Settings, writer: ChatModel, reviewer: ChatModel,
                 store: CheckpointStore, *, drafts_dir: Path = Path("drafts"), continuation: str | None = None):
        self.case = load_case(case_dir)
        self.spans = case_spans(self.case, load_policies())
        self.span_ids = {s.span_id for s in self.spans}
        self.settings, self.writer, self.reviewer, self.store = settings, writer, reviewer, store
        self.parent, self.drafts_dir = run_id, Path(drafts_dir)
        self.source = source_identity(self.spans)
        self.layers = load_layers()
        self.runs = lineage(store, run_id)
        self.fresh = not (store.root / run_id).exists()
        self.run_id = continuation          # the directory being written, once there is one
        self.manifest = read_manifest(store, continuation) if continuation else {
            "parent_run": run_id, "case_id": self.case["case_id"], "source": self.source,
            "constraints": {"layers_version": self.layers["version"]}}
        self.reused: dict[str, str] = {}
        self.rejected: dict[str, list[str]] = {}
        self._review_runs: list[str] = []

    # -- qualification ---------------------------------------------------------------------------
    def _find(self, stage: str, runs: list[str], check) -> tuple[str, dict] | None:
        for run in runs:
            record = self.store.load(run, stage)
            if record is None:
                continue
            reasons = check(record, read_manifest(self.store, run))
            if not reasons:
                self.reused[stage] = run
                return run, record
            self.rejected.setdefault(stage, []).extend(f"{run}: {r}" for r in reasons)
        return None

    def _stale(self, stage: str, man: dict) -> list[str]:
        """Why a saved writer or review no longer matches what it would be run with today."""
        if not man:
            return ["run has no manifest"]
        s = self.settings
        expected = {"writer": {"prompt": prompts.WRITER_VERSION, "model": s.writer_model,
                               "temperature": s.temperature, "max_output_tokens": s.max_output_tokens},
                    "review": {"prompt": prompts.REVIEW_VERSION, "model": s.review_model,
                               "temperature": s.temperature}}[stage]
        reasons = []
        src = man.get("source") or {}
        if src.get("sha256") != self.source["sha256"]:
            reasons.append("source documents changed")
        elif set(src.get("documents", [])) != set(self.source["documents"]):
            reasons.append("source document versions changed")
        block = man.get(stage) or {}
        reasons += [f"{k} was {block.get(k)!r}, now {v!r}" for k, v in expected.items() if block.get(k) != v]
        return reasons

    def _review_stale(self, record: dict, man: dict, draft: dict, rev: str, sha: str) -> list[str]:
        reasons = self._stale("review", man)
        meta = record.get("meta", {})
        saved_rev = meta.get("draft_revision") or (man.get("review") or {}).get("draft_revision")
        if saved_rev != rev:
            reasons.append(f"reviewed draft {saved_rev}, current draft is {rev}")
        elif meta.get("draft_sha256") and meta["draft_sha256"] != sha:
            reasons.append("draft content differs from the one reviewed")
        return reasons + schemas.validate_review(record["payload"], draft)

    # -- stages ----------------------------------------------------------------------------------
    def constraints(self) -> dict:
        def check(record, _man):
            p = record["payload"]
            return [] if (p.get("address"), p.get("layers_version")) == (self.case["address"], self.layers["version"]) \
                else ["address or constraint layers version changed"]
        found = self._find("constraints", self.runs, check)
        if found:
            return found[1]["payload"]
        payload = site_constraints(self.case["address"], self.layers)
        self._save("constraints", payload, {}, None)
        return payload

    def draft(self) -> tuple[dict, str]:
        """The draft the case now stands on and its revision: the saved or fresh writer output, or the
        officer's newest amendment of it."""
        amended = latest_revision(self.case["case_id"], self.drafts_dir)
        found = self._find("writer", self.runs, lambda rec, man: self._stale("writer", man))
        if found is None:
            if amended:
                raise StageFailed("writer", [f"officer amendment {amended[0]} was made on a draft that no longer "
                                             "matches its inputs; not regenerating over it. An officer must decide"])
            draft, usage = stages.run_writer(self.writer, self.case, self.spans, self.settings.max_source_chars)
            sha = digest(draft)
            self._save("writer", draft, {"usage": usage, "draft_revision": "r1", "draft_sha256": sha},
                       {**self._block("writer"), "input": "source", "draft_revision": "r1", "draft_sha256": sha})
            self._review_runs = []
            base = (draft, "r1")
        else:
            run, record = found
            self._review_runs = self.runs[:self.runs.index(run) + 1]
            base = (record["payload"], record.get("meta", {}).get("draft_revision", "r1"))
        if amended:
            self._review_runs = self.runs        # a revision label is unique, so any older review may match it
        draft, rev = (amended[1], amended[0]) if amended else base
        errors = schemas.validate_draft(draft, self.span_ids)
        if errors:
            raise StageFailed("writer", errors)
        return draft, rev

    def review(self, draft: dict, rev: str) -> dict:
        sha = digest(draft)
        found = self._find("review", self._review_runs,
                           lambda rec, man: self._review_stale(rec, man, draft, rev, sha))
        if found:
            return found[1]["payload"]
        review, usage = stages.run_review(self.reviewer, draft, self.spans, self.settings.max_source_chars)
        self._save("review", review, {"usage": usage, "draft_revision": rev, "draft_sha256": sha},
                   {**self._block("review"), "input": "writer", "draft_revision": rev, "draft_sha256": sha})
        return review

    def export(self, draft: dict, rev: str, review: dict, constraints: list[str] | None) -> dict:
        result = stages.export(self.case, draft, review)
        if constraints is not None:
            result["constraints"] = constraints
        newest = next((r for r in map(lambda run: self.store.load(run, "export"), self.runs) if r), None)
        if newest is None or newest["payload"] != result:
            self._save("export", result, {"draft_revision": rev}, None)
        return result

    # -- writing ---------------------------------------------------------------------------------
    def _block(self, stage: str) -> dict:
        s = self.settings
        if stage == "writer":
            return {"model": s.writer_model, "temperature": s.temperature,
                    "max_output_tokens": s.max_output_tokens, "prompt": prompts.WRITER_VERSION}
        return {"model": s.review_model, "temperature": s.temperature, "prompt": prompts.REVIEW_VERSION}

    def _open(self) -> None:
        self.run_id = self.parent if self.fresh else f"{self.parent}-c{len(self.runs)}"
        self.manifest["run_id"] = self.run_id
        self.store.write_manifest(self.run_id, self.manifest)
        self.store.save(self.run_id, "source", {"span_ids": [s.span_id for s in self.spans]},
                        {"manifest": source_manifest(self.spans)})

    def _save(self, stage: str, payload: dict, meta: dict, block: dict | None) -> None:
        if self.run_id is None:
            self._open()
        if block is not None:
            self.manifest[stage] = block
        self.store.save(self.run_id, stage, payload, meta)
        self.store.write_manifest(self.run_id, self.manifest)

    def finish(self) -> None:
        """Record what was reused and what was rejected, if anything was written."""
        if self.run_id is not None:
            self.manifest["reused"] = {**self.manifest.get("reused", {}), **self.reused}
            self.manifest["invalidated"] = {**self.manifest.get("invalidated", {}), **self.rejected}
            self.store.write_manifest(self.run_id, self.manifest)


def resume_case(case_dir: Path, run_id: str, settings: Settings, writer: ChatModel, reviewer: ChatModel,
                store: CheckpointStore, *, drafts_dir: Path = Path("drafts")) -> dict:
    r = Resumption(case_dir, run_id, settings, writer, reviewer, store, drafts_dir=drafts_dir)
    try:
        constraints = r.constraints()
        draft, rev = r.draft()
        review = r.review(draft, rev)
        return r.export(draft, rev, review, constraints["constraints"])
    finally:
        r.finish()


def publish(case: dict, run_id: str, store: CheckpointStore, drafts_dir: Path = Path("drafts")) -> dict:
    """Export the newest draft for the case, only if the saved review is of that draft."""
    saved_writer = store.load(run_id, "writer")
    review = store.load(run_id, "review")
    amended = latest_revision(case["case_id"], drafts_dir)
    rev, draft = amended or (saved_writer["meta"].get("draft_revision", "r1"), saved_writer["payload"])
    reviewed = review["meta"].get("draft_revision")
    if reviewed != rev:
        raise StageFailed("export", [f"saved review is of draft {reviewed}; current draft is {rev}"])
    result = stages.export(case, draft, review["payload"])
    result["constraints"] = store.load(run_id, "constraints")["payload"]["constraints"]
    store.save(run_id, "export", result, {"draft_revision": rev})
    return result


def latest_revision(case_id: str, drafts_dir: Path = Path("drafts")) -> tuple[str, dict] | None:
    """Officers can amend a draft in the case-management screen; amendments land in drafts/."""
    folder = Path(drafts_dir) / case_id
    revisions = sorted((p for p in folder.glob("r*.json") if p.stem[1:].isdigit()),
                       key=lambda p: int(p.stem[1:])) if folder.is_dir() else []
    if not revisions:
        return None
    data = json.loads(revisions[-1].read_text(encoding="utf-8"))
    return data.get("revision", revisions[-1].stem), data["draft"]


def latest_draft(case_id: str, drafts_dir: Path = Path("drafts")) -> dict | None:
    latest = latest_revision(case_id, drafts_dir)
    return latest[1] if latest else None
