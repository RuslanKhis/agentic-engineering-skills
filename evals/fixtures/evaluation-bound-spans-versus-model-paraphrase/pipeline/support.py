"""Support check for a draft's reasons."""
from __future__ import annotations

from pipeline.sources import Span


def reason_supported(reason: dict, spans: list[Span]) -> bool:
    """A reason is supported when every cited span exists and the writer marked it supported."""
    known = {s.span_id for s in spans}
    return bool(reason.get("citations")) and all(c in known for c in reason["citations"]) \
        and reason.get("support", "supported") == "supported"
