import sqlite3
import unittest

from app.clients.payments import PaymentsClient
from app.operations import OperationStore
from app.refund_adapter import RefundAdapter
from tests.provider_double import PaymentsProviderDouble


def make(script=None):
    provider = PaymentsProviderDouble(script)
    ops = OperationStore(sqlite3.connect(":memory:"))
    adapter = RefundAdapter(PaymentsClient("https://payments.test/v1", provider, "k"), ops, sleep=lambda s: None)
    return adapter, provider, ops


class RefundAdapterTests(unittest.TestCase):
    def test_success_records_the_operation(self):
        adapter, provider, ops = make()
        result = adapter.refund("op-1", "HO-10442", 2_500, "torn")
        self.assertTrue(result.ok)
        self.assertEqual(result.provider_refund_id, "re_0001")
        self.assertEqual(ops.get("op-1")["state"], "succeeded")
        self.assertEqual(provider.refunded_cents("HO-10442"), 2_500)

    def test_transient_error_is_retried(self):
        adapter, provider, ops = make([503, "ok"])
        result = adapter.refund("op-2", "HO-10442", 2_500, "torn")
        self.assertTrue(result.ok)
        self.assertEqual(len(provider.requests), 2)
        self.assertEqual(ops.get("op-2")["attempts"], 2)

    def test_declined_refund_is_not_retried(self):
        adapter, provider, ops = make([402])
        result = adapter.refund("op-3", "HO-10442", 2_500, "torn")
        self.assertFalse(result.ok)
        self.assertEqual(len(provider.requests), 1)
        self.assertEqual(ops.get("op-3")["state"], "failed")

    def test_completed_operation_is_not_sent_again(self):
        adapter, provider, ops = make()
        adapter.refund("op-4", "HO-10442", 2_500, "torn")
        again = adapter.refund("op-4", "HO-10442", 2_500, "torn")
        self.assertTrue(again.ok)
        self.assertEqual(len(provider.requests), 1)

    def test_timeout_before_acceptance_is_retried(self):
        adapter, provider, ops = make(["timeout_before_accept", "ok"])
        result = adapter.refund("op-5", "HO-10442", 2_500, "torn")
        self.assertTrue(result.ok)
        self.assertEqual(provider.refunded_cents("HO-10442"), 2_500)


if __name__ == "__main__":
    unittest.main()
