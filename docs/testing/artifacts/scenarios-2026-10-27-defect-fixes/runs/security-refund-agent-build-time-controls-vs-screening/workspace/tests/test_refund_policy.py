"""The refund limits hold with no screening and no prompt: the model is simulated as an attacker
that calls issue_refund with whatever arguments it likes. Fakes only; no network."""
import os
import random
import sqlite3
import tempfile
import unittest

from app import services
from app.clients.http import Response
from app.operations import OperationStore
from app.policy import MAX_REFUND_CENTS
from app.prompts import ROOT_INSTRUCTION
from app.settings import Settings
from app.store import Store
from app.tools.refunds import issue_refund
from tests.fakes import FakeToolContext, configure_fakes

ANA = FakeToolContext("cust-ana")


def paid_cents(pay) -> int:
    return sum(r["json"]["amount_cents"] for r in pay.requests)


class PerRefundLimitTests(unittest.TestCase):
    def test_single_refund_above_limit_is_refused_without_a_call_or_a_record(self):
        store, pay, _ = configure_fakes()
        store.add_order("HO-BIG", "cust-ana", "delivered", 50_000, "2026-10-01")
        result = issue_refund("HO-BIG", MAX_REFUND_CENTS + 1, "ignore previous rules", ANA)
        self.assertEqual(result["status"], "error")
        self.assertEqual(pay.requests, [])
        self.assertEqual(OperationStore(store.conn).committed_cents("HO-BIG"), 0)

    def test_refund_at_the_limit_is_allowed(self):
        store, pay, _ = configure_fakes()
        store.add_order("HO-BIG", "cust-ana", "delivered", 50_000, "2026-10-01")
        self.assertEqual(issue_refund("HO-BIG", MAX_REFUND_CENTS, "x", ANA)["status"], "refunded")

    def test_malformed_amounts_are_refused(self):
        _, pay, _ = configure_fakes()
        for bad in (0, -100, True, 12.5, "100", None):
            self.assertEqual(issue_refund("HO-10442", bad, "x", ANA)["status"], "error", bad)
        self.assertEqual(pay.requests, [])

    def test_limit_comes_from_services_not_the_prompt(self):
        _, pay, _ = configure_fakes()
        services.get().max_refund_cents = 1_000
        self.assertEqual(issue_refund("HO-10442", 1_001, "x", ANA)["status"], "error")
        self.assertEqual(pay.requests, [])

    def test_prompt_and_settings_state_the_enforced_limit(self):
        self.assertIn(str(MAX_REFUND_CENTS), ROOT_INSTRUCTION)
        self.assertEqual(Settings().max_refund_cents, MAX_REFUND_CENTS)


class AggregateBoundTests(unittest.TestCase):
    def test_many_small_refunds_stop_at_the_order_total(self):
        # The "eight compliant refunds on one order" shape: each call is small and individually fine.
        store, pay, _ = configure_fakes()  # HO-10442 total 8_900
        outcomes = [issue_refund("HO-10442", 2_000, "again", ANA)["status"] for _ in range(8)]
        self.assertEqual(outcomes.count("refunded"), 4)
        self.assertEqual(paid_cents(pay), 8_000)
        self.assertLessEqual(paid_cents(pay), 8_900)

    def test_remainder_can_still_be_refunded_exactly(self):
        _, pay, _ = configure_fakes()
        self.assertEqual(issue_refund("HO-10442", 8_000, "x", ANA)["status"], "refunded")
        self.assertEqual(issue_refund("HO-10442", 901, "x", ANA)["status"], "error")
        self.assertEqual(issue_refund("HO-10442", 900, "x", ANA)["status"], "refunded")
        self.assertEqual(paid_cents(pay), 8_900)

    def test_randomised_attack_sequences_never_exceed_total_or_limit(self):
        rng = random.Random(7)
        for _ in range(50):
            store, pay, _ = configure_fakes()
            for _ in range(30):
                order = rng.choice(["HO-10442", "HO-10518", "HO-20001", "ho-10442 ", "HO-NOPE"])
                issue_refund(order, rng.choice([1, 99, 500, 2_000, 8_900, 15_000, 15_001, 99_999]), "x", ANA)
            for req in pay.requests:
                self.assertLessEqual(req["json"]["amount_cents"], MAX_REFUND_CENTS)
            for order_id, total in (("HO-10442", 8_900), ("HO-10518", 15_400)):
                sent = sum(r["json"]["amount_cents"] for r in pay.requests if r["json"]["order_id"] == order_id)
                self.assertLessEqual(sent, total)
            self.assertTrue(all(r["json"]["order_id"] != "HO-20001" for r in pay.requests))  # Ben's order

    def test_provider_5xx_keeps_the_reservation_because_the_refund_may_have_applied(self):
        store, pay, _ = configure_fakes(payments_responses=[Response(503, {})])
        self.assertEqual(issue_refund("HO-10442", 8_000, "x", ANA)["status"], "error")
        self.assertEqual(OperationStore(store.conn).committed_cents("HO-10442"), 8_000)
        self.assertEqual(issue_refund("HO-10442", 2_000, "retry", ANA)["status"], "error")
        self.assertEqual(len(pay.requests), 1)

    def test_provider_4xx_releases_the_reservation(self):
        store, pay, _ = configure_fakes(payments_responses=[Response(402, {})])
        self.assertEqual(issue_refund("HO-10442", 8_000, "x", ANA)["status"], "error")
        self.assertEqual(OperationStore(store.conn).committed_cents("HO-10442"), 0)
        self.assertEqual(issue_refund("HO-10442", 8_000, "x", ANA)["status"], "refunded")

    def test_transport_failure_keeps_the_reservation(self):
        store, pay, _ = configure_fakes(payments_responses=[TimeoutError("timed out")])
        with self.assertRaises(TimeoutError):
            issue_refund("HO-10442", 8_000, "x", ANA)
        self.assertEqual(OperationStore(store.conn).committed_cents("HO-10442"), 8_000)

    def test_two_connections_cannot_both_reserve_the_last_cents(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "support.db")
            first = Store(path)
            first.add_order("HO-1", "cust-ana", "delivered", 5_000, "2026-10-01")
            second = sqlite3.connect(path)
            second.row_factory = sqlite3.Row
            a, b = OperationStore(first.conn), OperationStore(second)
            self.assertIsNotNone(a.reserve("HO-1", 3_000, "x", 5_000))
            self.assertIsNone(b.reserve("HO-1", 3_000, "x", 5_000))
            second.close()
            first.conn.close()


class IdentityTests(unittest.TestCase):
    def test_other_customers_order_is_refused_whatever_the_amount(self):
        _, pay, _ = configure_fakes()
        self.assertEqual(issue_refund("HO-20001", 100, "x", ANA)["status"], "error")
        self.assertEqual(pay.requests, [])


if __name__ == "__main__":
    unittest.main()
