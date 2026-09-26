"""Exercise the actual synthetic checker and JSON boundary, with no inference."""

import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import review


ROOT = Path(__file__).parent


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((ROOT / "reference.json").read_text())
        # Fail any accidental socket creation in either execution path.
        self.network = patch("socket.socket", side_effect=AssertionError("network forbidden"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def assert_boundary(self, accepted, expected_error=None):
        before = copy.deepcopy(self.case)
        errors = review.check(**self.case)
        response = json.loads(review.serve(json.dumps(self.case)))
        self.assertEqual(response, {"accepted": accepted, "errors": errors})
        self.assertEqual(not errors, accepted)
        if expected_error:
            self.assertIn(expected_error, errors)
        self.assertEqual(self.case, before)
        # Repeat invocation must be deterministic and must not mutate the request.
        self.assertEqual(response, json.loads(review.serve(json.dumps(self.case))))

    def test_truthful_refusal_accounts_for_independent_roof(self):
        self.assert_boundary(True)

    def test_original_case_still_requires_an_actual_roof_assessment(self):
        self.case = json.loads((ROOT / "case.json").read_text())
        self.assert_boundary(False, "issue coverage")

    def test_decisive_refusal_alone_preserves_existing_interface(self):
        del self.case["issues"]["roof"]
        del self.case["review"]["issue_dispositions"]
        self.assert_boundary(True)

    def test_roof_cannot_be_attached_to_access_reason(self):
        self.case["review"]["issue_dispositions"] = []
        self.case["review"]["claims"][0]["issue_ids"].append("roof")
        self.case["review"]["claims"][0]["evidence"].append("roof-report")
        self.assert_boundary(False, "claim issue association")

    def test_resolved_roof_cannot_be_a_gap(self):
        self.case["review"]["issue_dispositions"] = []
        self.case["review"]["gaps"] = [{"issue_id": "roof"}]
        self.assert_boundary(False, "not an unresolved gap")

    def test_fabricated_claim_fails(self):
        self.case["review"]["claims"].append({
            "claim_id": "reason-roof", "issue_ids": ["roof"],
            "support": "supported", "evidence": ["roof-report"],
        })
        self.case["review"]["issue_dispositions"] = []
        self.assert_boundary(False, "claim identity")

    def test_wrong_claim_evidence_fails(self):
        self.case["review"]["claims"][0]["evidence"] = ["roof-report"]
        self.assert_boundary(False, "claim evidence identity")

    def test_missing_claim_evidence_fails(self):
        self.case["review"]["claims"][0]["evidence"] = []
        self.assert_boundary(False, "missing claim evidence")

    def test_missing_or_wrong_independent_evidence_fails(self):
        for evidence in ([], ["access-report"], ["invented-report"]):
            with self.subTest(evidence=evidence):
                self.case["review"]["issue_dispositions"][0]["evidence"] = evidence
                self.assert_boundary(False, "issue evidence identity")

    def test_registered_required_evidence_cannot_be_omitted(self):
        self.case["issues"]["access"]["source_ids"].append("required-control-report")
        self.assert_boundary(False, "missing required issue evidence")

    def test_support_judgments_must_be_positive(self):
        for support in ("unsupported", "uncertain", "contradicted"):
            with self.subTest(support=support):
                self.case["review"]["claims"][0]["support"] = support
                self.assert_boundary(False, "unsupported claim")
        self.case["review"]["claims"][0]["support"] = "supported"
        self.case["review"]["issue_dispositions"][0]["support"] = "uncertain"
        self.assert_boundary(False, "unsupported issue disposition")

    def test_material_issue_cannot_be_downgraded_in_review(self):
        self.case["issues"]["roof"]["material"] = True
        self.case["review"]["issue_dispositions"][0]["material"] = False
        self.assert_boundary(False, "material issue requires claim")

    def test_approval_requires_its_material_claim(self):
        self.case["draft"]["outcome"] = "approve"
        self.case["issues"]["access"]["observation"] = "Required barrier is installed."
        self.assert_boundary(True)
        self.case["review"]["claims"] = []
        self.assert_boundary(False, "claim coverage")

    def test_unresolved_material_issue_blocks_even_if_fully_cited(self):
        self.case["issues"]["access"]["resolved"] = False
        self.assert_boundary(False, "unresolved material issue")

    def test_unresolved_material_gap_cannot_authorize_release(self):
        self.case["draft"]["claims"] = []
        self.case["review"]["claims"] = []
        self.case["issues"]["access"]["resolved"] = False
        self.case["review"]["gaps"] = [{"issue_id": "access"}]
        self.assert_boundary(False, "unresolved material issue")

    def test_unresolved_nonmaterial_gap_preserves_existing_contract(self):
        self.case["issues"]["roof"]["resolved"] = False
        self.case["review"]["issue_dispositions"] = []
        self.case["review"]["gaps"] = [{"issue_id": "roof"}]
        self.assert_boundary(True)

    def test_duplicate_or_unknown_independent_dispositions_fail(self):
        self.case["review"]["issue_dispositions"] *= 2
        self.assert_boundary(False, "duplicate issue disposition")
        self.case["review"]["issue_dispositions"] = [{"issue_id": "invented"}]
        self.assert_boundary(False, "unknown issue")

    def test_missing_and_duplicate_claims_fail(self):
        self.case["review"]["claims"] *= 2
        self.assert_boundary(False, "claim identity")
        self.case["review"]["claims"] = []
        self.assert_boundary(False, "claim coverage")


if __name__ == "__main__":
    unittest.main()
