"""Choose which local-plan policies the writer sees: keyword overlap between the proposal and each policy."""
from __future__ import annotations

import re

K = 2


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 3}


def queries_for(case: dict) -> list[str]:
    return [case["proposal"]]


def select_policies(case: dict, policies: dict, k: int = K) -> tuple[dict, dict]:
    """Return (policies restricted to the top k documents, trace)."""
    queries = queries_for(case)
    terms = set().union(*(_words(q) for q in queries))
    scored = []
    for doc in policies["documents"]:
        text = doc["title"] + " " + " ".join(p["text"] for p in doc["pages"])
        scored.append((len(terms & _words(text)), doc["doc_id"]))
    scored.sort(key=lambda pair: -pair[0])
    chosen = [doc_id for _, doc_id in scored[:k]]
    trace = {"queries": queries, "retrieved": chosen, "k": k}
    return {**policies, "documents": [d for d in policies["documents"] if d["doc_id"] in chosen]}, trace
