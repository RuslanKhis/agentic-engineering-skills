import unittest

from expense_agent import tools
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


if __name__ == "__main__":
    unittest.main()
