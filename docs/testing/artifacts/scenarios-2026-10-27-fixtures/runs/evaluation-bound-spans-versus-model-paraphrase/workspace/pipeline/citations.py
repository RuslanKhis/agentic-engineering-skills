"""Citation checks and server-side binding of span text."""
from __future__ import annotations

from pipeline.sources import Span


def _join_rejoining_hyphens(cited: list[Span]) -> str:
    """Join spans with newlines, except where a word was hyphenated across a line break.

    A line ending in a letter and "-" is rejoined to the next span only when that span is the next
    line of the same document, version and page and starts with a lowercase letter, so the quote
    can never bridge unrelated lines.
    """
    out = cited[0].text
    for prev, cur in zip(cited, cited[1:]):
        adjacent = (prev.doc_id, prev.version, prev.page, prev.line + 1) == \
                   (cur.doc_id, cur.version, cur.page, cur.line)
        if adjacent and prev.text[-2:-1].isalpha() and prev.text.endswith("-") and cur.text[:1].islower():
            out = out[:-1] + cur.text
        else:
            out += "\n" + cur.text
    return out


def quote_matches(quote: str, span_ids: list[str], spans: list[Span]) -> bool:
    """True when the quotation appears in the cited spans, joined in order.

    The exact join is tried first; the hyphen-rejoined join only adds the reading where a line-break
    hyphen is dropped ("build-\\ning" -> "building"). Nothing else is normalised.
    """
    by_id = {s.span_id: s for s in spans}
    if not span_ids or any(i not in by_id for i in span_ids):
        return False
    cited = [by_id[i] for i in span_ids]
    if quote in "\n".join(s.text for s in cited):
        return True
    return quote in _join_rejoining_hyphens(cited)


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
