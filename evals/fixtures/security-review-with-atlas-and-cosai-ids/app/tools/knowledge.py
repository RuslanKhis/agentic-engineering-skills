"""search_corpus over the shared operations corpus index."""
from __future__ import annotations

from corpus.index import CorpusIndex

_index: CorpusIndex | None = None


def search_corpus(query: str) -> dict:
    """Search the shared operations corpus (procedures, carrier notes, how-tos).

    Returns {"status": "ok", "passages": [{doc, uploaded_by, text}]} with at most four passages.
    """
    global _index
    if _index is None:
        _index = CorpusIndex.load()
    return {"status": "ok", "passages": _index.search(query, limit=4)}
