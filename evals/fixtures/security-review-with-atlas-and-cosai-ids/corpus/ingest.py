"""Nightly job: index every new upload in the shared corpus bucket.

Any member of ops-staff can upload to gs://tamsin-ops-corpus/; each file's text is split into
passages and appended to the index as is.
"""
from __future__ import annotations

import json

from corpus.index import INDEX_PATH


def ingest(new_files: list[dict]) -> int:
    """new_files: [{"name", "uploaded_by", "text"}] from the bucket listing since the last run."""
    passages = json.loads(INDEX_PATH.read_text(encoding="utf-8")) if INDEX_PATH.exists() else []
    added = 0
    for f in new_files:
        for chunk in [f["text"][i:i + 800] for i in range(0, len(f["text"]), 800)]:
            passages.append({"doc": f["name"], "uploaded_by": f["uploaded_by"], "text": chunk})
            added += 1
    INDEX_PATH.write_text(json.dumps(passages, indent=1), encoding="utf-8")
    return added
