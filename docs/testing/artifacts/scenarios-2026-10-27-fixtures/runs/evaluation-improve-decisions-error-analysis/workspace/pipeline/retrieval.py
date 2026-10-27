"""Choose which local-plan policies the writer sees: keyword overlap between the case text and each policy."""
from __future__ import annotations

import re

K = 2


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 3}


def queries_for(case: dict) -> list[str]:
    # The proposal line alone omits the facts that make a policy apply (parking after works,
    # a protected tree, a window distance), so the application's own page text is queried too.
    pages = [page["text"] for doc in case.get("documents", []) for page in doc["pages"]]
    return [case["proposal"], *pages]


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
