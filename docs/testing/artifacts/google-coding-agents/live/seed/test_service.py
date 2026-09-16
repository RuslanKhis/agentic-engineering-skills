import unittest

from provider import SyntheticProvider
from service import RefundService


class ExistingTests(unittest.TestCase):
    def test_success_keeps_public_contract(self):
        provider = SyntheticProvider()
        result = RefundService(provider).refund("order_42", "12.50")
        self.assertEqual(result, {
            "status": "applied", "operation_id": "order_42",
            "amount_minor": 1250, "refund_id": "refund-1",
        })
        self.assertEqual(provider.effects, [("order_42", 1250)])


if __name__ == "__main__":
    unittest.main()
