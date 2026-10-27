"""search_docs: retrieval over the help-centre articles and the community answers index."""
from __future__ import annotations

import json
from pathlib import Path

from app import services
from app.helpdesk import HelpIndex

COMMUNITY = Path(__file__).resolve().parents[2] / "help" / "community.json"


def search_docs(query: str) -> dict:
    """Search the help-centre articles and the community answers.

    Community answers are posts customers write on the public forum; they are indexed nightly.

    Args:
        query: A few keywords from the question.

    Returns:
        {"status": "ok", "results": [{"id", "source", "title", "body"}]} with at most five results.
    """
    articles = [dict(a, source="help-centre") for a in services.get().help_index.search(query)]
    posts = json.loads(COMMUNITY.read_text(encoding="utf-8"))
    community = [dict(p, source="community") for p in HelpIndex(posts).search(query)]
    return {"status": "ok", "results": (articles + community)[:5]}
