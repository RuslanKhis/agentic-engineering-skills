"""SSE relay for streamed replies (G02). The event source is injectable so tests need no SDK."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncIterator, Callable


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def relay(
    events: AsyncIterator[dict], record: Callable[[str], None] | None = None
) -> AsyncIterator[str]:
    """Turn runner events ({"partial": True, "text": ...} or a final event) into SSE frames.

    Ends in exactly one terminal state: completed, failed or interrupted. `record` receives
    that state. An interrupted stream (client gone) cannot send a frame, so it is recorded only.
    """
    terminal = "completed"
    try:
        async for event in events:
            if event.get("text"):
                yield sse("delta", {"text": event["text"]})
    except (asyncio.CancelledError, GeneratorExit):  # client disconnected
        terminal = "interrupted"
        raise
    except Exception:  # the runner raised after some partial text
        terminal = "failed"
    finally:
        aclose = getattr(events, "aclose", None)
        if aclose is not None:  # stop the run
            await aclose()
        if record is not None:
            record(terminal)
    if terminal == "failed":
        yield sse("failed", {"message": "The reply could not be finished."})
    else:
        yield sse("completed", {})


def make_route(run_events: Callable[[str, str, str], AsyncIterator[dict]]):
    """Build the FastAPI route; imported lazily so the module loads without fastapi."""
    from fastapi import Depends
    from fastapi.responses import StreamingResponse

    from app.server import ChatIn, current_principal

    async def chat_stream(body: ChatIn, principal=Depends(current_principal)):
        events = run_events(principal.user_id, body.session_id or "", body.message)
        record = lambda state: logging.getLogger(__name__).info("stream %s", state)
        return StreamingResponse(relay(events, record), media_type="text/event-stream")

    return chat_stream
