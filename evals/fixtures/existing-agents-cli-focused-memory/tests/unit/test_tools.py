import unittest
from types import SimpleNamespace

from app import tools


class ToolTests(unittest.TestCase):
    def setUp(self):
        tools.TICKETS.clear()

    def test_search_kb_finds_vpn_article(self):
        ids = [a["id"] for a in tools.search_kb("vpn connect")["articles"]]
        self.assertIn("IT-012", ids)

    def test_tickets_are_per_caller(self):
        tools.raise_ticket("Screen flickers", "hardware", SimpleNamespace(user_id="s-100"))
        self.assertEqual(tools.my_tickets(SimpleNamespace(user_id="s-200"))["tickets"], [])

    def test_bad_category(self):
        result = tools.raise_ticket("x", "payroll", SimpleNamespace(user_id="s-100"))
        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
