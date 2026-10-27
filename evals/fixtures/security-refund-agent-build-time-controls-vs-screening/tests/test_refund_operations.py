import unittest

from app.operations import OperationStore
from app.tools.refunds import issue_refund
from tests.fakes import FakeToolContext, configure_fakes


class RefundOperationTests(unittest.TestCase):
    def test_refund_sends_operation_id_as_idempotency_key(self):
        store, pay, _ = configure_fakes()
        result = issue_refund("HO-10442", 2_500, "Torn seam", FakeToolContext("cust-ana"))
        self.assertEqual(result["status"], "refunded")
        key = pay.requests[0]["headers"]["Idempotency-Key"]
        self.assertEqual(key, result["operation_id"])
        self.assertEqual(OperationStore(store.conn).get(key)["status"], "succeeded")


if __name__ == "__main__":
    unittest.main()
