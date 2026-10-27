"""Fetch a customer upload from the uploads bucket and stage it for the code sandbox."""
from __future__ import annotations

import base64
import mimetypes
import os
import re
from pathlib import Path

BUCKET = os.environ.get("UPLOADS_BUCKET", "fjord-uw-uploads")
MAX_BYTES = int(os.environ.get("UPLOADS_MAX_BYTES", str(25 * 1024 * 1024)))
UPLOAD_ID = re.compile(r"up-\d{1,12}")


def download_upload(upload_id: str, tool_context) -> dict:
    """Make a customer's uploaded file available to the code you run.

    Args:
        upload_id: The upload ID shown in the claims portal, e.g. "up-55120".

    Returns:
        {"status": "ok", "file": "<name>"} (read it by that name in your code) or
        {"status": "error", "message": ...}.
    """
    if not UPLOAD_ID.fullmatch(upload_id):
        return {"status": "error", "message": "upload_id must look like up-12345"}

    from google.adk.code_executors.code_execution_utils import File
    from google.adk.code_executors.code_executor_context import CodeExecutorContext
    from google.cloud import storage

    blobs = [b for b in storage.Client().bucket(BUCKET).list_blobs(prefix=f"{upload_id}/")
             if not b.name.endswith("/")]
    if not blobs:
        return {"status": "error", "message": f"no upload {upload_id}"}
    blob = blobs[0]
    if (blob.size or 0) > MAX_BYTES:
        return {"status": "error", "message": f"upload larger than {MAX_BYTES} bytes"}

    name = Path(blob.name).name
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    # Staged in session state, not on the service disk: the sandbox cannot see that disk.
    # Content encoding is base64 text (unverified against File's contract; see README).
    content = base64.b64encode(blob.download_as_bytes()).decode("ascii")
    CodeExecutorContext(tool_context.state).add_input_files(
        [File(name=name, content=content, mime_type=mime)]
    )
    return {"status": "ok", "file": name}
