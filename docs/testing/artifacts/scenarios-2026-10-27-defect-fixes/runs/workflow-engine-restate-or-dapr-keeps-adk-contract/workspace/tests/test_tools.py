import unittest

from app import services
from app.tools.help import search_help
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import request_refund
from tests.fakes import FakeApprovals, FakeToolContext, configure_fakes


class OrderToolTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()

    def test_lookup_own_order(self):
        result = lookup_order("ho-10442", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["order"]["total_cents"], 8_900)

    def test_another_customers_order_is_not_found(self):
        result = lookup_order("HO-20001", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "not_found")

    def test_list_my_orders_newest_first(self):
        result = list_my_orders(FakeToolContext("cust-ana"))
        self.assertEqual([o["order_id"] for o in result["orders"]], ["HO-10518", "HO-10442"])


class RefundToolTests(unittest.TestCase):
    """The tool only submits; payment is exercised in test_approvals."""

    def setUp(self):
        self.store, self.pay, _ = configure_fakes()
        self.approvals = FakeApprovals()
        services.get().approvals = self.approvals

    def test_request_submits_for_approval_and_pays_nothing(self):
        result = request_refund("ho-10442", 2_500, "Jacket arrived torn", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "pending_approval")
        self.assertEqual(self.pay.requests, [])
        self.assertEqual(self.store.refunds_for("HO-10442"), [])
        submitted = self.approvals.submitted[0]
        self.assertEqual((submitted.user_id, submitted.order_id, submitted.amount_cents),
                         ("cust-ana", "HO-10442", 2_500))
        self.assertEqual(submitted.operation_id, result["operation_id"])

    def test_same_request_gets_the_same_operation_id(self):
        first = request_refund("HO-10442", 2_500, "a", FakeToolContext("cust-ana"))
        again = request_refund("HO-10442", 2_500, "b", FakeToolContext("cust-ana"))
        self.assertEqual(first["operation_id"], again["operation_id"])

    def test_refund_above_order_total_is_refused_without_a_submission(self):
        result = request_refund("HO-10442", 9_000, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.approvals.submitted, [])

    def test_refund_on_another_customers_order_is_refused(self):
        result = request_refund("HO-20001", 100, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.approvals.submitted, [])

    def test_without_an_approval_gateway_the_tool_fails_closed(self):
        services.get().approvals = None
        result = request_refund("HO-10442", 100, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.pay.requests, [])

    def test_an_earlier_declined_request_is_not_reported_as_pending(self):
        services.get().approvals = FakeApprovals(status="declined")
        result = request_refund("HO-10442", 100, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")


class HelpToolTests(unittest.TestCase):
    def test_search_finds_returns_article(self):
        configure_fakes()
        ids = [a["id"] for a in search_help("how do refunds work")["articles"]]
        self.assertIn("kb-101", ids)


if __name__ == "__main__":
    unittest.main()
