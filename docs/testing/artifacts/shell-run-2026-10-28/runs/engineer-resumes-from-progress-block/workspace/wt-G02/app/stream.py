"""SSE relay for streamed replies (G02). The event source is injectable so tests need no SDK."""
from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncIterator, Callable


log = logging.getLogger(__name__)


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def relay(
    events: AsyncIterator[dict],
    on_interrupted: Callable[[], None] | None = None,
) -> AsyncIterator[str]:
    """Turn runner events ({"partial": True, "text": ...} or a final event) into SSE frames.

    Ends with exactly one terminal frame: completed, failed or interrupted. When the client
    disconnects no frame can be sent, so the run is stopped and `on_interrupted` records it.
    """
    try:
        async for event in events:
            if event.get("text"):
                yield sse("delta", {"text": event["text"]})
    except (asyncio.CancelledError, GeneratorExit):  # client went away mid-stream
        if on_interrupted:
            on_interrupted()
        raise
    except Exception:  # the runner raised after some partial text
        yield sse("failed", {"message": "The reply could not be finished."})
        return
    finally:
        aclose = getattr(events, "aclose", None)
        if aclose:
            await aclose()  # stops the run
    yield sse("completed", {})


def make_route(run_events: Callable[[str, str, str], AsyncIterator[dict]]):
    """Build the FastAPI route; imported lazily so the module loads without fastapi."""
    from fastapi import Depends
    from fastapi.responses import StreamingResponse

    from app.server import ChatIn, current_principal

    async def chat_stream(body: ChatIn, principal=Depends(current_principal)):
        events = run_events(principal.user_id, body.session_id or "", body.message)
        return StreamingResponse(relay(events, on_interrupted=lambda: log.info("stream interrupted")), media_type="text/event-stream")

    return chat_stream
