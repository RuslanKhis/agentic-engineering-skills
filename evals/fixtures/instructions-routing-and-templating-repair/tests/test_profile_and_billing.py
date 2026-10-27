import unittest

from app.tools.billing import get_invoice
from app.tools.profile import load_profile
from tests.fakes import FakeToolContext, configure_fakes


class ProfileToolTests(unittest.TestCase):
    def test_profile_is_written_to_state(self):
        configure_fakes()
        ctx = FakeToolContext("cust-ana")
        result = load_profile(ctx)
        self.assertEqual(result["name"], "Ana")
        self.assertEqual(ctx.state["customer_profile"], {"name": "Ana", "orders": 2})

    def test_unknown_customer(self):
        configure_fakes()
        self.assertEqual(load_profile(FakeToolContext("cust-zed"))["status"], "not_found")


class BillingToolTests(unittest.TestCase):
    def test_invoice_lines_add_up(self):
        configure_fakes()
        invoice = get_invoice("HO-10442", FakeToolContext("cust-ana"))
        self.assertEqual(sum(l["amount_cents"] for l in invoice["lines"]), invoice["total_cents"])

    def test_other_customers_invoice_is_not_found(self):
        configure_fakes()
        self.assertEqual(get_invoice("HO-20001", FakeToolContext("cust-ana"))["status"], "not_found")


if __name__ == "__main__":
    unittest.main()
