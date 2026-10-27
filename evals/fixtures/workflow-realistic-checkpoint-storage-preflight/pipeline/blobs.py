"""Private content store for large evidence, addressed by reference.

A reference is {"blob_id", "sha256", "size", "owner", "media_type"}. Content lives under
<root>/<owner>/<blob_id>; only the owning case team (the run's owner) may read it back.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import uuid


class BlobMissing(Exception):
    pass


class BlobChanged(Exception):
    pass


class BlobForbidden(Exception):
    pass


class PrivateBlobStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def put(self, owner: str, data: bytes, media_type: str = "application/json") -> dict:
        blob_id = uuid.uuid4().hex
        path = self.root / owner / blob_id
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return {"blob_id": blob_id, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data),
                "owner": owner, "media_type": media_type}

    def get(self, ref: dict, caller: str) -> bytes:
        if caller != ref.get("owner"):
            raise BlobForbidden(f"{caller} may not read {ref.get('blob_id')}")
        path = self.root / ref["owner"] / ref["blob_id"]
        if not path.exists():
            raise BlobMissing(ref["blob_id"])
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != ref["sha256"] or len(data) != ref["size"]:
            raise BlobChanged(ref["blob_id"])
        return data

    def get_json(self, ref: dict, caller: str):
        return json.loads(self.get(ref, caller).decode("utf-8"))
