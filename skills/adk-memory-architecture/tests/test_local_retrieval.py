"""Local retrieval controls: operative units, named references, one bounded second round."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local_retrieval.py"
SPEC = importlib.util.spec_from_file_location("local_retrieval", SCRIPT)
retrieval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(retrieval)

if not retrieval.fts5_available():
    pytest.skip("SQLite FTS5 is unavailable in this interpreter", allow_module_level=True)

H3 = "synthetic-local-plan:policy-h3-residential-extensions"
T2 = "synthetic-local-plan:policy-t2-parking"
D1 = "synthetic-local-plan:policy-d1-design-quality"
G4 = "synthetic-local-plan:policy-g4-gates-and-boundaries"
SPD_INTRO = "design-spd:design-spd"
TABLE_2 = "design-spd:table-2-minimum-visibility-splays"


@pytest.fixture
def fixture():
    return json.loads(retrieval.GOLD.read_text(encoding="utf-8"))


@pytest.fixture
def units(fixture):
    return retrieval.chunk_by_heading(retrieval.fixture_pages(fixture))


@pytest.fixture
def index(units):
    kept, _ = retrieval.screen_units(units)
    conn = retrieval.build_index(kept)
    yield conn
    conn.close()


def unit_ids(hits):
    return [hit["unit_id"] for hit in hits]


def test_two_page_policy_is_one_unit_with_a_page_span(units):
    by_id = {unit["unit_id"]: unit for unit in units}
    h3 = by_id[H3]
    assert (h3["page_start"], h3["page_end"]) == (2, 3)
    assert "Side extensions" in h3["text"] and "two-storey" in h3["text"]
    assert by_id[G4]["page_start"] == by_id[G4]["page_end"] == 4


def test_contents_entries_do_not_become_units(units):
    assert not any(unit["heading"].endswith(", page 2") for unit in units)
    assert len(units) == 8


def test_contents_and_monitoring_are_screened_and_listed(units):
    kept, screened = retrieval.screen_units(units)
    assert {item["unit_id"] for item in screened} == {
        "synthetic-local-plan:contents", "synthetic-local-plan:monitoring-framework"}
    assert all(item["reason"] for item in screened)
    assert {unit["unit_id"] for unit in kept} == {H3, T2, D1, G4, SPD_INTRO, TABLE_2}


def test_reference_resolution_finds_table_and_spd(units):
    g4 = next(unit for unit in units if unit["unit_id"] == G4)
    assert retrieval.resolve_references(g4["text"]) == ["Table 2", "Design SPD"]
    assert retrieval.resolve_references("see Policy H 3, Figure 4 and Appendix B") == [
        "Policy H3", "Figure 4", "Appendix B"]


def test_lookup_reference_is_deterministic(index):
    assert unit_ids(retrieval.lookup_reference(index, "Table 2")) == [TABLE_2]
    assert unit_ids(retrieval.lookup_reference(index, "Design SPD")) == [SPD_INTRO, TABLE_2]
    assert retrieval.lookup_reference(index, "Table 20") == []
    assert retrieval.lookup_reference(index, "Appendix Z") == []


def test_issue_retrieval_resolves_the_cited_spd_table(index):
    report = retrieval.retrieve_for_issues(
        index, [{"id": "splay", "query": "visibility splay for a gate on a classified road"}], k=2)
    entry = report["issues"]["splay"]
    assert TABLE_2 in unit_ids(entry["found"]) and G4 in unit_ids(entry["found"])
    assert entry["resolved_references"]["Table 2"] == [TABLE_2]
    assert entry["unresolved_references"] == []
    assert retrieval.sufficiency_problems(report) == []


def test_issue_without_operative_text_reports_none_found(index):
    report = retrieval.retrieve_for_issues(index, ["wind turbine noise limits"], k=3)
    entry = report["issues"]["issue-1"]
    assert entry["found"] == "none_found"
    assert entry["rounds"] == 2 and report["second_round_ran"] is True
    assert retrieval.sufficiency_problems(report) == ["issue-1: none_found"]


def test_unresolved_reference_survives_the_single_second_round(index):
    report = retrieval.retrieve_for_issues(
        index, ["gate visibility under Policy G4 and Appendix Z"], k=2)
    entry = report["issues"]["issue-1"]
    assert entry["rounds"] == 2
    assert entry["unresolved_references"] == ["Appendix Z"]
    assert "issue-1: unresolved reference Appendix Z" in retrieval.sufficiency_problems(report)
    assert report["queries_run"] == 2  # one query per round, never a third


def test_call_budget_stops_dispatch_and_is_reported(index):
    report = retrieval.retrieve_for_issues(index, ["parking spaces", "rear extension"], k=3, call_budget=1)
    assert report["calls_run"] == 1 and report["budget_exhausted"] is True
    assert report["second_round_ran"] is False
    assert report["issues"]["issue-2"]["skipped"] == "budget_exhausted"
    problems = retrieval.sufficiency_problems(report)
    assert "issue-2: not searched (budget_exhausted)" in problems
    assert "call budget exhausted before every issue was served" in problems


def test_rrf_prefers_presence_in_both_lists():
    fused = [unit_id for unit_id, _ in retrieval.rrf([["a", "b", "c"], ["b", "d"]])]
    assert fused[0] == "b" and fused.index("a") < fused.index("c")


def test_hybrid_fusion_changes_the_order_with_a_toy_embedder(index, units):
    kept, _ = retrieval.screen_units(units)
    synonyms = {"fence": "gate", "fences": "gate", "gates": "gate"}

    def tokens(text):
        return [synonyms.get(t, t) for t in re.findall(r"[a-z]+", text.lower())]

    vocabulary = sorted({t for unit in kept for t in tokens(unit["text"])} | {"gate"})

    def embed(text):
        counts = tokens(text)
        return [counts.count(term) for term in vocabulary]

    vectors = {unit["unit_id"]: embed(unit["heading"] + " " + unit["text"]) for unit in kept}
    assert retrieval.search_lexical(index, "fence", 3) == []
    hybrid = unit_ids(retrieval.search_hybrid(index, "fence", 3, embed=embed, unit_vectors=vectors))
    assert hybrid[0] == G4
    assert unit_ids(retrieval.search_hybrid(index, "fence", 3)) == []


def test_lexical_run_recall_on_the_gold_set(fixture, index):
    issues = [{"id": qid, "query": q["question"]} for qid, q in fixture["questions"].items()]
    report = retrieval.retrieve_for_issues(index, issues, k=3)
    recall = retrieval.recall_at_k(fixture["questions"], retrieval.found_unit_ids(report))
    assert recall["per_question"] == {"visibility-splay": 1.0, "rear-extension": 1.0,
                                      "parking-spaces": 1.0, "external-materials": 1.0}
    assert recall["mean"] == 1.0
    assert retrieval.sufficiency_problems(report) == []
    with pytest.raises(ValueError):
        retrieval.recall_at_k({"q": {"required_units": []}}, {})


def test_precision_and_irrelevant_hits_expose_ranking_noise(fixture, index):
    issues = [{"id": qid, "query": q["question"]} for qid, q in fixture["questions"].items()]
    results = retrieval.found_unit_ids(retrieval.retrieve_for_issues(index, issues, k=4))
    precision = retrieval.precision_at_k(fixture["questions"], results)
    assert precision["per_question"] == {"visibility-splay": 0.5, "rear-extension": 0.25,
                                         "parking-spaces": 1.0,
                                         "external-materials": pytest.approx(1 / 6)}
    assert precision["mean"] == pytest.approx((0.5 + 0.25 + 1.0 + 1 / 6) / 4)
    noise = retrieval.irrelevant_hits(fixture["questions"], results)
    assert noise["visibility-splay"] == [{"unit_id": T2, "rank": 3}, {"unit_id": SPD_INTRO, "rank": 4}]
    assert noise["parking-spaces"] == []
    # Noise is reported beside recall; it never changes sufficiency.
    report = retrieval.retrieve_for_issues(index, issues, k=4)
    assert retrieval.sufficiency_problems(report) == []
    clean = retrieval.irrelevant_hits(fixture["questions"], {"visibility-splay": [TABLE_2, G4]})
    assert clean["visibility-splay"] == []
    assert retrieval.precision_at_k(fixture["questions"], {"visibility-splay": [TABLE_2, G4]})[
        "per_question"]["visibility-splay"] == 1.0
    assert retrieval.precision_at_k(fixture["questions"], {})["per_question"]["rear-extension"] == 0.0


def test_recall_counts_missing_required_units(fixture):
    recall = retrieval.recall_at_k(fixture["questions"], {"visibility-splay": [G4], "parking-spaces": [T2]})
    assert recall["per_question"]["visibility-splay"] == 0.5
    assert recall["per_question"]["rear-extension"] == 0.0
    assert recall["mean"] == pytest.approx((0.5 + 0 + 1 + 0) / 4)


def test_four_truncated_searches_without_a_second_round_fail():
    observation = {
        "second_round_ran": False, "budget_exhausted": False,
        "issues": {f"issue-{i}": {"found": [{"unit_id": T2}], "truncated": True,
                                  "unresolved_references": ["Table 2"] if i == 4 else []}
                   for i in range(1, 5)},
    }
    problems = retrieval.sufficiency_problems(observation)
    assert len([p for p in problems if "truncated search without a second round" in p]) == 4
    assert "issue-4: unresolved reference Table 2" in problems


def test_cli_reports_recall_and_rejects_bad_issues(tmp_path):
    completed = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--k", "3"],
                               capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    output = json.loads(completed.stdout)
    assert output["recall"]["mean"] == 1.0 and output["problems"] == []
    assert output["precision"]["per_question"]["visibility-splay"] == 0.5
    assert [hit["unit_id"] for hit in output["irrelevant_hits"]["visibility-splay"]] == [T2, SPD_INTRO]
    assert [s["unit_id"] for s in output["screened_units"]] == [
        "synthetic-local-plan:contents", "synthetic-local-plan:monitoring-framework"]
    bad = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "--issues", '["", 3]'],
                         capture_output=True, text=True, check=False)
    assert bad.returncode == 1 and "invalid input" in bad.stderr
