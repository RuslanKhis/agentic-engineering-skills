"""Checkpoint store for stage results: one JSON record per stage under runs/<run-id>/."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


class StoreLimitExceeded(Exception):
    pass


class CheckpointStore:
    def __init__(self, root: str | Path, limit_bytes: int = 1_048_576) -> None:
        self.root = Path(root)
        self.limit_bytes = limit_bytes

    def save(self, run_id: str, stage: str, payload: dict, meta: dict) -> Path:
        record = {"stage": stage, "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                  "meta": meta, "payload": payload}
        data = json.dumps(record, indent=1, ensure_ascii=False).encode("utf-8")
        if len(data) > self.limit_bytes:
            raise StoreLimitExceeded(f"{stage} checkpoint is {len(data)} bytes; limit {self.limit_bytes}")
        path = self.root / run_id / f"{stage}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def load(self, run_id: str, stage: str) -> dict | None:
        path = self.root / run_id / f"{stage}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def write_manifest(self, run_id: str, manifest: dict) -> Path:
        path = self.root / run_id / "manifest.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
        return path
