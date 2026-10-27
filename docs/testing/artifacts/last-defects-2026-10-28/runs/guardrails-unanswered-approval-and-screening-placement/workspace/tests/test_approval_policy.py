import unittest

from app.approval_policy import (APPROVAL_THRESHOLD_CENTS, CONFIRMATION_TTL_SECONDS, refund_needs_approval,
                                 resolve_pending)


class ApprovalPolicyTests(unittest.TestCase):
    def test_large_refund_waits(self):
        self.assertTrue(refund_needs_approval(amount_cents=APPROVAL_THRESHOLD_CENTS + 1, order_id="HO-1"))

    def test_small_refund_goes_through(self):
        self.assertFalse(refund_needs_approval(amount_cents=1_000, order_id="HO-1"))

    def test_unrelated_message_never_approves(self):
        # The 2026-10-20 incident: a Monday "any news about my parcel?" executed the refund.
        self.assertEqual(resolve_pending("Hi, is there any news about my parcel?", 1_000.0, 1_060.0), "ask_again")

    def test_explicit_yes_approves_while_fresh(self):
        self.assertEqual(resolve_pending("Yes", 1_000.0, 1_060.0), "approve")

    def test_decline_variants(self):
        for text in ("no", "Cancel", "stop that", "don't"):
            self.assertEqual(resolve_pending(text, 1_000.0, 1_060.0), "decline")

    def test_yes_after_ttl_does_not_approve(self):
        late = 1_000.0 + CONFIRMATION_TTL_SECONDS + 1
        self.assertEqual(resolve_pending("yes", 1_000.0, late), "expired")

    def test_weekend_gap_expires(self):
        self.assertEqual(resolve_pending("yes", 0.0, 61 * 3600.0), "expired")


if __name__ == "__main__":
    unittest.main()
