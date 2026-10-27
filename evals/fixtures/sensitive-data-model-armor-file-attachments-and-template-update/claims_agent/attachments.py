"""Customer uploads that go to the model with the next message."""
from __future__ import annotations

from dataclasses import dataclass

from claims_agent import config

ACCEPTED_TYPES = {
    "image/jpeg", "image/png", "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class AttachmentRejected(Exception):
    pass


@dataclass
class Attachment:
    filename: str
    mime_type: str
    data: bytes


def accept_attachment(filename: str, content_type: str, data: bytes) -> Attachment:
    """Check an upload and keep it for the next model turn."""
    if content_type not in ACCEPTED_TYPES:
        raise AttachmentRejected(f"{content_type} files are not accepted")
    if len(data) > config.MAX_ATTACHMENT_BYTES:
        raise AttachmentRejected("files must be 10 MB or smaller")
    return Attachment(filename=filename, mime_type=content_type, data=data)


def to_part(attachment: Attachment):
    """The google.genai Part the agent receives."""
    from google.genai import types

    return types.Part.from_bytes(data=attachment.data, mime_type=attachment.mime_type)
