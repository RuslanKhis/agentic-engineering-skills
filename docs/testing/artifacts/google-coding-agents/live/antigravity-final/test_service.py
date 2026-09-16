import unittest

from provider import ProviderRejected, SyntheticProvider
from service import RefundService


class ExistingTests(unittest.TestCase):
    def test_success_keeps_public_contract(self):
        provider = SyntheticProvider()
        result = RefundService(provider).refund("order_42", "12.50")
        self.assertEqual(result, {
            "status": "applied", "operation_id": "order_42",
            "amount_minor": 1250, "refund_id": "refund-1",
        })
        self.assertEqual(provider.effects, [("order_42", 1250)])


class RetryAndRecoveryTests(unittest.TestCase):
    def test_lost_response_after_commit_recovered_with_single_effect(self):
        provider = SyntheticProvider(["commit_then_timeout", "success"])
        service = RefundService(provider)
        result = service.refund("order_lost_resp", "12.50")

        self.assertEqual(result, {
            "status": "applied",
            "operation_id": "order_lost_resp",
            "amount_minor": 1250,
            "refund_id": "refund-1",
        })
        self.assertEqual(len(provider.calls), 2)
        # Verify the same replay key was reused on retry
        call1_key = provider.calls[0][2]
        call2_key = provider.calls[1][2]
        self.assertEqual(call1_key, call2_key)
        # Verify only one side effect was applied
        self.assertEqual(provider.effects, [("order_lost_resp", 1250)])

    def test_timeout_before_commit_retried_and_succeeds(self):
        provider = SyntheticProvider(["timeout_before_commit", "success"])
        service = RefundService(provider)
        result = service.refund("order_timeout_retry", "25.00")

        self.assertEqual(result, {
            "status": "applied",
            "operation_id": "order_timeout_retry",
            "amount_minor": 2500,
            "refund_id": "refund-1",
        })
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0][2], provider.calls[1][2])
        self.assertEqual(provider.effects, [("order_timeout_retry", 2500)])

    def test_first_attempt_rejection_is_terminal_rejected_without_retry(self):
        provider = SyntheticProvider(["reject"])
        service = RefundService(provider)
        result = service.refund("order_reject_first", "15.00")

        self.assertEqual(result, {
            "status": "rejected",
            "operation_id": "order_reject_first",
            "amount_minor": 1500,
            "refund_id": None,
        })
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(len(provider.effects), 0)

    def test_timeout_then_rejection_is_unknown(self):
        provider = SyntheticProvider(["timeout_before_commit", "reject"])
        service = RefundService(provider)
        result = service.refund("order_timeout_then_rej", "15.00")

        self.assertEqual(result, {
            "status": "unknown",
            "operation_id": "order_timeout_then_rej",
            "amount_minor": 1500,
            "refund_id": None,
        })
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0][2], provider.calls[1][2])

    def test_commit_then_timeout_followed_by_rejection_is_unknown(self):
        provider = SyntheticProvider(["commit_then_timeout", "reject"])
        service = RefundService(provider)
        result = service.refund("order_commit_timeout_rej", "15.00")

        self.assertEqual(result, {
            "status": "unknown",
            "operation_id": "order_commit_timeout_rej",
            "amount_minor": 1500,
            "refund_id": None,
        })
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0][2], provider.calls[1][2])

    def test_two_timeouts_is_unknown(self):
        provider = SyntheticProvider(["timeout_before_commit", "timeout_before_commit"])
        service = RefundService(provider)
        result = service.refund("order_two_timeouts", "15.00")

        self.assertEqual(result, {
            "status": "unknown",
            "operation_id": "order_two_timeouts",
            "amount_minor": 1500,
            "refund_id": None,
        })
        self.assertEqual(len(provider.calls), 2)
        self.assertEqual(provider.calls[0][2], provider.calls[1][2])


