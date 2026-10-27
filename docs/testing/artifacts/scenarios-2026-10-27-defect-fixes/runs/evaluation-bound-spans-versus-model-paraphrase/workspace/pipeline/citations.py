"""Citation checks and server-side binding of span text."""
from __future__ import annotations

from pipeline.sources import Span


def quote_matches(quote: str, span_ids: list[str], spans: list[Span]) -> bool:
    """True when the quotation appears in the cited spans, joined in order."""
    by_id = {s.span_id: s for s in spans}
    if any(i not in by_id for i in span_ids):
        return False
    texts = [by_id[i].text for i in span_ids]
    if quote in "\n".join(texts):
        return True
    # A word hyphenated across a line break is split over two spans; accept the rejoined word.
    # Only a hyphen at the end of one cited span followed by a lowercase letter at the start
    # of the next is rejoined, and the quote must still lie inside the cited spans.
    rejoined = texts[0] if texts else ""
    for text in texts[1:]:
        if rejoined[-1:] == "-" and rejoined[-2:-1].isalpha() and text[:1].islower():
            rejoined = rejoined[:-1] + text
        else:
            rejoined += "\n" + text
    return quote in rejoined


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
