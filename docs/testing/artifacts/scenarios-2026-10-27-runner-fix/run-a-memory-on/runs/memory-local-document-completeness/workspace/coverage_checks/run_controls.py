"""Offline missing-evidence controls for the local policy retriever.

Builds adapter-style observations from the synthetic fixture, scores each with the
skill's scorer and compares the diagnoses with expectations held here (grader side).
Also replays the fixture questions through the real local_retrieval pipeline at its
default limits and scores what it actually returned. No PDF parsing, no network.

Usage: python3 -I run_controls.py [--fixture PATH] [--json]
Exit 0 when every control behaves as expected, 1 otherwise, 2 on unreadable input.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import sys

SKILL = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "adk-memory-architecture"
DEFAULT_FIXTURE = SKILL / "assets" / "document-coverage.json"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observation(fixture, hits, *, documents=None, extracted=None, origin="manual_golden",
                queries=("controlled fixture query",)):
    """Adapter record: extraction of every segment unless overridden, hits as full passages."""
    segments = fixture["segments"]
    docs = documents if documents is not None else sorted({s["document"] for s in segments.values()})
    ext = extracted if extracted is not None else {k: s["text"] for k, s in segments.items()}
    return {"available_documents": list(docs), "extracted_segments": ext,
            "hits": [{"segment": k, "text": t if t is not None else segments[k]["text"]}
                     for k, t in hits],
            "query_origin": origin, "queries": list(queries)}


def controls(fixture):
    seg = fixture["segments"]
    full = {k: s["text"] for k, s in seg.items()}
    maintenance_all = ["route-rule", "table-first", "table-continuation", "maintenance-exception"]
    cut = seg["table-continuation"]["text"].split(" | ")[0]  # truncated extraction of page 4
    # (name, question, observation, expected reasons per segment, expected pass)
    return [
        ("complete_text_control", "maintenance-route",
         observation(fixture, [(k, None) for k in maintenance_all]), {}, True),
        ("complete_table_control", "complete-table",
         observation(fixture, [("table-first", None), ("table-continuation", None)]), {}, True),
        ("main_policy_only", "maintenance-route",
         observation(fixture, [("route-rule", None), ("table-first", None), ("table-continuation", None)],
                     documents=["main-policy"],
                     extracted={k: v for k, v in full.items() if seg[k]["document"] == "main-policy"}),
         {"maintenance-exception": {"absent_content"}}, False),
        ("main_available_but_exception_not_returned", "maintenance-route",
         observation(fixture, [("route-rule", None), ("table-first", None), ("table-continuation", None)]),
         {"maintenance-exception": {"query_miss"}}, False),
        ("contents_only", "maintenance-route",
         observation(fixture, [("contents", None)]),
         {k: {"query_miss"} for k in maintenance_all}, False),
        ("first_table_page_only", "complete-table",
         observation(fixture, [("table-first", None)]),
         {"table-continuation": {"query_miss"}}, False),
        ("truncated_table_extraction", "complete-table",
         observation(fixture, [("table-first", None), ("table-continuation", cut)],
                     extracted={**full, "table-continuation": cut}),
         {"table-continuation": {"section_truncation"}}, False),
        ("empty_text_page", "maintenance-route",
         observation(fixture, [("table-first", None), ("table-continuation", None),
                               ("maintenance-exception", None)],
                     extracted={**full, "route-rule": ""}),
         {"route-rule": {"empty_extraction"}}, False),
        ("empty_image_page", "closure-status",
         observation(fixture, [], extracted={**full, "closure-notice": ""}),
         {"closure-notice": {"empty_extraction", "unviewed_visuals"}}, False),
        ("image_page_claimed_reviewed", "closure-status",
         {**observation(fixture, [], extracted={**full, "closure-notice": "Route Cedar is open."}),
          "claimed_visual_review": True},
         {"closure-notice": {"unviewed_visuals"}}, False),
    ]


def run_controls(fixture, scorer):
    results = []
    for name, question, obs, expected, expect_pass in controls(fixture):
        report = scorer.score(fixture, question, obs)
        got = {}
        for d in report["diagnoses"]:
            got.setdefault(d["segment"], set()).add(d["reason"])
        ok = got == expected and report["retrieval_pass"] is expect_pass
        results.append({"control": name, "question": question, "ok": ok,
                        "document_coverage": report["document_coverage"],
                        "section_coverage": report["operative_section_coverage"],
                        "diagnoses": {k: sorted(v) for k, v in got.items()},
                        "expected": {k: sorted(v) for k, v in expected.items()},
                        "retrieval_pass": report["retrieval_pass"]})
    # a contents hit is a document hit only: the numerator must not credit sections
    contents = next(r for r in results if r["control"] == "contents_only")
    contents["ok"] = (contents["ok"] and contents["document_coverage"]["covered"] >= 1
                      and contents["section_coverage"]["covered"] == 0)
    return results


def replay_retriever(fixture, scorer):
    """Run the shipped retriever (default k and budget) and score its actual output."""
    retrieval = load("local_retrieval")
    segments = fixture["segments"]
    pages = [{"document": s["document"], "page": s["page"], "text": s["text"]}
             for s in segments.values()]  # retriever never sees sections or questions
    kept, screened = retrieval.screen_units(retrieval.chunk_by_heading(pages))
    conn = retrieval.build_index(kept)
    by_page = {(s["document"], s["page"]): k for k, s in segments.items()}
    out = []
    for qid, q in fixture["questions"].items():
        report = retrieval.retrieve_for_issues(conn, [{"id": qid, "query": q["question"]}])
        entry = report["issues"][qid]
        found = [] if entry["found"] == "none_found" else entry["found"]
        hits = []
        for unit in found:
            key = by_page.get((unit["document"], unit["page_start"]))
            row = conn.execute("SELECT heading, text FROM unit_meta WHERE unit_id = ?",
                               (unit["unit_id"],)).fetchone()
            hits.append({"segment": key, "text": "\n".join(p for p in row if p)})
        documents = sorted({s["document"] for s in segments.values()})
        obs = {"available_documents": documents,
               "extracted_segments": {k: s["text"] for k, s in segments.items()},
               "hits": hits, "query_origin": "fixture_question_replay", "queries": [q["question"]]}
        scored = scorer.score(fixture, qid, obs)
        out.append({"question": qid, "k": report["k"], "calls_run": report["calls_run"],
                    "found_units": [u["unit_id"] for u in found],
                    "retriever_problems": retrieval.sufficiency_problems(report),
                    "document_coverage": scored["document_coverage"],
                    "section_coverage": scored["operative_section_coverage"],
                    "diagnoses": scored["diagnoses"], "invalid_hits": scored["invalid_hit_segments"],
                    "retrieval_pass": scored["retrieval_pass"]})
    return {"screened_units": screened, "questions": out}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        scorer = load("score_document_coverage")
        results = run_controls(fixture, scorer)
        replay = replay_retriever(fixture, scorer)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, StopIteration) as exc:
        print(f"invalid input: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"controls": results, "retriever_replay": replay}, indent=2))
    else:
        for r in results:
            d, s = r["document_coverage"], r["section_coverage"]
            print(f"{'OK  ' if r['ok'] else 'FAIL'} {r['control']:<44} docs {d['covered']}/{d['required']} "
                  f"sections {s['covered']}/{s['required']} {r['diagnoses']}")
        print("\nRetriever replay (default limits, not an agent query trace):")
        print("screened:", [u["unit_id"] for u in replay["screened_units"]])
        for q in replay["questions"]:
            d, s = q["document_coverage"], q["section_coverage"]
            print(f"  {q['question']}: pass={q['retrieval_pass']} docs {d['covered']}/{d['required']} "
                  f"sections {s['covered']}/{s['required']} found={q['found_units']}")
            for diag in q["diagnoses"]:
                print(f"     {diag['segment']}: {diag['reason']}")
            if q["invalid_hits"]:
                print(f"     invalid hits: {q['invalid_hits']}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
