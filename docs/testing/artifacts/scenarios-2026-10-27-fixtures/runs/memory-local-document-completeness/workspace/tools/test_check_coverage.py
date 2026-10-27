import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_coverage as cc

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "document-coverage.json").read_text(encoding="utf-8"))
SCORER = cc._load("score_document_coverage")


def obs(hit_keys, fixture=FIXTURE, extracted=None):
    segs = fixture["segments"]
    return {"available_documents": sorted({s["document"] for s in segs.values()}),
            "extracted_segments": extracted or {k: s["text"] for k, s in segs.items()},
            "hits": [{"segment": k, "text": segs[k]["text"]} for k in hit_keys],
            "query_origin": "manual_golden", "queries": ["q"]}


def reasons(report):
    return {(d["segment"], d["reason"]) for d in report["diagnoses"]}


def test_complete_spans_pass():
    keys = ["route-rule", "table-first", "table-continuation", "maintenance-exception"]
    assert SCORER.score(FIXTURE, "maintenance-route", obs(keys))["retrieval_pass"]


def test_main_only_fails_supplement_question():
    report = SCORER.score(FIXTURE, "maintenance-route", obs(["route-rule", "table-continuation"]))
    assert not report["retrieval_pass"]
    assert ("maintenance-exception", "query_miss") in reasons(report)
    assert ("table-first", "query_miss") in reasons(report)  # partial table


def test_contents_only_is_not_coverage():
    report = SCORER.score(FIXTURE, "complete-table", obs(["contents"]))
    assert not report["retrieval_pass"]


def test_empty_extraction_not_a_query_miss():
    extracted = {k: s["text"] for k, s in FIXTURE["segments"].items()}
    extracted["maintenance-exception"] = ""
    report = SCORER.score(FIXTURE, "maintenance-route", obs([], extracted=extracted))
    assert ("maintenance-exception", "empty_extraction") in reasons(report)


def test_unviewed_visual_always_unresolved():
    report = SCORER.score(FIXTURE, "closure-status", obs(["closure-notice"]))
    assert {"empty_extraction", "unviewed_visuals"} <= {r for _, r in reasons(report)}
    assert not report["retrieval_pass"]


def test_preflight_flags_empty_visual_and_missing_continuation():
    reasons_found = {f["reason"] for f in cc.preflight(FIXTURE)}
    assert {"empty_extraction", "unviewed_visuals"} <= reasons_found
    broken = copy.deepcopy(FIXTURE)
    del broken["segments"]["table-continuation"]
    assert any(f["reason"] == "absent_content" for f in cc.preflight(broken))
    del broken["segments"]["maintenance-exception"]
    assert any("Supplement S1" in f.get("detail", "") for f in cc.preflight(broken))


def test_run_does_not_pass_with_unresolved_notice():
    report = cc.run(FIXTURE)
    closure = next(q for q in report["questions"] if q["question"] == "closure-status")
    assert not closure["retrieval_pass"]
