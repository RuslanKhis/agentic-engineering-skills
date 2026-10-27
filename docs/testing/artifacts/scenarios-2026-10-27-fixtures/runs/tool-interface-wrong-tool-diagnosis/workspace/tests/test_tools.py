import unittest

from app.clients.http import Response
from app.tools.delivery import change_delivery_address, track_parcel
from app.tools.help import search_help
from app.tools.orders import get_order, list_my_orders, search_orders
from app.tools.refunds import issue_refund
from app.tools.returns import return_status, start_return
from app.tools.vouchers import apply_voucher
from tests.fakes import FakeToolContext, configure_fakes

ANA = FakeToolContext("cust-ana")


class OrderToolTests(unittest.TestCase):
    def setUp(self):
        self.store, self.pay, _ = configure_fakes()

    def test_get_own_order(self):
        result = get_order("ho-10442", ANA)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["order"]["total_cents"], 8_900)

    def test_another_customers_order_is_not_found(self):
        self.assertEqual(get_order("HO-20001", ANA)["status"], "not_found")

    def test_not_found_carries_hint(self):
        result = get_order("HO-20001", ANA)
        self.assertIn("list_my_orders", result["hint"])

    def test_order_tools_declare_semantic_parameter_names(self):
        import inspect
        self.assertEqual(list(inspect.signature(get_order).parameters)[0], "order_id")
        self.assertEqual(list(inspect.signature(search_orders).parameters)[0], "query")
        self.assertIn("get_order", search_orders.__doc__)
        self.assertIn("search_orders", get_order.__doc__)

    def test_search_by_status(self):
        result = search_orders("processing", ANA)
        self.assertEqual([o["order_id"] for o in result["orders"]], ["HO-10518"])

    def test_list_my_orders_newest_first(self):
        result = list_my_orders(ANA)
        self.assertEqual([o["order_id"] for o in result["orders"]], ["HO-10518", "HO-10442"])


class DeliveryAndReturnTests(unittest.TestCase):
    def setUp(self):
        configure_fakes()

    def test_track_parcel(self):
        self.assertEqual(track_parcel("HO-10518", ANA)["stage"], "Being packed")

    def test_address_change_only_before_shipping(self):
        self.assertEqual(change_delivery_address("HO-10518", "1 Quay St", "ab1 2cd", ANA)["status"], "changed")
        self.assertEqual(change_delivery_address("HO-10442", "1 Quay St", "ab1 2cd", ANA)["status"], "error")

    def test_return_round_trip(self):
        started = start_return("HO-10442", "JKT-TIDE-M", "too small", ANA)
        self.assertEqual(started["status"], "started")
        self.assertEqual(return_status(started["return_id"])["state"], "label_sent")

    def test_voucher(self):
        self.assertEqual(apply_voucher("HO-10518", "welcome10", ANA)["percent"], 10)
        self.assertEqual(apply_voucher("HO-10518", "NOPE", ANA)["status"], "error")


class RefundAndHelpTests(unittest.TestCase):
    def test_refund_records_provider_reference(self):
        store, pay, _ = configure_fakes()
        self.assertEqual(issue_refund("HO-10442", 2_500, "torn", ANA)["status"], "refunded")
        self.assertEqual(len(pay.requests), 1)

    def test_provider_rejection_is_reported(self):
        store, pay, _ = configure_fakes(payments_responses=[Response(402, {"error": "declined"})])
        self.assertEqual(issue_refund("HO-10442", 1_000, "x", ANA)["status"], "error")

    def test_help_search_returns_text(self):
        configure_fakes()
        self.assertIn("30 days", search_help("returns refund"))


if __name__ == "__main__":
    unittest.main()
