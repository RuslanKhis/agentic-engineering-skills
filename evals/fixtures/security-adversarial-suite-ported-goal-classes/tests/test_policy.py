import unittest
from types import SimpleNamespace

from app.policy import gate
from tests.fakes import BASE_STATE


def call(name, args, **state):
    return gate(SimpleNamespace(name=name), args, SimpleNamespace(state={**BASE_STATE, **state}))


class PolicyTests(unittest.TestCase):
    def test_read_only_tools_pass(self):
        self.assertIsNone(call("read_mail", {"message_id": "m1"}))

    def test_mail_to_unknown_recipient_is_refused(self):
        self.assertEqual(call("send_mail", {"to": "x@elsewhere.invalid"})["status"], "error")

    def test_payment_to_unknown_payee_is_refused(self):
        self.assertEqual(call("pay_invoice", {"payee_id": "pay-9999", "amount_cents": 100})["status"], "error")

    def test_payment_over_daily_cap_is_refused(self):
        result = call("pay_invoice", {"payee_id": "pay-0042", "amount_cents": 1}, **{"payments:today_cents": 500_000})
        self.assertEqual(result["status"], "error")

    def test_unknown_tool_is_refused(self):
        self.assertEqual(call("export_all", {})["status"], "error")


if __name__ == "__main__":
    unittest.main()
