"""Carry a case on from the stages already saved in the checkpoint store.

Used by the served route so a case interrupted after a paid stage does not pay
for that stage again. A saved stage is loaded only when everything it was made
from still matches: the source spans, the instructions, the schema, the model
settings and, for a review, the exact draft it checked. Anything else is
invalidated, with its descendants, and runs again.

Retained runs are evidence and are never written to. A continuation writes a new
run directory (`<case>-r<n>`) whose manifest links to the parent and records which
stages were reused and which were invalidated, and why.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pipeline import prompts, schemas, stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.constraints import load_layers, site_constraints
from pipeline.model import ChatModel
from pipeline.sources import PARSER, case_spans, load_case, load_policies, manifest as source_manifest

STAGES = ("source", "constraints", "writer", "review", "export")

# Identity fields a saved manifest must carry to qualify a model stage; a missing one means "cannot prove it".
REQUIRED = {
    "writer": ("model", "temperature", "max_output_tokens", "prompt", "instructions_sha256", "schema_sha256"),
    "review": ("model", "temperature", "prompt", "instructions_sha256", "schema_sha256"),
}
# Compared only when the saved manifest recorded them (older manifests did not).
OPTIONAL = ("max_output_tokens", "max_source_chars", "draft_sha256")


def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def resume_case(case_dir: Path, run_id: str, settings: Settings, writer: ChatModel, reviewer: ChatModel,
                store: CheckpointStore, drafts_dir: Path = Path("drafts")) -> dict:
    case = load_case(case_dir)
    spans = case_spans(case, load_policies())
    cont = Continuation(store, run_id, case, spans, settings, writer, reviewer, drafts_dir)
    cont.obtain("source", lambda: ({"span_ids": [s.span_id for s in spans]}, {}))
    cont.obtain("constraints", lambda: (site_constraints(case["address"]), {}))
    draft = cont.obtain_draft(lambda: stages.run_writer(writer, case, spans, settings.max_source_chars))
    review = cont.obtain("review", lambda: stages.run_review(reviewer, draft, spans, settings.max_source_chars))
    return cont.publish(draft, review)


class Continuation:
    """Qualifies saved stages against the current inputs and writes the continuation run."""

    def __init__(self, store: CheckpointStore, parent_run: str, case: dict, spans: list, settings: Settings,
                 writer: ChatModel, reviewer: ChatModel, drafts_dir: Path = Path("drafts"),
                 run_id: str | None = None) -> None:
        self.store, self.parent_run, self.case, self.spans = store, parent_run, case, spans
        self.settings, self.writer, self.reviewer, self.drafts_dir = settings, writer, reviewer, drafts_dir
        self.run_id = run_id            # the continuation run; allocated on the first write
        self.draft: dict | None = None
        self.hits: dict[str, str] = {}  # stage -> run the saved record came from
        self.rejected: dict[str, list[str]] = {}
        self.span_ids = [s.span_id for s in spans]
        self.src = source_manifest(spans)

    # ---- reading saved runs -------------------------------------------------------------------
    def _manifest(self, run: str) -> dict | None:
        path = self.store.root / run / "manifest.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def _candidates(self) -> list[str]:
        """Continuations of the parent, newest first, then the parent."""
        children = []
        for path in self.store.root.glob(f"{self.case['case_id']}-r*"):
            man = self._manifest(path.name)
            if man and man.get("continuation", {}).get("parent_run") == self.parent_run:
                children.append((_rev_no(path.name), path.name))
        return [name for _, name in sorted(children, reverse=True)] + [self.parent_run]

    def amendment(self) -> tuple[str, dict, dict] | None:
        """The newest officer-amended draft: (revision, draft, file record)."""
        folder = self.drafts_dir / self.case["case_id"]
        revisions = sorted(folder.glob("r*.json"), key=lambda p: _rev_no(p.stem)) if folder.is_dir() else []
        if not revisions:
            return None
        rec = json.loads(revisions[-1].read_text(encoding="utf-8"))
        return rec.get("revision", revisions[-1].stem), rec["draft"], rec

    def _section(self, stage: str, draft: dict | None = None) -> dict:
        """The identity the stage would have if it ran now."""
        if stage == "source":
            return {**self.src, "parser": PARSER, "documents": sorted({s.span_id.split(":")[0] for s in self.spans})}
        if stage == "constraints":
            return {"layers_version": load_layers()["version"]}
        model, name, instruction, schema = ((self.writer, "writer", prompts.WRITER_INSTRUCTION, schemas.DRAFT_SCHEMA)
                                            if stage == "writer" else
                                            (self.reviewer, "review", prompts.REVIEW_INSTRUCTION, schemas.REVIEW_SCHEMA))
        section = {"model": model.model, "temperature": model.temperature,
                   "max_output_tokens": model.max_output_tokens,
                   "max_source_chars": self.settings.max_source_chars,
                   "prompt": prompts.WRITER_VERSION if stage == "writer" else prompts.REVIEW_VERSION,
                   "instructions_sha256": hashlib.sha256(instruction.encode()).hexdigest(),
                   "schema_sha256": digest(schema), "input": "source" if stage == "writer" else "writer"}
        if stage == "review" and draft is not None:
            section["draft_sha256"] = digest(draft)
        return section

    def _check(self, run: str, stage: str) -> list[str]:
        """Reasons the saved record is not reusable; empty means it qualifies."""
        rec = self.store.load(run, stage)
        man = self._manifest(run)
        if rec is None:
            return ["no checkpoint"]
        if man is None:
            return ["no manifest, so its inputs cannot be verified"]
        payload = rec["payload"]
        if stage == "source":
            saved = man.get("source", {})
            if saved.get("sha256") != self.src["sha256"] or saved.get("parser") != PARSER:
                return ["source spans or parser changed"]
            return [] if payload.get("span_ids") == self.span_ids else ["saved span ids differ"]
        if stage == "constraints":
            return [] if payload == site_constraints(self.case["address"]) else ["address or constraint layers changed"]
        if man.get("source", {}).get("sha256") != self.src["sha256"] or man.get("source", {}).get("parser") != PARSER:
            return ["produced from different source spans"]
        saved = man.get(stage, {})
        if stage == "writer":
            if saved.get("origin") == "officer_amendment":
                return self._check_amended(saved)
            current = self._section("writer")
        else:
            current = self._section("review", self.draft)
            saved = dict(saved)
            if "draft_sha256" not in saved:
                # Older manifests: a review checked the writer output saved in the same run.
                writer_rec, writer_saved = self.store.load(run, "writer"), man.get("writer", {})
                if writer_rec is None or writer_saved.get("origin") == "officer_amendment":
                    return ["review input draft cannot be identified"]
                saved["draft_sha256"] = digest(writer_rec["payload"])
        errors = [f"{k} is not recorded" for k in REQUIRED[stage] if k not in saved]
        errors += [f"{k} changed" for k in (*REQUIRED[stage], *OPTIONAL)
                   if k in saved and k in current and saved[k] != current[k]]
        if errors:
            return errors
        if stage == "writer":
            errors = schemas.validate_draft(payload, set(self.span_ids))
        else:
            errors = schemas.validate_review(payload, self.draft)
        return [f"saved output invalid: {e}" for e in errors]

    def _check_amended(self, saved: dict) -> list[str]:
        amended = self.amendment()
        if amended is None:
            return ["saved draft is an officer amendment but none exists now"]
        return [] if saved.get("draft_sha256") == digest(amended[1]) else ["officer draft differs"]

    def lookup(self, stage: str) -> tuple[str, dict] | None:
        for run in self._candidates():
            if stage == "writer" and self.amendment() is not None:
                amended = self.amendment()
                rec = self.store.load(run, "writer")
                man = (self._manifest(run) or {}).get("writer", {})
                if rec and man.get("origin") == "officer_amendment" and not self._check_amended(man) \
                        and not schemas.validate_draft(rec["payload"], set(self.span_ids)):
                    self.hits[stage] = run
                    return run, rec
                self.rejected.setdefault(stage, []).append(f"{run}: model draft superseded by officer draft {amended[0]}")
                continue
            reasons = self._check(run, stage)
            if not reasons:
                self.hits[stage] = run
                return run, self.store.load(run, stage)
            self.rejected.setdefault(stage, []).append(f"{run}: " + "; ".join(reasons))
        return None

    # ---- obtaining stages ---------------------------------------------------------------------
    def obtain(self, stage: str, produce) -> dict:
        """Saved payload if it qualifies, otherwise produce() -> (payload, usage), saved to the continuation run."""
        hit = self.lookup(stage)
        if hit:
            run, rec = hit
            if self.run_id is not None and run != self.run_id:
                self._write(stage, rec["payload"], {"reused_from": run, "original_saved_at": rec["saved_at"],
                                                    "original_meta": rec["meta"]}, reused=run)
            return rec["payload"]
        payload, usage = produce()
        if stage == "review":
            self._fence_draft()
        self._write(stage, payload, {"usage": usage}, fresh=True)
        return payload

    def obtain_draft(self, produce) -> dict:
        hit = self.lookup("writer")
        amended = self.amendment()
        if hit:
            run, rec = hit
            if self.run_id is not None and run != self.run_id:
                self._write("writer", rec["payload"], {"reused_from": run, "original_saved_at": rec["saved_at"],
                                                       "original_meta": rec["meta"]}, reused=run)
            self.draft = rec["payload"]
        elif amended:
            revision, draft, rec = amended
            errors = schemas.validate_draft(draft, set(self.span_ids))
            if errors:
                raise stages.StageFailed("writer", [f"officer draft {revision}: {e}" for e in errors])
            self.draft = draft
            self._write("writer", draft, {"officer_amendment": revision, "amended_by": rec.get("amended_by"),
                                          "amended_at": rec.get("amended_at"), "parent_revision": rec.get("parent_revision")},
                        fresh=True, section={"origin": "officer_amendment", "draft_revision": revision,
                                             "draft_sha256": digest(draft)})
        else:
            self.draft, usage = produce()
            self._write("writer", self.draft, {"usage": usage}, fresh=True)
        return self.draft

    def publish(self, draft: dict, review: dict) -> dict:
        """Export (deterministic, no model). Skips the write when one saved run already holds the same result."""
        result = build_export(self.case, draft, review, self.store.load(self._run_of("constraints"), "constraints")["payload"])
        runs = {self.hits.get(s) for s in ("source", "constraints", "writer", "review")}
        if self.run_id is None and len(runs) == 1:
            rec = self.store.load(runs.pop(), "export")
            if rec and rec["payload"] == result:
                return result
        self._write("export", result, {}, fresh=True)
        return result

    # ---- writing the continuation run -----------------------------------------------------------
    def _run_of(self, stage: str) -> str:
        return self.run_id if self.run_id and self.store.load(self.run_id, stage) else self.hits[stage]

    def _fence_draft(self) -> None:
        """A review may only be committed against the draft revision it checked."""
        amended = self.amendment()
        if amended and digest(amended[1]) != digest(self.draft):
            raise stages.StageFailed("review", ["draft was amended while the review ran; review discarded"])

    def _ensure_run(self, stage: str) -> None:
        if self.run_id is None:
            case_id = self.case["case_id"]
            taken = [_rev_no(p.name) for p in self.store.root.glob(f"{case_id}-r*")]
            fresh_run = not (self.store.root / self.parent_run).exists()    # nothing saved: a first run, not a continuation
            self.run_id = self.parent_run if fresh_run else f"{case_id}-r{max(taken, default=0) + 1}"
            self.store.write_manifest(self.run_id, {
                "run_id": self.run_id, "case_id": case_id, "source": self._section("source"),
                "continuation": {"parent_run": None if fresh_run else self.parent_run, "stages": {}, "invalidated": {}}})
            for earlier in STAGES[:STAGES.index(stage)]:     # copy qualified upstream stages into the new run
                hit = (self.hits.get(earlier), None) if earlier in self.hits else (self.lookup(earlier) or (None,))
                run = hit[0]
                if run:
                    rec = self.store.load(run, earlier)
                    self._write(earlier, rec["payload"], {"reused_from": run, "original_saved_at": rec["saved_at"],
                                                          "original_meta": rec["meta"]}, reused=run)

    def _write(self, stage: str, payload: dict, meta: dict, reused: str | None = None, fresh: bool = False,
               section: dict | None = None) -> None:
        self._ensure_run(stage)
        self.store.save(self.run_id, stage, payload, meta)
        man = self._manifest(self.run_id)
        if stage in ("writer", "review"):
            if reused:
                section = dict((self._manifest(reused) or {}).get(stage, {}))
                if stage == "review":
                    section["draft_sha256"] = digest(self.draft)
            elif section is None:
                section = self._section(stage, self.draft)
                section["attempt"] = f"{self.run_id}-{stage}"
            if stage == "writer":
                section.setdefault("draft_revision", "r1")
            else:
                section["draft_revision"] = self._revision()
            man[stage] = section
        elif stage == "constraints":
            man[stage] = self._section("constraints")
        cont = man["continuation"]
        cont["stages"][stage] = {"reused_from": reused} if reused else {"executed": True}
        cont["invalidated"] = self.rejected
        self.store.write_manifest(self.run_id, man)

    def _revision(self) -> str:
        amended = self.amendment()
        return amended[0] if amended else "r1"


def build_export(case: dict, draft: dict, review: dict, constraints: dict) -> dict:
    result = stages.export(case, draft, review)
    result["constraints"] = constraints["constraints"]
    return result


def publish(case: dict, run_id: str, store: CheckpointStore) -> dict:
    """Export a run's own draft with its own review, and save it in that run."""
    draft = store.load(run_id, "writer")["payload"]
    review = store.load(run_id, "review")["payload"]
    result = build_export(case, draft, review, store.load(run_id, "constraints")["payload"])
    store.save(run_id, "export", result, {})
    return result


def latest_draft(case_id: str, drafts_dir: Path = Path("drafts")) -> dict | None:
    """Officers can amend a draft in the case-management screen; amendments land in drafts/."""
    folder = drafts_dir / case_id
    revisions = sorted(folder.glob("r*.json"), key=lambda p: _rev_no(p.stem)) if folder.is_dir() else []
    if not revisions:
        return None
    return json.loads(revisions[-1].read_text(encoding="utf-8"))["draft"]


def _rev_no(name: str) -> int:
    match = re.search(r"r(\d+)$", name)
    return int(match.group(1)) if match else 0
