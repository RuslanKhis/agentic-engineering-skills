"""Turns agent events into the public NDJSON frames of POST /api/chat/stream.

Frames (one JSON object per line):
  {"type": "session", "session_id": ...}                      first
  {"type": "tool_start", "id": ..., "title": ...}
  {"type": "tool_end", "id": ..., "title": ..., "ok": bool}
  {"type": "text", "text": ...}                               complete text of one event
  {"type": "done"} | {"type": "error", "message": ...}        exactly one, last

Only tool titles and an ok flag are public: arguments and results can hold
other people's data, so they never leave the server. Duck-typed on the event
so this module needs no google.adk import.
"""
from __future__ import annotations

import json
import logging
from typing import Any, AsyncIterator

log = logging.getLogger(__name__)

TOOL_TITLES = {
    "lookup_order": "Look up order",
    "list_my_orders": "List your orders",
    "search_help": "Search help articles",
    "issue_refund": "Issue refund",
    "fetch_email": "Read email",
    "send_email": "Send email",
}
FAILED_STATUSES = {"error", "not_found"}
GENERIC_ERROR = "The assistant stopped before finishing. Please try again."


def frame(**fields: Any) -> bytes:
    return (json.dumps(fields, separators=(",", ":")) + "\n").encode()


def _title(name: str | None) -> str:
    return TOOL_TITLES.get(name or "", "Run a tool")


def _frames_for_event(event: Any, open_calls: dict[str, str]) -> list[bytes]:
    out: list[bytes] = []
    if getattr(event, "error_code", None) or getattr(event, "error_message", None):
        log.error("agent event error: %s", getattr(event, "error_code", None))
        return [frame(type="error", message=GENERIC_ERROR)]
    parts = getattr(getattr(event, "content", None), "parts", None) or []
    for part in parts:
        if getattr(part, "thought", False):
            continue
        call = getattr(part, "function_call", None)
        resp = getattr(part, "function_response", None)
        if call is not None:
            call_id = call.id or call.name
            open_calls[call_id] = call.name
            out.append(frame(type="tool_start", id=call_id, title=_title(call.name)))
        elif resp is not None:
            call_id = resp.id or resp.name
            name = open_calls.pop(call_id, resp.name)
            result = resp.response if isinstance(resp.response, dict) else {}
            ok = result.get("status") not in FAILED_STATUSES and "status" in result
            out.append(frame(type="tool_end", id=call_id, title=_title(name), ok=ok))
        elif getattr(part, "text", None):
            out.append(frame(type="text", text=part.text))
    return out


async def stream_frames(session_id: str, events: AsyncIterator[Any]) -> AsyncIterator[bytes]:
    """Yield frames; any failure after the first frame becomes a terminal error frame."""
    yield frame(type="session", session_id=session_id)
    open_calls: dict[str, str] = {}
    try:
        async for event in events:
            for out in _frames_for_event(event, open_calls):
                yield out
                if json.loads(out)["type"] == "error":
                    return
    except Exception:
        log.exception("agent run failed after streaming began")
        yield frame(type="error", message=GENERIC_ERROR)
        return
    finally:
        aclose = getattr(events, "aclose", None)
        if aclose:
            await aclose()
    for call_id, name in open_calls.items():  # run ended without a result for these
        yield frame(type="tool_end", id=call_id, title=_title(name), ok=False)
    yield frame(type="done")
