"""Help-centre search."""
from __future__ import annotations

from app import services


def search_help(query: str) -> str:
    """Search the help centre for articles matching the query and return the matching
    article bodies joined together."""
    articles = services.get().help_index.search(query)
    return "\n\n".join(a["body"] for a in articles)
