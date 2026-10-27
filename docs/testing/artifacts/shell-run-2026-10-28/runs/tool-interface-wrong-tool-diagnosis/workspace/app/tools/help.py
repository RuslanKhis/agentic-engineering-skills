"""Help-centre search."""
from __future__ import annotations

from app import services


def search_help(query: str) -> dict:
    """Search the help centre for policy and how-to articles (returns window,
    refund rules, delivery times). Not for a customer's own orders; use
    get_order or list_my_orders for those.

    Args:
        query: Keywords describing the question, e.g. "returns refund".

    Returns:
        {"status": "ok", "articles": "<matching article bodies joined by blank lines>"}
        or {"status": "not_found", "hint": ...} when nothing matches.
    """
    articles = services.get().help_index.search(query)
    if not articles:
        return {"status": "not_found", "hint": "No article matched; try different keywords."}
    return {"status": "ok", "articles": "\n\n".join(a["body"] for a in articles)}