class IdempotencyAndLedgerTests(unittest.TestCase):
    def test_repeating_completed_operation_returns_stored_without_dispatch(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        r1 = service.refund("op_repeat_applied", "50.00")
        self.assertEqual(r1["status"], "applied")
        self.assertEqual(len(provider.calls), 1)

        r2 = service.refund("op_repeat_applied", "50.00")
        self.assertEqual(r2, r1)
        self.assertEqual(len(provider.calls), 1)

    def test_repeating_with_equivalent_amount_spellings(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        r1 = service.refund("op_spelling", "12.5")
        self.assertEqual(r1["status"], "applied")
        self.assertEqual(r1["amount_minor"], 1250)
        self.assertEqual(len(provider.calls), 1)

        # Equivalent spellings: "12.50", "012.50", "0012.5"
        for spelling in ["12.50", "012.50", "0012.5"]:
            r = service.refund("op_spelling", spelling)
            self.assertEqual(r, r1)
            self.assertEqual(len(provider.calls), 1)

    def test_repeating_rejected_operation_returns_stored_without_dispatch(self):
        provider = SyntheticProvider(["reject"])
        service = RefundService(provider)

        r1 = service.refund("op_repeat_rej", "30.00")
        self.assertEqual(r1["status"], "rejected")
        self.assertEqual(len(provider.calls), 1)

        r2 = service.refund("op_repeat_rej", "30.00")
        self.assertEqual(r2, r1)
        self.assertEqual(len(provider.calls), 1)

    def test_repeating_unknown_operation_returns_stored_without_dispatch(self):
        provider = SyntheticProvider(["timeout_before_commit", "timeout_before_commit"])
        service = RefundService(provider)

        r1 = service.refund("op_repeat_unk", "30.00")
        self.assertEqual(r1["status"], "unknown")
        self.assertEqual(len(provider.calls), 2)

        r2 = service.refund("op_repeat_unk", "30.00")
        self.assertEqual(r2, r1)
        self.assertEqual(len(provider.calls), 2)

    def test_changed_amount_on_dispatched_id_raises_value_error(self):
        provider = SyntheticProvider(["success", "reject", "timeout_before_commit", "timeout_before_commit"])
        service = RefundService(provider)

        # 1. Applied
        service.refund("op_mod_applied", "10.00")
        with self.assertRaises(ValueError):
            service.refund("op_mod_applied", "10.01")

        # 2. Rejected
        service.refund("op_mod_rej", "20.00")
        with self.assertRaises(ValueError):
            service.refund("op_mod_rej", "25.00")

        # 3. Unknown
        service.refund("op_mod_unk", "30.00")
        with self.assertRaises(ValueError):
            service.refund("op_mod_unk", "35.00")

    def test_returned_result_is_isolated_from_mutation(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        res1 = service.refund("op_isolated", "10.00")
        res1["status"] = "tampered"
        res2 = service.refund("op_isolated", "10.00")
        self.assertEqual(res2["status"], "applied")


class ConfirmationTests(unittest.TestCase):
    def test_unconfirmed_returns_cancelled_with_zero_provider_calls(self):
        provider = SyntheticProvider()
        service = RefundService(provider)

        res = service.refund("op_cancel", "15.00", confirmed=False)
        self.assertEqual(res, {
            "status": "cancelled",
            "operation_id": "op_cancel",
            "amount_minor": 1500,
            "refund_id": None,
        })
        self.assertEqual(len(provider.calls), 0)

    def test_unconfirmed_does_not_block_later_confirmed_dispatch(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        res_c = service.refund("op_confirm_later", "15.00", confirmed=False)
        self.assertEqual(res_c["status"], "cancelled")
        self.assertEqual(len(provider.calls), 0)

        res_a = service.refund("op_confirm_later", "15.00", confirmed=True)
        self.assertEqual(res_a["status"], "applied")
        self.assertEqual(len(provider.calls), 1)

    def test_previously_dispatched_called_with_confirmed_false_returns_stored_result(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        res1 = service.refund("op_already_done", "15.00", confirmed=True)
        self.assertEqual(res1["status"], "applied")
        self.assertEqual(len(provider.calls), 1)

        res2 = service.refund("op_already_done", "15.00", confirmed=False)
        self.assertEqual(res2["status"], "applied")
        self.assertEqual(len(provider.calls), 1)


class InputValidationTests(unittest.TestCase):
    def setUp(self):
        self.provider = SyntheticProvider()
        self.service = RefundService(self.provider)

    def test_invalid_operation_id_types_and_formats(self):
        invalid_ids = [
            123,
            None,
            [],
            {},
            "",
            "a" * 65,
            "op 1",
            "op.1",
            "op/1",
            "op@1",
            "op:1",
            "op\n1",
            "op#1",
        ]
        for bad_id in invalid_ids:
            with self.subTest(bad_id=bad_id):
                with self.assertRaises(ValueError):
                    self.service.refund(bad_id, "10.00")
        self.assertEqual(len(self.provider.calls), 0)

    def test_valid_operation_id_boundaries(self):
        self.service.refund("x", "1.00")
        self.service.refund("x" * 64, "1.00")
        self.service.refund("abc_XYZ-123", "1.00")
        self.assertEqual(len(self.provider.calls), 3)

    def test_invalid_amount_formats_raise_value_error(self):
        invalid_amounts = [
            12.5,
            1250,
            None,
            "",
            "1" * 33,
            "-10.00",
            "+10.00",
            " 10.00",
            "10.00 ",
            "10. 00",
            "1e2",
            "1E2",
            ".50",
            ".5",
            "10.",
            "10.500",
            "10.123",
            "abc",
            "NaN",
            "Infinity",
            "10,00",
            "0",
            "0.00",
            "0.0",
            "10000.01",
            "10001",
            "1000000",
        ]
        for bad_amount in invalid_amounts:
            with self.subTest(bad_amount=bad_amount):
                with self.assertRaises(ValueError):
                    self.service.refund("op_val", bad_amount)
        self.assertEqual(len(self.provider.calls), 0)

    def test_valid_amount_boundaries(self):
        # 1 minor unit ($0.01)
        r_min = self.service.refund("op_min", "0.01")
        self.assertEqual(r_min["amount_minor"], 1)

        # 1,000,000 minor units ($10,000.00)
        r_max = self.service.refund("op_max", "10000.00")
        self.assertEqual(r_max["amount_minor"], 1000000)

        # Integer spelling of maximum
        r_max_int = self.service.refund("op_max_int", "10000")
        self.assertEqual(r_max_int["amount_minor"], 1000000)

        # Single decimal digit
        r_one_dec = self.service.refund("op_one_dec", "0.5")
        self.assertEqual(r_one_dec["amount_minor"], 50)

        # Leading zeros
        r_leading = self.service.refund("op_lead", "007.50")
        self.assertEqual(r_leading["amount_minor"], 750)


class ReplayKeyPrivacyTests(unittest.TestCase):
    def test_replay_key_stays_internal_and_keys_match_contract(self):
        provider = SyntheticProvider(["success"])
        service = RefundService(provider)

        result = service.refund("op_privacy", "12.50")
        self.assertNotIn("replay_key", result)
        self.assertEqual(
            set(result.keys()),
            {"status", "operation_id", "amount_minor", "refund_id"},
        )


if __name__ == "__main__":
    unittest.main()

