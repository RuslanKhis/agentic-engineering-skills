import json
from pathlib import Path
import unittest

from campaign.admission import Request, admit, load_approvals
from campaign.dispatch import apply_late_receipts, dispatch
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


def inbox():
    lines = (ROOT / "data" / "receipts-inbox.jsonl").read_text().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.approvals = load_approvals(ROOT / "approvals")
        self.ledger = seeded()
        apply_late_receipts(self.ledger, inbox())

    def go(self, transport, case, stage, approvals=None):
        approvals = self.approvals if approvals is None else approvals
        return dispatch(self.ledger, CONFIG, approvals, transport, Request(case, stage), {})

    def test_late_receipts_redelivered_are_counted_once(self):
        self.assertEqual(self.ledger.settled_cents(), 96 + 41 + 52 + 104 + 102)
        apply_late_receipts(self.ledger, inbox())
        self.assertEqual(self.ledger.settled_cents(), 395)

    def test_conflicting_receipt_is_rejected(self):
        with self.assertRaises(ValueError):
            self.ledger.settle({"receipt_id": "rc-9005", "reservation_id": "r-05", "amount_cents": 1})

    def test_approved_continuation_goes_once_even_if_response_is_lost_again(self):
        transport = CountingTransport(["no_response"])
        self.assertFalse(self.go(transport, "case-07", "review").reason == "ok")
        self.assertEqual(len(transport.sends), 1)
        again = self.go(transport, "case-07", "review")
        self.assertFalse(again.allowed)
        self.assertEqual(len(transport.sends), 1)
        open_holds = self.ledger.open_reserved_cents()
        self.assertEqual(open_holds, 60 + 60)  # old and new unanswered attempts both stay held

    def test_approved_continuation_success_then_no_more(self):
        transport = CountingTransport()
        self.assertTrue(self.go(transport, "case-07", "review").allowed)
        self.assertFalse(self.go(transport, "case-07", "review").allowed)
        self.assertEqual(len(transport.sends), 1)

    def test_approval_does_not_cover_other_stage_or_case(self):
        transport = CountingTransport()
        self.assertFalse(self.go(transport, "case-03", "generation").allowed)  # failed earlier, other case/stage
        self.assertFalse(self.go(transport, "case-07", "generation").allowed)  # already completed
        self.assertFalse(self.go(transport, "case-99", "review").allowed)      # outside cohort
        self.assertEqual(transport.sends, [])

    def test_interrupted_attempt_with_late_receipt_is_not_paid_twice(self):
        transport = CountingTransport()
        decision = self.go(transport, "case-05", "generation")
        self.assertFalse(decision.allowed)
        self.assertIn("already paid", decision.reason)
        self.assertEqual(transport.sends, [])

    def test_continuation_without_approval_is_refused(self):
        transport = CountingTransport()
        self.assertFalse(self.go(transport, "case-07", "review", approvals=[]).allowed)
        self.assertEqual(transport.sends, [])

    def test_open_holds_and_stale_balance_reduce_allowance(self):
        # envelope 1600 - settled 395 - open 60; balance 1560 - everything committed since the reading
        self.assertEqual(self.ledger.remaining_allowance(1600), min(1600 - 395 - 60, 1560 - 395 - 60))
        tight = dict(CONFIG, envelope=dict(CONFIG["envelope"], spend_cents=1600))
        self.ledger.conn.execute("UPDATE provider_balance SET remaining_cents = 500")
        self.assertFalse(admit(self.ledger, tight, self.approvals, Request("case-07", "review")).allowed)

    def test_unanswered_attempts_count_as_sends(self):
        self.assertEqual(self.ledger.sends(), 7)

    def test_reserve_is_not_tightened_below_configured(self):
        self.assertEqual(admit(self.ledger, CONFIG, [], Request("case-04", "generation")).reserve_cents, 110)


if __name__ == "__main__":
    unittest.main()
