"""Synthetic corpus controls: returned document IDs alone cannot establish coverage."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "score_document_coverage.py"
SPEC = importlib.util.spec_from_file_location("document_coverage", SCRIPT)
coverage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coverage)


@pytest.fixture
def corpus():
    return json.loads(coverage.FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture
def observed(corpus):
    return {
        "available_documents": sorted({s["document"] for s in corpus["segments"].values()}),
        "extracted_segments": {key: s["text"] for key, s in corpus["segments"].items()},
        "hits": [{"segment": key, "text": s["text"]}
                 for key, s in corpus["segments"].items() if s["text"]],
        "query_origin": "manual_golden",
        "queries": ["synthetic fixture control; no agent query was run"],
    }


def test_complete_reference_has_separate_metrics(corpus, observed):
    result = coverage.score(corpus, "maintenance-route", observed)
    assert result["retrieval_pass"] is True
    assert result["document_coverage"] == {"covered": 2, "required": 2}
    assert result["operative_section_coverage"] == {"covered": 3, "required": 3}
    assert result["agent_query_exercised"] is False
    assert result["answer_support"] == "not_scored"
    assert result["pdf_extraction"] == "not_exercised"


def test_empty_or_unknown_section_expectations_cannot_pass(corpus, observed):
    for sections in ([], ["not-in-inventory"]):
        corpus["questions"]["maintenance-route"]["required_sections"] = sections
        with pytest.raises(ValueError):
            coverage.score(corpus, "maintenance-route", observed)


def test_agent_origin_without_recorded_queries_is_not_execution_evidence(corpus, observed):
    observed["query_origin"] = "agent"
    for queries in ([], [""], None):
        observed["queries"] = queries
        result = coverage.score(corpus, "maintenance-route", observed)
        assert result["agent_query_exercised"] is False


def test_main_document_only_fails_supplement_question(corpus, observed):
    observed["hits"] = [hit for hit in observed["hits"]
                        if corpus["segments"][hit["segment"]]["document"] == "main-policy"]
    result = coverage.score(corpus, "maintenance-route", observed)
    assert result["retrieval_pass"] is False
    assert result["document_coverage"] == {"covered": 1, "required": 2}
    assert result["operative_section_coverage"] == {"covered": 2, "required": 3}
    assert result["diagnoses"][0]["reason"] == "query_miss"


def test_contents_hit_is_not_an_operative_section(corpus, observed):
    observed["hits"] = [observed["hits"][0]]
    result = coverage.score(corpus, "complete-table", observed)
    assert result["document_coverage"] == {"covered": 1, "required": 1}
    assert result["operative_section_coverage"] == {"covered": 0, "required": 1}


def test_multi_page_table_requires_continuation(corpus, observed):
    observed["hits"] = [h for h in observed["hits"] if h["segment"] != "table-continuation"]
    result = coverage.score(corpus, "complete-table", observed)
    assert result["retrieval_pass"] is False
    assert result["operative_section_coverage"]["covered"] == 0
    assert result["diagnoses"] == [{"segment": "table-continuation", "document": "main-policy",
                                    "page": 4, "reason": "query_miss"}]


@pytest.mark.parametrize("failure", ["absent_content", "empty_extraction", "section_truncation"])
def test_missing_extraction_reasons_remain_distinct(corpus, observed, failure):
    key = "maintenance-exception"
    observed["hits"] = [h for h in observed["hits"] if h["segment"] != key]
    if failure == "absent_content":
        observed["available_documents"].remove("supplement-s1")
    elif failure == "empty_extraction":
        observed["extracted_segments"][key] = ""
    else:
        observed["extracted_segments"][key] = "Supplement S1."
    result = coverage.score(corpus, "maintenance-route", observed)
    assert result["retrieval_pass"] is False
    assert result["diagnoses"][0]["reason"] == failure
    assert result["evidence_result"] == "unresolved_evidence"


def test_valid_but_truncated_hit_fails(corpus, observed):
    observed["hits"][-1]["text"] = "Supplement S1."
    result = coverage.score(corpus, "maintenance-route", observed)
    assert result["retrieval_pass"] is False
    assert result["invalid_hit_segments"] == []
    assert result["diagnoses"][0]["reason"] == "section_truncation"


def test_unrelated_text_cannot_buy_document_coverage(corpus, observed):
    observed["hits"][-1]["text"] = "There is an exception somewhere."
    result = coverage.score(corpus, "maintenance-route", observed)
    assert result["retrieval_pass"] is False
    assert result["invalid_hit_segments"] == ["maintenance-exception"]
    assert result["document_coverage"]["covered"] == 1


def test_image_only_empty_extraction_is_unresolved_even_if_review_claimed(corpus, observed):
    observed["visual_reviews"] = [{"segment": "closure-notice", "status": "reviewed"}]
    result = coverage.score(corpus, "closure-status", observed)
    assert result["retrieval_pass"] is False
    assert {d["reason"] for d in result["diagnoses"]} == {"empty_extraction", "unviewed_visuals"}
    assert result["evidence_result"] == "unresolved_evidence"


def test_cli_reports_failure_with_nonzero_exit(corpus, observed, tmp_path):
    observation_path = tmp_path / "observation.json"
    observation_path.write_text(json.dumps(observed), encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPT), "--question", "closure-status",
                             "--observation", str(observation_path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)["evidence_result"] == "unresolved_evidence"
