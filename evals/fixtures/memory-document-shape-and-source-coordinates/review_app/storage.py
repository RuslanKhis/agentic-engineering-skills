"""Envelope storage: every stage's output is saved as an immutable envelope and reopened by ID.

An envelope is {"run_id", "stage", "producer", "inputs", "payload"}. put() writes it under
runs/<run_id>/<stage>.<sha12>.json and refuses to overwrite; get() reopens it and checks the
digest. There is no size limit in the adapter; the filesystem store is the configured backend
locally and in CI.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


class EnvelopeError(Exception):
    pass


class EnvelopeStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    @staticmethod
    def _bytes(envelope: dict) -> bytes:
        return json.dumps(envelope, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    def put(self, envelope: dict) -> str:
        for field in ("run_id", "stage", "producer", "inputs", "payload"):
            if field not in envelope:
                raise EnvelopeError(f"envelope has no {field}")
        data = self._bytes(envelope)
        digest = hashlib.sha256(data).hexdigest()
        path = self.root / envelope["run_id"] / f"{envelope['stage']}.{digest[:12]}.json"
        if path.exists():
            raise EnvelopeError(f"{path.name} already stored")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return f"{envelope['run_id']}/{path.name}"

    def get(self, envelope_id: str) -> dict:
        path = self.root / envelope_id
        data = path.read_bytes()
        if not path.name.split(".")[-2] == hashlib.sha256(data).hexdigest()[:12]:
            raise EnvelopeError(f"{envelope_id} does not match its digest")
        return json.loads(data)
