"""Project public text from trusted ADK-like events; this is not secret redaction.

Adapt the gateway contract and retain upstream credential exclusion. The caller
owns runner/stream shutdown. Character, event and time caps are configurable
example policy values, not measured service guarantees. No provider calls here.
"""
from __future__ import annotations

import asyncio
from collections.abc import AsyncIterable
import sys

if sys.version_info < (3, 11):
    raise RuntimeError("The public-text adapter requires Python 3.11 or later.")


class PublicProjectionError(ValueError):
    """Fixed safe failure: never include the rejected object's representation."""


def _positive(value: int) -> None:
    if type(value) is not int or value <= 0:
        raise PublicProjectionError("A positive integer limit is required.")


def project_final_text(event: object, *, max_chars: int = 20_000,
                       max_parts: int = 512) -> str | None:
    """Return final text, or None for non-final/content-free events.

    Only text from parts with thought=False/None is copied. Credentials already
    present in that allowed text are NOT detected or removed by this function.
    """
    _positive(max_chars)
    _positive(max_parts)
    try:
        final = event.is_final_response()
        if type(final) is not bool:
            raise PublicProjectionError("Invalid event completion flag.")
        if not final or event.content is None:
            return None
        parts = event.content.parts
        if parts is None:
            return ""
        if not isinstance(parts, (list, tuple)) or len(parts) > max_parts:
            raise PublicProjectionError("Invalid or excessive event parts.")
        output: list[str] = []
        count = 0
        for part in parts:
            thought = part.thought
            if thought is not None and type(thought) is not bool:
                raise PublicProjectionError("Invalid part visibility flag.")
            if thought:
                continue
            value = part.text
            if value is None:
                continue
            if not isinstance(value, str):
                raise PublicProjectionError("Invalid public text field.")
            count += len(value)
            if count > max_chars:
                raise PublicProjectionError("Public text exceeds its limit.")
            output.append(value)
        return "".join(output).strip()
    except PublicProjectionError:
        raise
    except Exception:
        raise PublicProjectionError("Invalid public event shape.") from None


async def collect_final_text(events: AsyncIterable[object], *,
                             max_chars: int = 20_000, max_parts: int = 512,
                             max_events: int = 1_000,
                             timeout_seconds: float = 30.0) -> str | None:
    """Consume through later events within caps; return the last final text.

    This final-JSON adapter is optional. Preserve a streaming application's own
    completion/cancellation contract rather than changing its public protocol.
    """
    _positive(max_chars)
    _positive(max_parts)
    _positive(max_events)
    if (type(timeout_seconds) not in (float, int)
            or not 0 < timeout_seconds < float("inf")):
        raise PublicProjectionError("A finite positive timeout is required.")
    result = None
    count = 0
    try:
        async with asyncio.timeout(timeout_seconds):
            async for event in events:
                count += 1
                if count > max_events:
                    raise PublicProjectionError("Event count exceeds its limit.")
                candidate = project_final_text(event, max_chars=max_chars,
                                               max_parts=max_parts)
                if candidate is not None:
                    result = candidate
    except PublicProjectionError:
        raise
    except Exception:
        raise PublicProjectionError("Public event collection failed.") from None
    return result
