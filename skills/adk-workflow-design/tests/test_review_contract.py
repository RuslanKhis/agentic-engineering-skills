"""Synthetic contract regressions; no SDK, network, provider or quality claims."""

from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review_contract.py"
SPEC = importlib.util.spec_from_file_location("review_contract", SCRIPT)
contract = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = contract
SPEC.loader.exec_module(contract)


def broken_claim_only_checker(claim_ids, resolved, reviews, gaps):
    """Retained failing design: issue coverage can be laundered through any claim.

    This test-only checker intentionally cannot express a resolved, nondecisive
    issue independently of a draft claim. It is a reproducer, never release code.
    """
    covered = set()
    for claim_id, issue_ids in reviews:
        if claim_id not in claim_ids:
            return "claim_identity"
        covered.update(issue_ids)
    for issue_id in gaps:
        if resolved[issue_id]:
            return "resolved_gap"
        covered.add(issue_id)
    return "accepted" if set(resolved) <= covered else "issue_coverage"


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        # Entirely invented premises; substantive expectations are fixed here.
        self.evidence = (
            contract.Evidence("exit-note", "The only exit is obstructed."),
            contract.Evidence("paint-note", "The sign colour complies with the specified palette."),
        )
        self.issues = (
            contract.Issue("exit", "Is the exit usable?", ("exit-note",)),
            contract.Issue("paint", "Is the sign colour acceptable?", ("paint-note",),
                           material=False),
        )
        self.draft = contract.Draft(
            "draft-1", "refuse", (contract.Claim(
                "exit-refusal", "Refuse because the only exit is obstructed.",
                ("exit",), ("exit-note",)),))

    def reference(self, draft=None, issues=None, evidence=None):
        frame = contract.compile_frame(draft or self.draft, issues or self.issues,
                                       evidence or self.evidence)
        return {"frame_id": frame["frame_id"],
                "claims": {key: {"judgment": "supported", "evidence": {
                    source: "supports" for source in slot["evidence"]}}
                    for key, slot in frame["claims"].items()},
                "issues": {key: {"judgment": "adverse" if slot["identity"] == "exit"
                                 else "acceptable", "evidence": {
                                     source: "supports" for source in slot["evidence"]}}
                           for key, slot in frame["issues"].items()}}

    def consume(self, review, draft=None, issues=None, evidence=None, limit=10000):
        return contract.consume_review(json.dumps(review), draft or self.draft,
                                       issues or self.issues, evidence or self.evidence,
                                       max_output_bytes=limit)

    def test_retained_broken_checker_reproduces_five_paths(self):
        claims = {"exit-refusal"}
        honest = [("exit-refusal", ("exit",))]
        self.assertEqual(broken_claim_only_checker(claims, {"exit": True}, honest, []),
                         "accepted")
        resolved = {"exit": True, "paint": True}
        self.assertEqual(broken_claim_only_checker(claims, resolved, honest, []),
                         "issue_coverage")
        self.assertEqual(broken_claim_only_checker(claims, resolved, honest, ["paint"]),
                         "resolved_gap")
        self.assertEqual(broken_claim_only_checker(
            claims, resolved, honest + [("invented-paint-claim", ("paint",))], []),
            "claim_identity")
        self.assertEqual(broken_claim_only_checker(
            claims, resolved, [("exit-refusal", ("exit", "paint"))], []), "accepted")

    def test_adding_separately_acceptable_issue_preserves_honest_refusal(self):
        original = self.reference(issues=self.issues[:1])
        before = self.consume(original, issues=self.issues[:1])
        expanded = self.reference()
        after = self.consume(expanded)
        self.assertTrue(before["publishable"])
        self.assertTrue(after["publishable"])
        self.assertEqual(original["claims"], expanded["claims"])
        self.assertEqual(expanded["issues"]["i2"]["judgment"], "acceptable")

    def test_model_cannot_attach_unrelated_issue_or_source_to_claim(self):
        for field, value in (("issue_ids", ["exit", "paint"]),
                             ("source_ids", ["exit-note", "paint-note"])):
            with self.subTest(field=field):
                review = self.reference()
                review["claims"]["c1"][field] = value
                with self.assertRaises(contract.ContractError):
                    self.consume(review)

    def test_missing_duplicate_and_invented_slots_fail(self):
        for section, key in (("claims", "c1"), ("issues", "i2")):
            review = self.reference()
            del review[section][key]
            with self.assertRaises(contract.ContractError):
                self.consume(review)
            review = self.reference()
            review[section]["invented"] = review[section][key]
            with self.assertRaises(contract.ContractError):
                self.consume(review)
        review = self.reference()
        del review["issues"]["i2"]["evidence"]["s1"]
        with self.assertRaises(contract.ContractError):
            self.consume(review)
        raw = json.dumps(self.reference())
        raw = raw.replace('"judgment": "supported"',
                          '"judgment": "supported", "judgment": "supported"')
        with self.assertRaises(contract.ContractError):
            contract.consume_review(raw, self.draft, self.issues, self.evidence,
                                    max_output_bytes=10000)

    def test_draft_correction_requires_new_frame_even_at_same_revision(self):
        original = self.reference()
        corrections = (
            replace(self.draft, revision="draft-2"),
            replace(self.draft, claims=(replace(self.draft.claims[0], text="Revised reason."),)),
            replace(self.draft, controls=("new-control",)),
        )
        for draft in corrections:
            with self.subTest(draft=draft):
                with self.assertRaises(contract.ContractError):
                    self.consume(original, draft=draft)
                self.assertTrue(self.consume(self.reference(draft=draft), draft=draft)["accepted"])

    def test_source_or_issue_change_invalidates_frame(self):
        evidence = (replace(self.evidence[0], text="A changed observation."), self.evidence[1])
        with self.assertRaises(contract.ContractError):
            self.consume(self.reference(), evidence=evidence)
        issues = (self.issues[0], replace(self.issues[1], material=True))
        with self.assertRaises(contract.ContractError):
            self.consume(self.reference(), issues=issues)

    def approval_case(self):
        evidence = (contract.Evidence("barrier-note", "A temporary barrier controls the hazard."),)
        issues = (contract.Issue("hazard", "Can the hazard be controlled?", ("barrier-note",),
                                 required_controls=("retain-barrier",)),)
        draft = contract.Draft("approval-1", "approve", (contract.Claim(
            "barrier-condition", "Approve with the temporary barrier retained.",
            ("hazard",), ("barrier-note",)),), ("retain-barrier",))
        review = self.reference(draft, issues, evidence)
        review["issues"]["i1"]["judgment"] = "controlled"
        return draft, issues, evidence, review

    def test_approval_with_required_control_and_deleted_control_mutation(self):
        draft, issues, evidence, review = self.approval_case()
        self.assertTrue(self.consume(review, draft, issues, evidence)["publishable"])
        missing = replace(draft, controls=())
        review = self.reference(missing, issues, evidence)
        # Relabelling the issue acceptable cannot evade a server-owned obligation.
        result = self.consume(review, missing, issues, evidence)
        self.assertFalse(result["publishable"])
        self.assertIn("missing controls", " ".join(result["blockers"]))

    def test_unresolved_evidence_is_expressible_without_inventing_support(self):
        draft = contract.Draft("unresolved-1", "unresolved", ())
        issues = (contract.Issue("inspection", "Is the inspection complete?", ()),)
        review = self.reference(draft, issues)
        review["issues"]["i1"]["judgment"] = "no_relevant_evidence"
        result = self.consume(review, draft, issues)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["publishable"])
        self.assertIn("no_relevant_evidence", " ".join(result["blockers"]))

    def test_no_relevant_evidence_and_all_irrelevant_never_count_as_support(self):
        for judgment, source in (("no_relevant_evidence", "irrelevant"),
                                 ("adverse", "irrelevant"), ("adverse", "uncertain")):
            review = self.reference()
            review["issues"]["i1"] = {"judgment": judgment, "evidence": {"s1": source}}
            self.assertFalse(self.consume(review)["publishable"])
        review = self.reference()
        review["claims"]["c1"]["evidence"]["s1"] = "irrelevant"
        self.assertFalse(self.consume(review)["publishable"])

    def test_issue_uncertainty_changes_material_gate_or_nonmaterial_warning(self):
        for judgment in ("unsupported", "uncertain", "contradicted", "no_relevant_evidence"):
            with self.subTest(judgment=judgment):
                review = self.reference()
                review["issues"]["i2"]["judgment"] = judgment
                result = self.consume(review)
                self.assertTrue(result["publishable"])
                self.assertEqual(len(result["warnings"]), 1)
                material = (self.issues[0], replace(self.issues[1], material=True))
                review["frame_id"] = contract.compile_frame(
                    self.draft, material, self.evidence)["frame_id"]
                result = self.consume(review, issues=material)
                self.assertFalse(result["publishable"])

    def test_registered_contradiction_cannot_be_hidden_by_acceptable_disposition(self):
        draft, issues, evidence, review = self.approval_case()
        evidence += (contract.Evidence("barrier-absent", "The required barrier is absent."),)
        issues = (replace(issues[0], evidence_ids=("barrier-note", "barrier-absent"),
                          contrary_ids=("barrier-absent",), material=False),)
        review = self.reference(draft, issues, evidence)
        review["issues"]["i1"]["judgment"] = "contradicted"
        review["issues"]["i1"]["evidence"]["s2"] = "contradicts"
        result = self.consume(review, draft, issues, evidence)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["publishable"])
        review["issues"]["i1"]["judgment"] = "acceptable"
        review["issues"]["i1"]["evidence"]["s2"] = "supports"
        self.assertFalse(self.consume(review, draft, issues, evidence)["publishable"])

    def test_unsupported_claim_and_refusal_without_adverse_issue_fail_release(self):
        review = self.reference()
        review["claims"]["c1"]["judgment"] = "unsupported"
        self.assertFalse(self.consume(review)["publishable"])
        review = self.reference()
        review["issues"]["i1"]["judgment"] = "acceptable"
        self.assertFalse(self.consume(review)["publishable"])

    def test_exact_serialized_output_limit_and_size_measurement(self):
        review = self.reference()
        count = len(json.dumps(review).encode())
        result = self.consume(review, limit=count)
        self.assertEqual(result["sizes_bytes"]["response"], count)
        self.assertGreater(result["sizes_bytes"]["schema"], count)
        with self.assertRaises(contract.ContractError):
            self.consume(review, limit=count - 1)

    def test_server_rejects_duplicate_and_unknown_identity(self):
        with self.assertRaises(contract.ContractError):
            contract.compile_frame(self.draft, self.issues + self.issues, self.evidence)
        claim = replace(self.draft.claims[0], evidence_ids=("paint-note",))
        with self.assertRaises(contract.ContractError):
            contract.compile_frame(replace(self.draft, claims=(claim,)), self.issues, self.evidence)


if __name__ == "__main__":
    unittest.main()
