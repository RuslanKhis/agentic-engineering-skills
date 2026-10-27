"""Non-blocking writer warnings, kept with the checkpoint for the reviewer and the audit."""
from __future__ import annotations

import re

from pipeline.sources import Span


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def draft_warnings(draft: dict, spans: list[Span]) -> list[dict]:
    by_id = {s.span_id: s for s in spans}
    warnings = []
    for cit in draft.get("citations", []):
        span = by_id.get(cit.get("span_id"))
        if span is not None and cit.get("quote") != span.text:
            warnings.append({"code": "quote_not_verbatim" if _norm(cit["quote"]) != _norm(span.text)
                             else "quote_whitespace", "span_id": span.span_id,
                             "quote": cit.get("quote"), "span_text": span.text})
    return warnings
