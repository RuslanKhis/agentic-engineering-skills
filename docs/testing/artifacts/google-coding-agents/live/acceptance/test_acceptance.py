"""Independent checks; execute with generated project first on PYTHONPATH."""
import unittest

from provider import SyntheticProvider
from service import RefundService


class RefundAcceptance(unittest.TestCase):
    def test_lost_reply_reuses_key_and_produces_one_effect(self):
        provider = SyntheticProvider(["commit_then_timeout", "success"])
        result = RefundService(provider).refund("order-1", "12.34")
        self.assertEqual(result["status"], "applied")
        self.assertEqual(result["amount_minor"], 1234)
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0], provider.calls[1])
        self.assertEqual(provider.effects, [("order-1", 1234)])
        self.assertNotIn("replay_key", result)

    def test_repeated_applied_operation_returns_original_receipt(self):
        provider = SyntheticProvider()
        service = RefundService(provider)
        original = service.refund("order-2", "01.00")
        repeated = service.refund("order-2", "1.0")
        self.assertEqual(original, repeated)
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(provider.effects, [("order-2", 100)])

    def test_changed_payload_does_not_dispatch(self):
        provider = SyntheticProvider()
        service = RefundService(provider)
        service.refund("order-3", "2.00")
        with self.assertRaises(ValueError):
            service.refund("order-3", "2.01")
        self.assertEqual(len(provider.calls), 1)

    def test_later_rejection_preserves_earlier_uncertainty(self):
        provider = SyntheticProvider(["commit_then_timeout", "reject"])
        result = RefundService(provider).refund("order-4", "4")
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["refund_id"])
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0], provider.calls[1])
        self.assertEqual(provider.effects, [("order-4", 400)])

    def test_unknown_repeat_uses_record_without_more_dispatch(self):
        provider = SyntheticProvider(["timeout_before_commit"] * 2)
        service = RefundService(provider)
        original = service.refund("order-5", "5")
        repeated = service.refund("order-5", "005.00")
        self.assertEqual(original["status"], "unknown")
        self.assertEqual(original, repeated)
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.effects, [])

    def test_invalid_amounts_and_ids_never_reach_provider(self):
        bad_amounts = [None, True, 1, 1.0, "", "0", "-1", "+1", "NaN",
                       "Infinity", "1e2", " 1.00", "1.001", "10000.01",
                       "9" * 33, "\u0661.00"]
        for amount in bad_amounts:
            with self.subTest(amount=repr(amount)):
                provider = SyntheticProvider()
                with self.assertRaises(ValueError):
                    RefundService(provider).refund("order-6", amount)
                self.assertEqual(provider.calls, [])
        for operation_id in ["", None, "bad id", "a" * 65, "\u00e9"]:
            with self.subTest(operation_id=operation_id):
                provider = SyntheticProvider()
                with self.assertRaises(ValueError):
                    RefundService(provider).refund(operation_id, "1")
                self.assertEqual(provider.calls, [])

    def test_contract_valid_money_is_exact_and_canonical(self):
        for amount, expected in [("0001.00", 100), ("0.01", 1),
                                 ("1.1", 110), ("10000", 1000000)]:
            with self.subTest(amount=amount):
                provider = SyntheticProvider()
                result = RefundService(provider).refund("order-7", amount)
                self.assertEqual(result["amount_minor"], expected)
                self.assertEqual(provider.effects, [("order-7", expected)])
                self.assertIsInstance(provider.calls[0][1], int)

    def test_no_confirmation_means_no_attempt(self):
        provider = SyntheticProvider()
        result = RefundService(provider).refund("order-8", "8", confirmed=False)
        self.assertEqual(result["status"], "cancelled")
        self.assertIsNone(result["refund_id"])
        self.assertEqual(provider.calls, [])

    def test_first_rejection_is_terminal_and_repeated_call_is_cached(self):
        provider = SyntheticProvider(["reject", "success"])
        service = RefundService(provider)
        original = service.refund("order-9", "9")
        repeated = service.refund("order-9", "9.00")
        self.assertEqual(original["status"], "rejected")
        self.assertEqual(original, repeated)
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(provider.effects, [])


if __name__ == "__main__":
    unittest.main()
