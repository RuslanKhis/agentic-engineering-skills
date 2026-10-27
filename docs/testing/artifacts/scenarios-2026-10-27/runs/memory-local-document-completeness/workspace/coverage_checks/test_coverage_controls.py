"""Offline controls for missing-evidence diagnosis, using the skill's synthetic fixture.

Run (from outside this directory, isolated mode):
    python -I -m unittest discover -s coverage_checks -p 'test_*.py'
Observations are authored adapter records, not real retriever or PDF output.
Expected sections stay in the fixture's `questions` block (evaluator side).
"""
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / ".claude" / "skills" / "adk-memory-architecture"


def _load_scorer():
    spec = importlib.util.spec_from_file_location(
        "score_document_coverage", SKILL / "scripts" / "score_document_coverage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORER = _load_scorer()
FIXTURE = json.loads((SKILL / "assets" / "document-coverage.json").read_text(encoding="utf-8"))
SEGMENTS = FIXTURE["segments"]
ALL_DOCS = ["main-policy", "supplement-s1", "notice-n1"]


def observation(hit_keys, extracted=None, documents=None, queries=("manual control query",)):
    """Build an adapter-style observation; hits carry the full extracted passage."""
    if extracted is None:
        extracted = {key: seg["text"] for key, seg in SEGMENTS.items()}
    return {
        "available_documents": list(ALL_DOCS if documents is None else documents),
        "extracted_segments": extracted,
        "hits": [{"segment": key, "text": SEGMENTS[key]["text"]} for key in hit_keys],
        "query_origin": "manual_golden",
        "queries": list(queries),
    }


def reasons(report):
    return {(d["segment"], d["reason"]) for d in report["diagnoses"]}


class CoverageControls(unittest.TestCase):
    def score(self, question, obs):
        return SCORER.score(FIXTURE, question, obs)

    def test_honest_complete_text_control_passes(self):
        report = self.score("maintenance-route", observation(
            ["route-rule", "table-first", "table-continuation", "maintenance-exception"]))
        self.assertTrue(report["retrieval_pass"])
        self.assertEqual(report["document_coverage"], {"covered": 2, "required": 2})
        self.assertEqual(report["operative_section_coverage"], {"covered": 3, "required": 3})
        self.assertEqual(report["diagnoses"], [])
        self.assertEqual(report["evidence_result"], "complete_fixture_spans")
        # A manual run is not agent evidence.
        self.assertFalse(report["agent_query_exercised"])

    def test_main_policy_only_misses_supplement_exception(self):
        report = self.score("maintenance-route", observation(
            ["route-rule", "table-first", "table-continuation"]))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(report["document_coverage"], {"covered": 1, "required": 2})
        self.assertEqual(report["operative_section_coverage"], {"covered": 2, "required": 3})
        self.assertEqual(reasons(report), {("maintenance-exception", "query_miss")})

    def test_main_only_corpus_reports_absent_supplement(self):
        extracted = {k: v["text"] for k, v in SEGMENTS.items() if v["document"] == "main-policy"}
        report = self.score("maintenance-route", observation(
            ["route-rule", "table-first", "table-continuation"],
            extracted=extracted, documents=["main-policy"]))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(reasons(report), {("maintenance-exception", "absent_content")})

    def test_contents_only_hit_counts_as_document_hit_only(self):
        report = self.score("maintenance-route", observation(["contents"]))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(report["document_coverage"], {"covered": 1, "required": 2})
        self.assertEqual(report["operative_section_coverage"], {"covered": 0, "required": 3})
        self.assertEqual(
            {seg for seg, reason in reasons(report) if reason == "query_miss"},
            {"route-rule", "table-first", "table-continuation", "maintenance-exception"})

    def test_first_table_page_only_is_incomplete(self):
        report = self.score("complete-table", observation(["table-first"]))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(report["operative_section_coverage"], {"covered": 0, "required": 1})
        self.assertEqual(reasons(report), {("table-continuation", "query_miss")})

    def test_truncated_continuation_passage_is_not_complete(self):
        obs = observation(["table-first", "table-continuation"])
        obs["hits"][1]["text"] = SEGMENTS["table-continuation"]["text"][:60]
        report = self.score("complete-table", obs)
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(reasons(report), {("table-continuation", "section_truncation")})

    def test_truncated_extraction_is_diagnosed_before_query(self):
        extracted = {k: v["text"] for k, v in SEGMENTS.items()}
        extracted["table-continuation"] = extracted["table-continuation"][:60]
        report = self.score("complete-table", observation(["table-first"], extracted=extracted))
        self.assertEqual(reasons(report), {("table-continuation", "section_truncation")})

    def test_empty_text_page_is_empty_extraction_not_no_provision(self):
        extracted = {k: v["text"] for k, v in SEGMENTS.items()}
        extracted["maintenance-exception"] = ""
        report = self.score("maintenance-route", observation(
            ["route-rule", "table-first", "table-continuation"], extracted=extracted))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(reasons(report), {("maintenance-exception", "empty_extraction")})

    def test_empty_image_page_is_unresolved_with_two_diagnoses(self):
        extracted = {k: v["text"] for k, v in SEGMENTS.items()}
        report = self.score("closure-status", observation([], extracted=extracted))
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(report["evidence_result"], "unresolved_evidence")
        self.assertEqual(reasons(report), {("closure-notice", "empty_extraction"),
                                           ("closure-notice", "unviewed_visuals")})

    def test_claimed_review_cannot_resolve_image_page(self):
        obs = observation([])
        obs["visual_review_claimed"] = True  # unauthenticated model assertion
        obs["hits"] = [{"segment": "closure-notice", "text": "Route Cedar is closed."}]
        report = self.score("closure-status", obs)
        self.assertFalse(report["retrieval_pass"])
        self.assertIn(("closure-notice", "unviewed_visuals"), reasons(report))
        self.assertIn("closure-notice", report["invalid_hit_segments"])

    def test_fabricated_hit_text_is_invalid(self):
        obs = observation(["route-rule", "table-first", "table-continuation"])
        obs["hits"].append({"segment": "maintenance-exception", "text": "Any raised route may be 1.0 m."})
        report = self.score("maintenance-route", obs)
        self.assertFalse(report["retrieval_pass"])
        self.assertEqual(report["invalid_hit_segments"], ["maintenance-exception"])

    def test_irrelevant_neighbour_does_not_raise_coverage(self):
        report = self.score("complete-table", observation(["contents", "route-rule", "table-first"]))
        self.assertEqual(report["operative_section_coverage"], {"covered": 0, "required": 1})

    def test_agent_origin_requires_recorded_queries(self):
        obs = observation(["table-first", "table-continuation"], queries=[])
        obs["query_origin"] = "agent"
        self.assertFalse(self.score("complete-table", obs)["agent_query_exercised"])

    def test_expected_sections_are_not_in_segment_records(self):
        # Retriever input is segments only; required_sections live under `questions`.
        for seg in SEGMENTS.values():
            self.assertNotIn("required_sections", seg)


if __name__ == "__main__":
    unittest.main()
