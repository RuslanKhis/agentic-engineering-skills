import json
from pathlib import Path
import unittest

from campaign.admission import Request, admit, load_approvals
from campaign.dispatch import dispatch
from campaign.ledger import Ledger
from tests.fake_provider import CountingTransport

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "campaign.json").read_text())


def seeded():
    return Ledger.from_seed(ROOT / "data" / "ledger-seed.json")


class DispatchTests(unittest.TestCase):
    def test_new_case_is_admitted_and_settled(self):
        ledger, transport = seeded(), CountingTransport()
        decision = dispatch(ledger, CONFIG, [], transport, Request("case-04", "generation"), {"case": "case-04"})
        self.assertTrue(decision.allowed)
        self.assertEqual(len(transport.sends), 1)
        self.assertEqual(ledger.attempts_for("case-04:generation")[0]["status"], "succeeded")

    def test_completed_identity_is_not_sent_again(self):
        ledger, transport = seeded(), CountingTransport()
        decision = dispatch(ledger, CONFIG, [], transport, Request("case-01", "generation"), {})
        self.assertFalse(decision.allowed)
        self.assertEqual(transport.sends, [])

    def test_case_outside_cohort_needs_approval(self):
        ledger, transport = seeded(), CountingTransport()
        decision = dispatch(ledger, CONFIG, [], transport, Request("case-99", "generation"), {})
        self.assertFalse(decision.allowed)
        self.assertEqual(transport.sends, [])

    def test_spending_allowance_is_enforced(self):
        ledger = seeded()
        config = dict(CONFIG, envelope=dict(CONFIG["envelope"], spend_cents=300))
        decision = admit(ledger, config, [], Request("case-06", "generation"))
        self.assertFalse(decision.allowed)

    def test_settled_spend_matches_receipts(self):
        self.assertEqual(seeded().settled_cents(), 96 + 41 + 52 + 104)

    def test_approvals_load(self):
        approvals = load_approvals(ROOT / "approvals")
        self.assertEqual(approvals[0]["scope"]["stage"], "review")


if __name__ == "__main__":
    unittest.main()
