import json
import unittest
from pathlib import Path

from expense_agent import tools
from expense_agent.rules import mandatory_escalation_reason
from expense_agent.store import ClaimStore


def claim(claim_id="EXP-1", category="meals", total=42.0):
    return {"claim_id": claim_id, "employee_id": "emp-1", "category": category, "total_eur": total,
            "receipt_image": True}


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.store = ClaimStore()
        tools.configure(self.store)
        self.store.add(claim())

    def test_decide_records_the_decision(self):
        result = tools.decide_claim("EXP-1", "approve", "Within the meal cap")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(self.store.get("EXP-1")["lane"], "decided")

    def test_escalate_records_the_lane(self):
        tools.escalate_claim("EXP-1", "Unusual")
        self.assertEqual(self.store.get("EXP-1")["lane"], "finance_review")

    def test_claim_cannot_be_triaged_twice(self):
        tools.escalate_claim("EXP-1", "Unusual")
        self.assertEqual(tools.decide_claim("EXP-1", "approve", "x")["status"], "error")

    def test_invalid_decision_is_refused(self):
        self.assertEqual(tools.decide_claim("EXP-1", "maybe", "x")["status"], "error")

    def test_travel_claim_cannot_be_decided(self):
        self.store.add(claim("EXP-2", category="rail", total=50.0))
        self.assertEqual(tools.decide_claim("EXP-2", "approve", "x")["status"], "error")
        self.assertIsNone(self.store.get("EXP-2")["lane"])

    def test_claim_over_500_cannot_be_decided(self):
        self.store.add(claim("EXP-3", category="software", total=500.01))
        self.assertEqual(tools.decide_claim("EXP-3", "approve", "x")["status"], "error")

    def test_claim_at_500_can_be_decided(self):
        self.store.add(claim("EXP-4", category="software", total=500.0))
        self.assertEqual(tools.decide_claim("EXP-4", "approve", "x")["status"], "ok")


class SampleExportTests(unittest.TestCase):
    def test_rule_mandated_share_of_recent_claims(self):
        path = Path(__file__).resolve().parent.parent / "data" / "recent-claims.jsonl"
        claims = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        forced = [c for c in claims if mandatory_escalation_reason(c)]
        # 15 of 40 (37.5 %): the floor the written rules set, far above the 10 % target.
        self.assertEqual(len(claims), 40)
        self.assertEqual(len(forced), 15)


if __name__ == "__main__":
    unittest.main()
