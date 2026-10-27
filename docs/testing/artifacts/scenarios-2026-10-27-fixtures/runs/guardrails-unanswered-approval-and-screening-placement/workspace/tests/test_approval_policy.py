import unittest

from app.approval_policy import (
    APPROVAL_THRESHOLD_CENTS, APPROVAL_TTL_SECONDS, approval_expired, interpret_reply, refund_needs_approval)


class ApprovalPolicyTests(unittest.TestCase):
    def test_large_refund_waits(self):
        self.assertTrue(refund_needs_approval(amount_cents=APPROVAL_THRESHOLD_CENTS + 1, order_id="HO-1"))

    def test_small_refund_goes_through(self):
        self.assertFalse(refund_needs_approval(amount_cents=1_000, order_id="HO-1"))

    def test_expiry(self):
        self.assertFalse(approval_expired(0, APPROVAL_TTL_SECONDS))
        self.assertTrue(approval_expired(0, APPROVAL_TTL_SECONDS + 1))

    def test_only_explicit_yes_confirms(self):
        self.assertIs(interpret_reply("Yes."), True)
        self.assertIs(interpret_reply("no thanks"), False)
        self.assertIs(interpret_reply("Cancel"), False)
        for text in ("where is my order?", "yes but also check HO-2", "", "maybe"):
            self.assertIsNone(interpret_reply(text))


if __name__ == "__main__":
    unittest.main()
