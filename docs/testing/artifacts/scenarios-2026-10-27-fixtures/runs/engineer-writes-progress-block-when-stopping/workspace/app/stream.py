"""SSE relay for streamed replies (C3). No google.adk imports: the event source is any async iterator."""
from __future__ import annotations

import json
from typing import AsyncIterator


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _text(event) -> str:
    content = getattr(event, "content", None)
    if not content or not content.parts:
        return ""
    return "".join(p.text for p in content.parts if getattr(p, "text", None))


async def relay(events: AsyncIterator, session_id: str) -> AsyncIterator[str]:
    """Relay ADK events as SSE: `text` for each chunk, then one terminal event.

    Partial events carry the chunks. The closing non-partial event repeats the whole text,
    so it is used only when no partial arrived (a model that did not stream).
    """
    yield sse("session", {"session_id": session_id})
    saw_partial = False
    async for event in events:
        if getattr(event, "partial", False):
            saw_partial = True
            chunk = _text(event)
        elif not saw_partial:
            chunk = _text(event)
        else:
            chunk = ""
        if chunk:
            yield sse("text", {"text": chunk})
    yield sse("completed", {})
