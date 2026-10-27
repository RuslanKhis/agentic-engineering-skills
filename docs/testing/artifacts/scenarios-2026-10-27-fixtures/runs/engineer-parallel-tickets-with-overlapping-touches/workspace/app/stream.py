"""SSE adapter: relays text chunks from a run and ends with exactly one terminal event (C3).

Kept free of `google.adk` imports so it runs under the offline unit tests; `app/server.py`
turns ADK partial events into the text chunks this module relays.
"""
from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Awaitable, Callable

COMPLETED = "completed"
FAILED = "failed"
INTERRUPTED = "interrupted"


def frame(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def relay(chunks: AsyncIterator[str], is_disconnected: Callable[[], Awaitable[bool]],
                record: Callable[[str], None]) -> AsyncIterator[str]:
    """Yield SSE frames for `chunks`, then one terminal frame; `record` gets the terminal state.

    A client that goes away (seen by polling `is_disconnected`, or as the response generator
    being cancelled or closed) stops the run by closing `chunks`, and the state is `interrupted`.
    """
    state = COMPLETED
    try:
        async for text in chunks:
            if await is_disconnected():
                state = INTERRUPTED
                break
            yield frame("text", {"text": text})
    except (asyncio.CancelledError, GeneratorExit):
        state = INTERRUPTED
        raise
    except Exception:
        state = FAILED
    finally:
        await _close(chunks)
        record(state)
    if state != INTERRUPTED:
        yield frame(state, {})


async def _close(chunks: AsyncIterator[str]) -> None:
    aclose = getattr(chunks, "aclose", None)
    if aclose is not None:
        await aclose()
