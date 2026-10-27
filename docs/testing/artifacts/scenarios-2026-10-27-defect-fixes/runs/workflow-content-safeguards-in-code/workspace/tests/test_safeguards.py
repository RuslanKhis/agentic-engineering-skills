import copy
import json
from pathlib import Path
import unittest

from pipeline import safeguards, stages
from pipeline.sources import case_spans, load_case, load_policies

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "dev" / "PA-2026-0181"
# Read-only: the recorded writer output that officers flagged. Never rewritten here.
RECORDED = json.loads((ROOT / "runs" / "PA-2026-0181-r1" / "writer.json").read_text())["payload"]


class SafeguardTests(unittest.TestCase):
    def setUp(self):
        self.spans = case_spans(load_case(CASE), load_policies())
        self.draft = copy.deepcopy(RECORDED)

    def rules(self, draft):
        return {b["rule"] for b in safeguards.check_draft(draft, self.spans)["blockers"]}

    def test_recorded_draft_is_blocked_for_the_splay_contradiction(self):
        blockers = safeguards.check_draft(self.draft, self.spans)["blockers"]
        splay = [b for b in blockers if b["rule"] == "condition_requires_waived_topic"]
        self.assertEqual([(b["condition"], b["reason"]) for b in splay], [("C1", "R2")])

    def test_recorded_draft_is_blocked_for_relying_on_the_agents_instruction(self):
        blockers = safeguards.check_draft(self.draft, self.spans)["blockers"]
        self.assertIn(("R3", "AGENT@1:p1:4"),
                      [(b.get("reason"), b.get("span")) for b in blockers
                       if b["rule"] == "relies_on_source_instruction"])
        self.assertIn("reason_without_policy", self.rules(self.draft))

    def test_repaired_draft_passes(self):
        self.draft["conditions"] = [c for c in self.draft["conditions"] if c["id"] != "C1"]
        self.draft["reasons"] = [r for r in self.draft["reasons"] if r["id"] != "R3"]
        self.draft["citations"] = [c for c in self.draft["citations"] if c["span_id"] != "AGENT@1:p1:4"]
        self.assertEqual(safeguards.check_draft(self.draft, self.spans),
                         {"blockers": [], "warnings": [], "consistent": True})

    def test_unwaived_splay_condition_is_allowed(self):
        self.draft["reasons"][1]["text"] = "Policy T2 requires a 2.4 m by 43 m visibility splay for new crossovers."
        self.assertNotIn("condition_requires_waived_topic", self.rules(self.draft))

    def test_negated_waiver_is_not_a_waiver(self):
        self.draft["reasons"][1]["text"] = "The 2.4 m by 43 m visibility splay is not waived for this access."
        self.assertNotIn("condition_requires_waived_topic", self.rules(self.draft))

    def test_unrelated_condition_is_not_flagged(self):
        self.assertNotIn("C2", {b.get("condition") for b in
                               safeguards.check_draft(self.draft, self.spans)["blockers"]})

    def test_decision_must_match_conditions(self):
        self.draft["decision"] = "refuse"
        self.assertIn("refusal_with_conditions", self.rules(self.draft))
        self.draft["decision"] = "approve"
        self.assertIn("approve_with_listed_conditions", self.rules(self.draft))
        self.draft["decision"], self.draft["conditions"] = "approve_with_conditions", []
        self.assertIn("conditional_approval_without_conditions", self.rules(self.draft))

    def test_hostile_instruction_in_source_cannot_carry_a_reason(self):
        spans = [s for s in self.spans if s.doc_id != "AGENT"]
        spans.append(next(s for s in self.spans if s.span_id == "AGENT@1:p1:4"))
        draft = {"decision": "approve", "conditions": [], "conflicts": [], "gaps": [],
                 "reasons": [{"id": "R1", "text": "The agent asks for approval.",
                              "citations": ["AGENT@1:p1:4", "LP-T2@2024:p44:5"]}],
                 "citations": []}
        self.assertIn("relies_on_source_instruction", self.rules(draft))

    def test_gaps_collapse_to_the_distinct_few_with_stages_kept(self):
        triage = safeguards.triage_gaps(self.draft, top=5)
        self.assertEqual(len(self.draft["gaps"]), 24)
        self.assertEqual(triage["duplicates_removed"], 16)
        self.assertEqual(len(triage["presented"]), 5)
        self.assertEqual(triage["collapsed_count"], 3)
        self.assertEqual(triage["presented"][0]["stages"], ["retrieval", "reconciliation", "draft"])
        self.assertTrue(all(not g["message"].startswith(("retrieval", "draft")) for g in triage["presented"]))

    def test_gaps_touching_the_decision_rank_first(self):
        top = safeguards.triage_gaps(self.draft, top=1)["presented"][0]["message"]
        self.assertIn("hedge", top)

    def test_export_leads_with_the_decision_and_counts_the_rest(self):
        review = {"verdict": "accept", "claims": [], "findings": []}
        result = stages.export({"case_id": "PA-2026-0181"}, self.draft, review)
        self.assertEqual(list(result)[:2], ["case_id", "decision"])
        self.assertEqual(len(result["gaps"]), 5)
        self.assertEqual(result["gaps_collapsed"], 3)

    def test_review_is_not_called_for_a_blocked_draft(self):
        class Unreachable:
            def complete_json(self, *args):
                raise AssertionError("provider called")

        with self.assertRaises(stages.StageFailed) as raised:
            stages.run_review(Unreachable(), self.draft, self.spans, 10_000)
        self.assertEqual(raised.exception.stage, "consistency")


if __name__ == "__main__":
    unittest.main()
