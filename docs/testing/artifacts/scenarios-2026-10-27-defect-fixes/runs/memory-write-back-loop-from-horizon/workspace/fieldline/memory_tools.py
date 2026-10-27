"""Model-callable memory tools. No google.adk imports so the unit tests run without the SDK.

The engineer is always tool_context.user_id (set by the Runner from the authenticated session). The model
chooses what to remember and its topic; it cannot choose whose memory, and it cannot turn memory on.
"""
from __future__ import annotations

from fieldline.memory_governor import MemoryGovernor

_governor: MemoryGovernor | None = None


def set_governor(governor: MemoryGovernor | None) -> None:
    global _governor
    _governor = governor


def _gov() -> MemoryGovernor:
    if _governor is None:
        from fieldline.services import governor  # deferred: services imports the ADK
        set_governor(governor())
    return _governor


def _call(tool_context) -> tuple[str, str, str]:
    return tool_context.user_id, tool_context.invocation_id, tool_context.function_call_id


def remember(topic: str, text: str, tool_context, site_id: str = "") -> dict:
    """Save one fact the engineer explicitly asked you to remember about themselves.

    Only call this when the engineer says to remember something. Never infer it from conversation.
    Never include codes, passwords, phone numbers or other people's details.

    Args:
        topic: "answer_style" (how they like answers), "kit" (equipment they carry) or "site_note"
            (their own note about a site).
        text: The fact, one short line, in the engineer's own terms.
        site_id: Required for a site_note, e.g. "NW-0522". Leave empty otherwise.
    """
    user, inv, call = _call(tool_context)
    return _gov().stage(user, inv, call, topic, text, site_id or None)


def list_my_memories(tool_context) -> dict:
    """Show the engineer everything that is remembered about them, with each item's save status."""
    return {"status": "ok", "memories": _gov().list_memories(tool_context.user_id)}


def correct_memory(memory_id: str, new_text: str, tool_context) -> dict:
    """Replace one remembered item with a corrected version, at the engineer's request.

    Args:
        memory_id: The id from list_my_memories.
        new_text: The corrected fact, one short line.
    """
    user, inv, call = _call(tool_context)
    return _gov().correct(user, inv, call, memory_id, new_text)


async def forget_memory(memory_id: str, tool_context) -> dict:
    """Delete one remembered item at the engineer's request.

    Args:
        memory_id: The id from list_my_memories.
    """
    return await _gov().forget(tool_context.user_id, memory_id)
