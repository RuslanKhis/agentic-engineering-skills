"""Offline completeness checks for the synthetic park-route retriever.

Runs the skill's local lexical retriever over the extracted segments in
document-coverage.json (questions only, never required_sections), records the
observation, and scores it with the skill's scorer. Adds preflight inventory
checks that flag missing evidence before any query is run. Standard library only.

    python3 -I tools/check_coverage.py --fixture document-coverage.json [--k 4]
Exit 0: every question complete and no preflight finding; 1: missing evidence; 2: bad input.
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/adk-memory-architecture/scripts"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL_SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preflight(fixture):
    """Inventory findings that make an answer unresolved regardless of ranking."""
    segments = fixture["segments"]
    documents = {s["document"] for s in segments.values()}
    pages = {(s["document"], s["page"]) for s in segments.values()}
    findings = []
    for key, seg in segments.items():
        if not seg["text"].strip():
            findings.append({"segment": key, "reason": "empty_extraction"})
        if seg.get("visual_required"):
            findings.append({"segment": key, "reason": "unviewed_visuals"
                             if not seg.get("visual_asset_present") else "visual_review_receipt_needed"})
        for match in re.finditer(r"[Cc]ontinued on page (\d+)", seg["text"]):
            if (seg["document"], int(match.group(1))) not in pages:
                findings.append({"segment": key, "reason": "absent_content",
                                 "detail": f"continuation page {match.group(1)} missing"})
        if seg["section"] != "contents":
            for match in re.finditer(r"\b(Supplement S\d+|Notice N\d+)\b", seg["text"]):
                slug = match.group(1).lower().replace("supplement ", "supplement-").replace("notice ", "notice-")
                if slug not in documents:
                    findings.append({"segment": key, "reason": "absent_content",
                                     "detail": f"referenced {match.group(1)} not in inventory"})
    return findings


def observe(fixture, question_id, k, local_retrieval, max_chars=None):
    """Record what the retriever actually returns for the question text alone."""
    segments = fixture["segments"]
    units = [{"unit_id": key, "document": s["document"], "heading": s["section"], "text": s["text"],
              "page_start": s["page"], "page_end": s["page"]} for key, s in segments.items()]
    conn = local_retrieval.build_index(units)
    query = fixture["questions"][question_id]["question"]
    hits = local_retrieval.search_lexical(conn, query, k)
    return {
        "available_documents": sorted({s["document"] for s in segments.values()}),
        "extracted_segments": {key: s["text"] for key, s in segments.items()},
        "hits": [{"segment": h["unit_id"], "text": h["text"][:max_chars] if max_chars else h["text"]}
                 for h in hits],
        "query_origin": "manual_golden",  # question text, not an agent-formulated query
        "queries": [query],
    }


def run(fixture, k=4, max_chars=None):
    scorer, retrieval = _load("score_document_coverage"), _load("local_retrieval")
    results = []
    for qid in fixture["questions"]:
        report = scorer.score(fixture, qid, observe(fixture, qid, k, retrieval, max_chars))
        report["returned_segments"] = None
        results.append(report)
    return {"k": k, "preflight": preflight(fixture), "questions": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--max-chars", type=int, default=None)
    args = parser.parse_args()
    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        report = run(fixture, args.k, args.max_chars)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print(f"invalid input: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    ok = not report["preflight"] and all(q["retrieval_pass"] for q in report["questions"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
