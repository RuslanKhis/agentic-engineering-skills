"""History trimming used by the summariser plugin. Pure functions; no ADK import."""
from __future__ import annotations

from typing import Any, Sequence


def content_text(content: Any) -> str:
    return " ".join(getattr(p, "text", None) or "" for p in (getattr(content, "parts", None) or []))


def _is_turn_start(content: Any) -> bool:
    """A user content with no function_response part. Every function call and its
    result lie between two turn starts, so cutting only here keeps them together."""
    if getattr(content, "role", None) != "user":
        return False
    return not any(getattr(p, "function_response", None) for p in (getattr(content, "parts", None) or []))


def trim_contents(contents: Sequence[Any], max_items: int) -> tuple[list[Any], list[Any]]:
    """Keep at least the newest max_items contents; return (kept, dropped).

    max_items is a minimum: the cut moves earlier to the nearest turn start so a
    function call is never separated from its response. If no turn start lies at
    or before the cut, nothing is dropped (the current turn is always sent whole).
    """
    if len(contents) <= max_items:
        return list(contents), []
    cut = len(contents) - max_items
    while cut > 0 and not _is_turn_start(contents[cut]):
        cut -= 1
    if cut == 0:
        return list(contents), []
    return list(contents[cut:]), list(contents[:cut])


def summary_line(dropped: Sequence[Any], limit_chars: int = 600) -> str:
    """A one-paragraph digest of the dropped turns, newest last."""
    pieces = [content_text(c).strip() for c in dropped]
    text = " / ".join(p for p in pieces if p)
    return text[-limit_chars:]
