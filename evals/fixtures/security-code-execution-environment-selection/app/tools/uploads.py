"""Fetch a customer upload from the uploads bucket to local disk."""
from __future__ import annotations

import os
from pathlib import Path

BUCKET = os.environ.get("UPLOADS_BUCKET", "fjord-uw-uploads")
LOCAL_DIR = Path(os.environ.get("UPLOADS_DIR", "/tmp/uploads"))


def download_upload(upload_id: str) -> dict:
    """Download a customer's uploaded file so code can read it.

    Args:
        upload_id: The upload ID shown in the claims portal, e.g. "up-55120".

    Returns:
        {"status": "ok", "path": "/tmp/uploads/<file>"} or {"status": "error", "message": ...}.
    """
    from google.cloud import storage

    blobs = list(storage.Client().bucket(BUCKET).list_blobs(prefix=f"{upload_id}/"))
    if not blobs:
        return {"status": "error", "message": f"no upload {upload_id}"}
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    target = LOCAL_DIR / Path(blobs[0].name).name
    blobs[0].download_to_filename(str(target))
    return {"status": "ok", "path": str(target)}
