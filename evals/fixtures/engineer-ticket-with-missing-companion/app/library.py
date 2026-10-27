"""Keyword search over the policy library (policies.json beside this file)."""
from __future__ import annotations

import json
from pathlib import Path
import re

POLICIES = json.loads((Path(__file__).with_name("policies.json")).read_text(encoding="utf-8"))


def search_policies(query: str) -> dict:
    """Search internal policies by keywords; returns at most three sections with IDs."""
    terms = {t for t in re.findall(r"[a-z]+", query.lower()) if len(t) > 2}
    hits = [p for p in POLICIES if terms & set(re.findall(r"[a-z]+", p["text"].lower()))]
    return {"status": "ok", "sections": hits[:3]}
