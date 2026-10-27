import json
import unittest
from pathlib import Path

from expense_agent import tools
from expense_agent.policy import forced_escalation_reason
from expense_agent.store import ClaimStore


def claim(category="meals", total=42.0, claim_id="EXP-1"):
    return {"claim_id": claim_id, "employee_id": "emp-1", "category": category, "total_eur": total,
            "receipt_image": True}


class PolicyTests(unittest.TestCase):
    def test_travel_categories_are_forced(self):
        for category in ("flights", "rail", "hotel", "car hire", "Hotel"):
            self.assertIsNotNone(forced_escalation_reason(claim(category, 10)))

    def test_over_500_is_forced_and_500_is_not(self):
        self.assertIsNotNone(forced_escalation_reason(claim("software", 500.01)))
        self.assertIsNone(forced_escalation_reason(claim("software", 500)))

    def test_ordinary_claim_is_left_to_the_model(self):
        self.assertIsNone(forced_escalation_reason(claim("taxi", 20)))

    def test_unreadable_fields_fail_closed(self):
        for bad in ({}, {"category": "taxi"}, {"category": "taxi", "total_eur": "12"},
                    {"category": "taxi", "total_eur": float("nan")},
                    {"category": "taxi", "total_eur": True}, {"category": None, "total_eur": 5}):
            self.assertIsNotNone(forced_escalation_reason(bad), bad)

    def test_decide_cannot_override_a_forced_escalation(self):
        store = ClaimStore()
        tools.configure(store)
        store.add(claim("flights", 900))
        self.assertEqual(tools.decide_claim("EXP-1", "approve", "x")["status"], "error")
        self.assertIsNone(store.get("EXP-1")["lane"])

    def test_floor_share_of_recent_claims(self):
        path = Path(__file__).parent.parent / "data" / "recent-claims.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        forced = sum(forced_escalation_reason(r) is not None for r in rows)
        # 15 of 40: the code floor alone is above the 10 % product target.
        self.assertEqual((forced, len(rows)), (15, 40))


if __name__ == "__main__":
    unittest.main()
