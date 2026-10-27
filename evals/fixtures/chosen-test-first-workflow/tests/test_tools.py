import unittest

from app.tools.help import search_help
from app.tools.orders import list_my_orders, lookup_order
from app.tools.refunds import issue_refund
from tests.fakes import FakeToolContext, configure_fakes


class OrderToolTests(unittest.TestCase):
    def setUp(self):
        self.store, self.provider, _, _ = configure_fakes()

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
    def setUp(self):
        self.store, self.provider, _, _ = configure_fakes()

    def test_refund_success_response(self):
        result = issue_refund("HO-10442", 2_500, "Jacket arrived torn", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "refunded")
        self.assertEqual(result["amount_cents"], 2_500)
        self.assertTrue(result["refund_id"].startswith("rf_"))
        self.assertEqual(self.store.refunds_for("HO-10442")[0]["provider_ref"], "re_0001")

    def test_refund_above_order_total_is_refused_without_a_call(self):
        result = issue_refund("HO-10442", 9_000, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.provider.requests, [])

    def test_refund_on_another_customers_order_is_refused(self):
        result = issue_refund("HO-20001", 100, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.provider.requests, [])

    def test_provider_rejection_is_reported(self):
        self.store, self.provider, _, _ = configure_fakes(provider_script=[402])
        result = issue_refund("HO-10442", 1_000, "x", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertEqual(self.store.refunds_for("HO-10442"), [])


class HelpToolTests(unittest.TestCase):
    def test_search_finds_returns_article(self):
        configure_fakes()
        ids = [a["id"] for a in search_help("how do refunds work")["articles"]]
        self.assertIn("kb-101", ids)


if __name__ == "__main__":
    unittest.main()
