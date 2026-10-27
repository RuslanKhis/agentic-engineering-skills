import unittest

from app.approval_policy import APPROVAL_THRESHOLD_CENTS, refund_needs_approval


class ApprovalPolicyTests(unittest.TestCase):
    def test_large_refund_waits(self):
        self.assertTrue(refund_needs_approval(amount_cents=APPROVAL_THRESHOLD_CENTS + 1, order_id="HO-1"))

    def test_small_refund_goes_through(self):
        self.assertFalse(refund_needs_approval(amount_cents=1_000, order_id="HO-1"))


if __name__ == "__main__":
    unittest.main()
