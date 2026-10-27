"""Checkpoint store for stage results: one JSON record per stage under runs/<run-id>/.

The store sits on a document database whose single-record limit is 1 MiB. A record over the
limit is refused; the refused record is kept beside the run as <stage>.rejected.json so the
failure can be examined. Large content can instead live in the private blob store
(pipeline/blobs.py) and be referenced from a record as {"$blob": <reference>}; reopen()
resolves those references for the run's owner.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path

from pipeline.blobs import PrivateBlobStore


class StoreLimitExceeded(Exception):
    pass


class CheckpointStore:
    def __init__(self, root: str | Path, limit_bytes: int = 1_048_576,
                 blobs: PrivateBlobStore | None = None, owner: str | None = None) -> None:
        self.root = Path(root)
        self.limit_bytes = limit_bytes
        self.blobs = blobs
        self.owner = owner

    @classmethod
    def from_settings(cls, settings, owner: str | None = None) -> "CheckpointStore":
        owner = owner or os.environ.get("CASE_TEAM")
        blobs = PrivateBlobStore(settings.blob_dir) if owner else None
        return cls(settings.checkpoint_dir, settings.checkpoint_limit_bytes, blobs=blobs, owner=owner)

    @staticmethod
    def _encode(record: dict) -> bytes:
        return json.dumps(record, indent=1, ensure_ascii=False).encode("utf-8")

    def _spill(self, record: dict, data: bytes) -> tuple[dict, bytes]:
        """Move the largest top-level fields of meta, then payload, into the blob store until the
        record fits. Nothing is dropped or truncated: each field is stored whole, by reference."""
        record = {**record, "meta": dict(record["meta"]), "payload": dict(record["payload"])}
        for section in ("meta", "payload"):
            fields = sorted(record[section], key=lambda k: len(json.dumps(record[section][k])), reverse=True)
            for key in fields:
                if len(data) <= self.limit_bytes:
                    return record, data
                value = record[section][key]
                if isinstance(value, dict) and set(value) == {"$blob"}:
                    continue
                ref = self.blobs.put(self.owner, json.dumps(value, ensure_ascii=False).encode("utf-8"))
                record[section][key] = {"$blob": ref}
                data = self._encode(record)
        return record, data

    def save(self, run_id: str, stage: str, payload: dict, meta: dict) -> Path:
        record = {"stage": stage, "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                  "meta": meta, "payload": payload}
        data = self._encode(record)
        path = self.root / run_id / f"{stage}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        if len(data) > self.limit_bytes and self.blobs is not None and self.owner:
            record, data = self._spill(record, data)
        if len(data) > self.limit_bytes:
            (self.root / run_id / f"{stage}.rejected.json").write_bytes(data)
            raise StoreLimitExceeded(f"{stage} checkpoint is {len(data)} bytes; limit {self.limit_bytes}")
        path.write_bytes(data)
        return path

    def load(self, run_id: str, stage: str) -> dict | None:
        path = self.root / run_id / f"{stage}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def reopen(self, run_id: str, stage: str, caller: str) -> dict | None:
        """Load a record and resolve every {"$blob": ref} in it for the caller."""
        record = self.load(run_id, stage)
        if record is None:
            return None
        return self._resolve(record, caller)

    def _resolve(self, value, caller):
        if isinstance(value, dict):
            if set(value) == {"$blob"}:
                if self.blobs is None:
                    raise RuntimeError("record holds blob references but no blob store is configured")
                return self.blobs.get_json(value["$blob"], caller)
            return {k: self._resolve(v, caller) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve(v, caller) for v in value]
        return value

    def write_manifest(self, run_id: str, manifest: dict) -> Path:
        path = self.root / run_id / "manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
        return path
