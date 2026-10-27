import unittest

from app import services
from app.clients.http import Response
from app.tools.cancellations import cancel_order
from tests.fakes import FakeToolContext, configure_fakes

OK = Response(200, {"order_id": "HO-90001", "status": "cancelled", "cancellation_id": "c-1"})


def setup(responses=None):
    store, _, _ = configure_fakes(orders_responses=responses)
    store.add_order("HO-90001", "cust-ana", "processing", 5_000, "2026-10-25")
    store.add_order("HO-90002", "cust-ana", "delivered", 5_000, "2026-10-01")
    store.add_order("HO-90003", "cust-ben", "processing", 5_000, "2026-10-25")
    return store, services.get().orders.transport


class CancelOrderTests(unittest.TestCase):
    def test_cancels_own_order_and_records_it(self):
        store, orders = setup([OK])
        result = cancel_order("ho-90001", FakeToolContext("cust-ana"))
        self.assertEqual(result, {"status": "cancelled", "order_id": "HO-90001", "cancellation_id": "c-1"})
        self.assertEqual(store.get_order("HO-90001")["status"], "cancelled")
        self.assertEqual(len(orders.requests), 1)
        req = orders.requests[0]
        self.assertEqual((req["method"], req["url"]), ("POST", "https://orders.test/v2/orders/HO-90001/cancel"))
        self.assertEqual(req["headers"]["Authorization"], "Bearer test-token")

    def test_another_customers_order_makes_no_call(self):
        _, orders = setup()
        self.assertEqual(cancel_order("HO-90003", FakeToolContext("cust-ana"))["status"], "error")
        self.assertEqual(orders.requests, [])

    def test_delivered_or_already_cancelled_makes_no_call(self):
        store, orders = setup([OK])
        self.assertEqual(cancel_order("HO-90002", FakeToolContext("cust-ana"))["status"], "error")
        cancel_order("HO-90001", FakeToolContext("cust-ana"))
        self.assertEqual(cancel_order("HO-90001", FakeToolContext("cust-ana"))["status"], "error")
        self.assertEqual(len(orders.requests), 1)

    def test_409_means_shipped_and_local_status_is_unchanged(self):
        store, _ = setup([Response(409, {})])
        result = cancel_order("HO-90001", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "error")
        self.assertIn("shipped", result["message"])
        self.assertEqual(store.get_order("HO-90001")["status"], "processing")

    def test_timeout_is_unknown_and_not_retried(self):
        store, orders = setup([TimeoutError("slow")])
        result = cancel_order("HO-90001", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(len(orders.requests), 1)
        self.assertEqual(store.get_order("HO-90001")["status"], "processing")

    def test_server_error_and_odd_body_are_unknown(self):
        for resp in (Response(503, {}), Response(200, {"status": "cancelled"})):
            with self.subTest(resp=resp):
                setup([resp])
                self.assertEqual(cancel_order("HO-90001", FakeToolContext("cust-ana"))["status"], "unknown")

    def test_client_error_is_a_plain_error(self):
        setup([Response(404, {})])
        self.assertEqual(cancel_order("HO-90001", FakeToolContext("cust-ana"))["status"], "error")


if __name__ == "__main__":
    unittest.main()
