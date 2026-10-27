"""Tools over a small local paper index. No google.adk imports."""
from __future__ import annotations

PAPERS = {
    "p-101": {"title": "Retrieval-augmented generation for policy documents", "year": 2025,
              "abstract": "We study chunking by operative unit for planning policy retrieval."},
    "p-102": {"title": "Measuring tool-use reliability in agents", "year": 2026,
              "abstract": "Repeated trials and pass^k for tool-using agents."},
}


def search_papers(query: str, limit: int = 5) -> dict:
    """Search the paper index by title keywords. Returns ids, titles and years."""
    words = query.lower().split()
    hits = [{"paper_id": k, "title": v["title"], "year": v["year"]}
            for k, v in PAPERS.items() if any(w in v["title"].lower() for w in words)]
    return {"status": "ok", "papers": hits[:limit]}


def get_abstract(paper_id: str) -> dict:
    """Return one paper's abstract by its id, e.g. "p-101"."""
    paper = PAPERS.get(paper_id)
    if paper is None:
        return {"status": "not_found", "message": f"No paper {paper_id}."}
    return {"status": "ok", "abstract": paper["abstract"]}
