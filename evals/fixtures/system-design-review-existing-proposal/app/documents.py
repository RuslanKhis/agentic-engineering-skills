"""Search the shared document index and keep the caller's tenant's chunks."""
from __future__ import annotations

from typing import Protocol

TOP_K = 20


class Index(Protocol):
    def query(self, text: str, top_k: int) -> list[dict]: ...


_index: Index | None = None


def set_index(index: Index) -> None:
    global _index
    _index = index


def search_documents(query: str, tool_context) -> dict:
    """Search the customer's travel policies and itineraries.

    Args:
        query: What the traveller is asking about, in a few words.

    Returns:
        {"status": "ok", "chunks": [{"doc_id", "title", "text"}]}.
    """
    tenant_id = tool_context.state.get("tenant_id")
    hits = _index.query(query, TOP_K)
    chunks = [{"doc_id": h["doc_id"], "title": h["title"], "text": h["text"]}
              for h in hits if h.get("tenant_id") == tenant_id]
    return {"status": "ok", "chunks": chunks}
