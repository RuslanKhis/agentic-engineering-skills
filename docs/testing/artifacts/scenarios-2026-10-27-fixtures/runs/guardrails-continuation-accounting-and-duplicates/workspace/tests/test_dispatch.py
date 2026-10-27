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

    # continuation, approval scope and accounting
    def approvals(self):
        return load_approvals(ROOT / "approvals")

    def test_approved_review_continuation_goes_out_once(self):
        ledger, transport = seeded(), CountingTransport(["no_response"])
        req = Request("case-07", "review")
        first = dispatch(ledger, CONFIG, self.approvals(), transport, req, {})
        self.assertFalse(first.allowed)           # lost response again
        self.assertEqual(len(transport.sends), 1)
        again = dispatch(ledger, CONFIG, self.approvals(), transport, req, {})
        self.assertFalse(again.allowed)           # approval covered one request only
        self.assertEqual(len(transport.sends), 1)

    def test_continuation_without_approval_is_refused(self):
        ledger, transport = seeded(), CountingTransport()
        decision = dispatch(ledger, CONFIG, [], transport, Request("case-07", "review"), {})
        self.assertFalse(decision.allowed)
        self.assertEqual(transport.sends, [])

    def test_approval_does_not_cover_other_stage_or_case(self):
        for req in (Request("case-03", "generation"), Request("case-07", "generation"), Request("case-99", "review")):
            ledger, transport = seeded(), CountingTransport()
            self.assertFalse(dispatch(ledger, CONFIG, self.approvals(), transport, req, {}).allowed, req)
            self.assertEqual(transport.sends, [])

    def test_late_receipt_means_already_charged_and_is_deduplicated(self):
        from campaign.dispatch import apply_late_receipts, load_receipts
        ledger, transport = seeded(), CountingTransport()
        apply_late_receipts(ledger, load_receipts(ROOT / "data" / "receipts-inbox.jsonl"))
        self.assertEqual(ledger.settled_cents(), 293 + 102)
        decision = dispatch(ledger, CONFIG, self.approvals(), transport, Request("case-05", "generation"), {})
        self.assertFalse(decision.allowed)
        self.assertEqual(transport.sends, [])

    def test_open_holds_count_against_allowance(self):
        ledger = seeded()  # settled 293 + open holds 110 + 60
        self.assertEqual(ledger.committed_cents(), 463)
        self.assertEqual(ledger.remaining_allowance(1600), 1600 - 463)

    def test_stale_balance_is_reduced_by_spend_since_observation(self):
        ledger = seeded()
        self.assertEqual(ledger.remaining_allowance(10_000), 1560 - 463)
        config = dict(CONFIG, envelope=dict(CONFIG["envelope"], spend_cents=10_000))
        ledger.conn.execute("UPDATE provider_balance SET remaining_cents = 500")
        self.assertFalse(admit(ledger, config, [], Request("case-04", "generation")).allowed)

    def test_reserve_is_not_tightened_by_cheap_receipts(self):
        ledger = seeded()
        self.assertEqual(admit(ledger, CONFIG, [], Request("case-04", "review")).reserve_cents, 60)

    def test_lost_response_keeps_its_hold_and_counts_as_a_send(self):
        ledger, transport = seeded(), CountingTransport(["no_response"])
        before = ledger.committed_cents()
        dispatch(ledger, CONFIG, [], transport, Request("case-04", "generation"), {})
        self.assertEqual(ledger.committed_cents(), before + 110)
        self.assertEqual(ledger.sends(), 8)

    def test_stage_allocation_is_enforced(self):
        ledger = seeded()
        config = dict(CONFIG, stages=dict(CONFIG["stages"],
                      generation=dict(CONFIG["stages"]["generation"], spend_cents=300)))
        self.assertFalse(admit(ledger, config, [], Request("case-04", "generation")).allowed)


if __name__ == "__main__":
    unittest.main()
