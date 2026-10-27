"""History trimming used by the summariser plugin. Pure functions; no ADK import."""
from __future__ import annotations

from typing import Any, Sequence


def content_text(content: Any) -> str:
    return " ".join(getattr(p, "text", None) or "" for p in (getattr(content, "parts", None) or []))


def trim_contents(contents: Sequence[Any], max_items: int) -> tuple[list[Any], list[Any]]:
    """Keep the newest max_items contents; return (kept, dropped)."""
    if len(contents) <= max_items:
        return list(contents), []
    cut = len(contents) - max_items
    return list(contents[cut:]), list(contents[:cut])


def summary_line(dropped: Sequence[Any], limit_chars: int = 600) -> str:
    """A one-paragraph digest of the dropped turns, newest last."""
    pieces = [content_text(c).strip() for c in dropped]
    text = " / ".join(p for p in pieces if p)
    return text[-limit_chars:]
