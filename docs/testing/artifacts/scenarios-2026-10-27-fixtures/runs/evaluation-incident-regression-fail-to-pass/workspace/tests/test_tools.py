import unittest

from app.clients.http import Response
from app.tools.help import search_help
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import issue_refund, propose_refund
from tests.fakes import FakeToolContext, configure_fakes


class OrderToolTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()

    def test_lookup_own_order(self):
        result = lookup_order("ho-10442", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "ok")

    def test_another_customers_order_is_not_found(self):
        self.assertEqual(lookup_order("HO-20001", FakeToolContext("cust-ana"))["status"], "not_found")

    def test_list_my_orders_newest_first(self):
        result = list_my_orders(FakeToolContext("cust-ana"))
        self.assertEqual([o["order_id"] for o in result["orders"]], ["HO-10518", "HO-10442"])


class RefundToolTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()
        self.ctx = FakeToolContext("cust-ana")

    def test_proposal_then_issue_refunds_once(self):
        self.assertEqual(propose_refund("HO-10442", 2_500, "torn", self.ctx)["status"], "awaiting_confirmation")
        self.assertEqual(issue_refund(self.ctx)["status"], "refunded")
        self.assertEqual(len(self.pay.requests), 1)

    def test_second_issue_after_one_proposal_does_not_refund_twice(self):
        # Incident: the customer said "yes" twice and the agent called issue_refund twice.
        propose_refund("HO-10442", 2_500, "torn", self.ctx)
        self.assertEqual(issue_refund(self.ctx)["status"], "refunded")
        self.assertEqual(issue_refund(self.ctx)["status"], "nothing_pending")
        self.assertEqual(len(self.pay.requests), 1)
        self.assertEqual(len(self.store.refunds_for("HO-10442")), 1)

    def test_issue_without_proposal_pays_nothing(self):
        self.assertEqual(issue_refund(self.ctx)["status"], "nothing_pending")
        self.assertEqual(self.pay.requests, [])

    def test_proposal_on_another_customers_order_is_refused(self):
        self.assertEqual(propose_refund("HO-20001", 100, "x", self.ctx)["status"], "error")

    def test_provider_rejection_is_reported(self):
        self.store, self.pay, _ = configure_fakes(payments_responses=[Response(402, {"error": "declined"})])
        propose_refund("HO-10442", 1_000, "x", self.ctx)
        self.assertEqual(issue_refund(self.ctx)["status"], "error")
        self.assertEqual(self.store.refunds_for("HO-10442"), [])


class HelpToolTests(unittest.TestCase):
    def test_search_finds_returns_article(self):
        configure_fakes()
        self.assertIn("kb-101", [a["id"] for a in search_help("how do refunds work")["articles"]])


if __name__ == "__main__":
    unittest.main()
