"""A small keyword index over the help-centre articles in help/articles.json."""
from __future__ import annotations

import json
from pathlib import Path
import re

ARTICLES = Path(__file__).resolve().parent.parent / "help" / "articles.json"


class HelpIndex:
    def __init__(self, articles: list[dict] | None = None) -> None:
        if articles is None:
            articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
        self.articles = articles

    def search(self, query: str, limit: int = 3) -> list[dict]:
        terms = {t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2}
        scored = []
        for article in self.articles:
            words = set(re.findall(r"[a-z0-9]+", (article["title"] + " " + article["body"]).lower()))
            score = len(terms & words)
            if score:
                scored.append((score, article))
        scored.sort(key=lambda pair: -pair[0])
        return [a for _, a in scored[:limit]]
