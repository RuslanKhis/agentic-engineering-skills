"""Save a conversation transcript to the customer's own Google Drive (drive.file scope)."""
from __future__ import annotations

from app import services


class DriveNotConnected(Exception):
    pass


def save_transcript_to_drive(conversation_id: str, tool_context) -> dict:
    """Save one of the signed-in customer's conversations to their Google Drive as a text file.

    Needs the customer to have connected Google Drive; otherwise returns needs_consent.

    Args:
        conversation_id: The conversation to save.

    Returns:
        {"status": "saved", "file_id": ...} or {"status": "needs_consent"} or {"status": "not_found"}.
    """
    svc = services.get()
    conversation = next((c for c in svc.store.conversations_for(tool_context.user_id)
                         if c["conversation_id"] == conversation_id), None)
    if conversation is None:
        return {"status": "not_found"}
    drive = getattr(svc, "drive", None)
    if drive is None:
        return {"status": "needs_consent"}
    try:
        file_id = drive.upload_text(tool_context.user_id, f"Harbour Outfitters chat {conversation_id}.txt",
                                    conversation["transcript"])
    except DriveNotConnected:
        return {"status": "needs_consent"}
    return {"status": "saved", "file_id": file_id}
