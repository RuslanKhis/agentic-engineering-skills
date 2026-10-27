import unittest
from types import SimpleNamespace

from fieldline import tools


class ToolTests(unittest.TestCase):
    def setUp(self):
        tools.VISITS.clear()

    def test_get_site(self):
        self.assertEqual(tools.get_site("nw-0417")["name"], "Hollins Farm mast")

    def test_unknown_site(self):
        self.assertEqual(tools.get_site("NW-9999")["status"], "not_found")

    def test_log_visit_records_engineer(self):
        result = tools.log_visit("NW-0522", "Replaced splice tray.", SimpleNamespace(user_id="eng-ravi"))
        self.assertEqual(result["engineer_id"], "eng-ravi")


if __name__ == "__main__":
    unittest.main()
