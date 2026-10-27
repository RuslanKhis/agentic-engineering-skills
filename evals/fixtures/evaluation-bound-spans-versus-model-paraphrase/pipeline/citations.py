"""Citation checks and server-side binding of span text."""
from __future__ import annotations

from pipeline.sources import Span


def quote_matches(quote: str, span_ids: list[str], spans: list[Span]) -> bool:
    """True when the quotation appears in the cited spans, joined in order."""
    by_id = {s.span_id: s for s in spans}
    if any(i not in by_id for i in span_ids):
        return False
    joined = "\n".join(by_id[i].text for i in span_ids)
    return quote in joined


def bind(selection: dict, spans: list[Span]) -> dict:
    """Resolve the model's selected span ids to the original text, server-side.

    selection: {"span_ids": [...], "explanation": "..."}; the text returned is the source's own.
    """
    by_id = {s.span_id: s for s in spans}
    missing = [i for i in selection["span_ids"] if i not in by_id]
    if missing:
        raise KeyError(f"unknown span ids: {missing}")
    return {"span_ids": list(selection["span_ids"]),
            "text": "\n".join(by_id[i].text for i in selection["span_ids"]),
            "explanation": selection.get("explanation", "")}
