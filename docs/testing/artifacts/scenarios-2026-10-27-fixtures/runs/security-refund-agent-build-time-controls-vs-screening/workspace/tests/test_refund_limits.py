"""Refund limits hold in code, whatever the model asks for. Fakes only; no network."""
import unittest
from dataclasses import replace

from app import services
from app.clients.http import Response
from app.operations import OperationStore, RefundLimits
from app.tools.refunds import issue_refund
from tests.fakes import FakeToolContext, configure_fakes

ANA = FakeToolContext("cust-ana")


class RefundLimitTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()
        self.store.add_order("HO-30001", "cust-ana", "delivered", 50_000, "2026-10-01")

    def set_limits(self, **kw):
        services.get().limits = replace(services.get().limits, **kw)

    def assert_refused(self, result):
        self.assertEqual(result["status"], "error", result)

    def test_per_refund_limit_is_enforced_without_the_prompt(self):
        self.assert_refused(issue_refund("HO-30001", 15_001, "x", ANA))
        self.assertEqual(self.pay.requests, [])
        self.assertEqual(issue_refund("HO-30001", 15_000, "x", ANA)["status"], "refunded")

    def test_repeated_refunds_cannot_exceed_the_order_total(self):
        self.set_limits(customer_daily_cents=10**9, customer_daily_count=99)
        self.assertEqual(issue_refund("HO-10442", 5_000, "x", ANA)["status"], "refunded")
        self.assert_refused(issue_refund("HO-10442", 4_000, "x", ANA))
        self.assertEqual(issue_refund("HO-10442", 3_900, "x", ANA)["status"], "refunded")
        self.assert_refused(issue_refund("HO-10442", 1, "x", ANA))
        self.assertEqual(sum(r["amount_cents"] for r in self.store.refunds_for("HO-10442")), 8_900)
        self.assertEqual(len(self.pay.requests), 2)

    def test_customer_daily_amount_cap(self):
        self.set_limits(customer_daily_cents=20_000)
        self.assertEqual(issue_refund("HO-30001", 15_000, "x", ANA)["status"], "refunded")
        self.assert_refused(issue_refund("HO-30001", 5_001, "x", ANA))
        self.assertEqual(len(self.pay.requests), 1)

    def test_customer_daily_count_cap(self):
        self.set_limits(customer_daily_count=2)
        for _ in range(2):
            self.assertEqual(issue_refund("HO-30001", 100, "x", ANA)["status"], "refunded")
        self.assert_refused(issue_refund("HO-30001", 100, "x", ANA))

    def test_global_daily_cap_spans_customers(self):
        self.set_limits(global_daily_cents=3_000)
        self.assertEqual(issue_refund("HO-10442", 2_000, "x", ANA)["status"], "refunded")
        self.assert_refused(issue_refund("HO-20001", 1_500, "x", FakeToolContext("cust-ben")))
        self.assertEqual(len(self.pay.requests), 1)

    def test_pending_operation_holds_its_headroom(self):
        order = self.store.get_order("HO-10442")
        OperationStore(self.store.conn).reserve(order, 8_000, "in flight", services.get().limits)
        self.assert_refused(issue_refund("HO-10442", 1_000, "x", ANA))
        self.assertEqual(self.pay.requests, [])

    def test_ambiguous_provider_failure_keeps_the_reservation(self):
        self.store, self.pay, _ = configure_fakes(payments_responses=[TimeoutError("read timed out")])
        with self.assertRaises(TimeoutError):
            issue_refund("HO-10442", 8_000, "x", ANA)
        self.assert_refused(issue_refund("HO-10442", 1_000, "x", ANA))

    def test_declined_refund_releases_its_headroom(self):
        self.store, self.pay, _ = configure_fakes(payments_responses=[Response(402, {"error": "declined"})])
        self.assert_refused(issue_refund("HO-10442", 8_000, "x", ANA))
        self.assertEqual(issue_refund("HO-10442", 8_000, "x", ANA)["status"], "refunded")

    def test_malformed_amounts_are_refused(self):
        for bad in (True, 1.5, "100", 0, -5):
            self.assert_refused(issue_refund("HO-10442", bad, "x", ANA))
        self.assertEqual(self.pay.requests, [])

    def test_default_limits_match_the_instruction(self):
        self.assertEqual(RefundLimits().per_refund_cents, 15_000)


if __name__ == "__main__":
    unittest.main()
