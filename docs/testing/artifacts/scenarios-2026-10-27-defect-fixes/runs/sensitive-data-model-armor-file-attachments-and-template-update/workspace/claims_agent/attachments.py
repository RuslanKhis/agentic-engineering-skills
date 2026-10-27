"""Customer uploads that go to the model with the next message."""
from __future__ import annotations

import io
import zipfile
from dataclasses import dataclass

from claims_agent import config

ACCEPTED_TYPES = {
    "image/jpeg", "image/png", "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# Kind names match the Model Armor ByteDataItem types. Only these can be screened: the
# template has no image modality, so photos are refused until its owner enables one.
KIND_BY_TYPE = {
    "application/pdf": "PDF",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "WORD_DOCUMENT",
    "image/jpeg": "IMAGE",
    "image/png": "IMAGE",
}
SCREENABLE_KINDS = {"PDF", "WORD_DOCUMENT"}


class AttachmentRejected(Exception):
    pass


@dataclass
class Attachment:
    filename: str
    mime_type: str
    data: bytes
    kind: str = ""


def detect_kind(data: bytes) -> str | None:
    """Classify by leading bytes, never by what the client declared."""
    if data.startswith(b"%PDF-"):
        return "PDF"
    if data.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n")):
        return "IMAGE"
    if data.startswith(b"PK\x03\x04"):
        try:
            names = set(zipfile.ZipFile(io.BytesIO(data)).namelist())  # directory only, no inflation
        except (zipfile.BadZipFile, ValueError):
            return None
        if "[Content_Types].xml" in names and "word/document.xml" in names:
            return "WORD_DOCUMENT"
    return None


def accept_attachment(filename: str, content_type: str, data: bytes) -> Attachment:
    """Check an upload and keep it for the next model turn."""
    if content_type not in ACCEPTED_TYPES:
        raise AttachmentRejected(f"{content_type} files are not accepted")
    if len(data) > config.MAX_ATTACHMENT_BYTES:
        raise AttachmentRejected("files must be 10 MB or smaller")
    kind = detect_kind(data)
    if kind is None or kind != KIND_BY_TYPE[content_type]:
        raise AttachmentRejected("the file contents do not match its type")
    if kind not in SCREENABLE_KINDS:
        raise AttachmentRejected("photos cannot be accepted yet; describe the damage in writing")
    if not config.SCREENABLE_FILE_MIN_BYTES <= len(data) <= config.SCREENABLE_FILE_MAX_BYTES:
        raise AttachmentRejected("documents must be between 69 bytes and 4 MB")
    return Attachment(filename=filename, mime_type=content_type, data=data, kind=kind)


def to_part(attachment: Attachment):
    """The google.genai Part the agent receives."""
    from google.genai import types

    return types.Part.from_bytes(data=attachment.data, mime_type=attachment.mime_type)
