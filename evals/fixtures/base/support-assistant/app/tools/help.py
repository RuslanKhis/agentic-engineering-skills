"""Help-centre search."""
from __future__ import annotations

from app import services


def search_help(query: str) -> dict:
    """Search the help-centre articles (returns, delivery, faults, account, gift cards).

    Args:
        query: A few keywords from the customer's question.

    Returns:
        {"status": "ok", "articles": [{"id", "title", "body"}]} with at most three articles.
    """
    return {"status": "ok", "articles": services.get().help_index.search(query)}
