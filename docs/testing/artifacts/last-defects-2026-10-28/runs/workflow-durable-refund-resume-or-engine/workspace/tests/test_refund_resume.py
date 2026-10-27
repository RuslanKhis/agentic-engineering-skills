"""Replay of the 2026-10-21 incident: the refund tool body runs again after resume.

ADK resume runs tools at least once, so the body can execute twice (pod evicted after the provider
accepted, then a second approval). These tests replay the body against a provider double that
de-duplicates on Idempotency-Key and assert one refund at the provider.
"""
import unittest

from app.clients.payments import PaymentsClient
from app.tools.refunds import issue_refund
from tests.fakes import DedupingProviderTransport, FakeToolContext, configure_fakes


class RefundReplayTests(unittest.TestCase):
    def setUp(self):
        self.store, _, _ = configure_fakes()
        self.provider = DedupingProviderTransport()
        from app import services
        services.get().payments = PaymentsClient("https://payments.test/v1", self.provider, "test-key")

    def call(self, call_id="call-1"):
        return issue_refund("HO-10442", 6_400, "damaged", FakeToolContext("cust-ana", function_call_id=call_id))

    def test_crash_after_provider_accepted_then_second_approval_pays_once(self):
        real_record = self.store.record_refund
        calls = {"n": 0}

        def crash_once(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("pod evicted")  # provider already accepted
            return real_record(*args, **kwargs)

        self.store.record_refund = crash_once
        with self.assertRaises(RuntimeError):
            self.call()
        result = self.call()  # resumed invocation after the manager approves again

        self.assertEqual(result["status"], "refunded")
        self.assertEqual(len(self.provider.requests), 2)  # the body did run twice
        self.assertEqual(len(self.provider.refunds), 1)  # one effect at the provider
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_plain_replay_returns_same_refund_id(self):
        first, second = self.call(), self.call()
        self.assertEqual(first["refund_id"], second["refund_id"])
        self.assertEqual(len(self.provider.refunds), 1)
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_a_different_function_call_is_a_different_refund(self):
        self.call("call-1")
        self.call("call-2")
        self.assertEqual(len(self.provider.refunds), 2)

    def test_missing_call_identity_fails_closed(self):
        result = self.call(call_id=None)
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.provider.requests, [])

    def test_double_detects_a_fresh_key_per_attempt(self):
        """Control: the pre-fix behaviour (new key each attempt) would pay twice on this double."""
        for _ in range(2):
            self.provider.request("POST", "u", json={"order_id": "HO-10442"},
                                  headers={"Idempotency-Key": f"k{_}"})
        self.assertEqual(len(self.provider.refunds), 2)


if __name__ == "__main__":
    unittest.main()
