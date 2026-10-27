"""Keyword index over corpus documents; built nightly by corpus/ingest.py."""
from __future__ import annotations

import json
from pathlib import Path
import re

INDEX_PATH = Path(__file__).resolve().parent / "index.json"


class CorpusIndex:
    def __init__(self, passages: list[dict]) -> None:
        self.passages = passages

    @classmethod
    def load(cls, path: Path = INDEX_PATH) -> "CorpusIndex":
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def search(self, query: str, limit: int = 4) -> list[dict]:
        terms = {t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2}
        scored = [(len(terms & set(re.findall(r"[a-z0-9]+", p["text"].lower()))), p) for p in self.passages]
        return [p for s, p in sorted(scored, key=lambda x: -x[0]) if s][:limit]
