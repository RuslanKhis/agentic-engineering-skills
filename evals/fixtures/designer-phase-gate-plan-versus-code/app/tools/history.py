"""Conversation history tools."""
from __future__ import annotations

from app import services


def bulk_delete_history(tool_context) -> dict:
    """Delete every saved conversation of the signed-in customer.

    Use only when the customer asks to delete all of their chat history.

    Returns:
        {"status": "deleted", "count": <number of conversations removed>}.
    """
    count = services.get().store.delete_conversations(tool_context.user_id)
    return {"status": "deleted", "count": count}
