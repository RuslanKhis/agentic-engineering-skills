"""Offline controls for missing-evidence diagnosis (grader side).

Expected diagnoses live here, with the grader; the retriever never sees them.
Observations are hand-built adapter records from the synthetic fixture, so
every run is `query_origin: manual_golden`, not agent evidence. No PDF parsing,
OCR or visual review is exercised.

Run: python3 -I checks/coverage_controls.py [path/to/document-coverage.json]
Exit 0 when every control behaves as expected, 1 otherwise, 2 on unreadable input.
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORER = ROOT / ".claude/skills/adk-memory-architecture/scripts/score_document_coverage.py"
DEFAULT_FIXTURE = ROOT / "document-coverage.json"

DOCS = ["main-policy", "supplement-s1", "notice-n1"]


def load_scorer():
    spec = importlib.util.spec_from_file_location("score_document_coverage", SCORER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observation(fixture, hits, *, documents=DOCS, extracted=None, partial=None, **extra):
    """Adapter record: full extraction unless overridden; hits are whole segments
    unless `partial` maps a segment to a shorter returned passage."""
    segs = fixture["segments"]
    if extracted is None:
        extracted = {key: seg["text"] for key, seg in segs.items()
                     if seg["document"] in documents}
    partial = partial or {}
    return {
        "available_documents": list(documents),
        "extracted_segments": extracted,
        "hits": [{"segment": key, "text": partial.get(key, segs[key]["text"])} for key in hits],
        "query_origin": "manual_golden",
        "queries": ["golden query for " + ",".join(hits) if hits else "no results"],
        **extra,
    }


def controls(fixture):
    """(name, question, observation, expect_pass, expected {segment: {reasons}},
    expected (document_covered, section_covered))."""
    segs = fixture["segments"]
    full = ["route-rule", "table-first", "table-continuation", "maintenance-exception"]
    no_s1 = ["main-policy"]
    prefix = segs["table-continuation"]["text"][:40]
    empty_rule = {k: v["text"] for k, v in segs.items() if k != "closure-notice"}
    empty_rule["route-rule"] = ""
    empty_closure = {k: v["text"] for k, v in segs.items()}
    return [
        ("complete_text_control", "maintenance-route", observation(fixture, full),
         True, {}, (2, 3)),
        ("complete_table_control", "complete-table",
         observation(fixture, ["table-first", "table-continuation"]), True, {}, (1, 1)),
        # Main policy returned for every question: no supplementary exception.
        ("main_policy_only", "maintenance-route",
         observation(fixture, ["route-rule", "table-first", "table-continuation"]),
         False, {"maintenance-exception": {"query_miss"}}, (1, 2)),
        # Supplement never ingested: absent, not a query problem.
        ("supplement_not_ingested", "maintenance-route",
         observation(fixture, ["route-rule", "table-first", "table-continuation"],
                     documents=no_s1),
         False, {"maintenance-exception": {"absent_content"}}, (1, 2)),
        # Contents hit is a document hit only; no operative section arrives.
        ("contents_only", "maintenance-route", observation(fixture, ["contents"]),
         False, {"route-rule": {"query_miss"}, "table-first": {"query_miss"},
                 "table-continuation": {"query_miss"},
                 "maintenance-exception": {"query_miss"}}, (1, 0)),
        # Two-page table with only page 3 returned.
        ("partial_table_first_page", "complete-table",
         observation(fixture, ["table-first"]),
         False, {"table-continuation": {"query_miss"}}, (1, 0)),
        # Continuation returned but cut short.
        ("partial_table_truncated_hit", "complete-table",
         observation(fixture, ["table-first", "table-continuation"],
                     partial={"table-continuation": prefix}),
         False, {"table-continuation": {"section_truncation"}}, (1, 0)),
        # Present page extracted to "": do not infer no provision.
        ("empty_extraction_rule", "maintenance-route",
         observation(fixture, ["table-first", "table-continuation", "maintenance-exception"],
                     extracted=empty_rule),
         False, {"route-rule": {"empty_extraction"}}, (2, 2)),
        # Image-only page: empty text and no completed review.
        ("empty_image_page", "closure-status",
         observation(fixture, [], extracted=empty_closure),
         False, {"closure-notice": {"empty_extraction", "unviewed_visuals"}}, (0, 0)),
        # A claimed review is not a receipt; the text-only pack stays unresolved.
        ("claimed_visual_review_ignored", "closure-status",
         observation(fixture, [], extracted=empty_closure, visual_review="completed"),
         False, {"closure-notice": {"empty_extraction", "unviewed_visuals"}}, (0, 0)),
    ]


def main(argv):
    try:
        path = Path(argv[1]) if len(argv) > 1 else DEFAULT_FIXTURE
        fixture = json.loads(path.read_text(encoding="utf-8"))
        scorer = load_scorer()
        cases = controls(fixture)
        failures = []
        for name, question, obs, expect_pass, expected, (docs, secs) in cases:
            report = scorer.score(fixture, question, obs)
            got = {}
            for item in report["diagnoses"]:
                got.setdefault(item["segment"], set()).add(item["reason"])
            problems = []
            if report["retrieval_pass"] != expect_pass:
                problems.append(f"retrieval_pass={report['retrieval_pass']}")
            if got != expected:
                problems.append(f"diagnoses {got} != {expected}")
            if report["document_coverage"]["covered"] != docs:
                problems.append(f"document coverage {report['document_coverage']}")
            if report["operative_section_coverage"]["covered"] != secs:
                problems.append(f"section coverage {report['operative_section_coverage']}")
            if report["agent_query_exercised"]:
                problems.append("manual run counted as agent evidence")
            if report["invalid_hit_segments"]:
                problems.append(f"invalid hits {report['invalid_hit_segments']}")
            print(f"{'ok  ' if not problems else 'FAIL'} {name}"
                  + ("" if not problems else ": " + "; ".join(problems)))
            if problems:
                failures.append(name)
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(f"invalid input: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(f"{len(cases) - len(failures)}/{len(cases)} controls behaved as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
