import unittest

from research_agent import tools


class ToolTests(unittest.TestCase):
    def test_search_finds_report(self):
        self.assertEqual(tools.search_reports("bike market")["reports"][0]["report_id"], "rpt-eu-bikes-2026")

    def test_unknown_report_is_refused(self):
        self.assertEqual(tools.submit_procurement_request("rpt-x", "why")["status"], "error")


if __name__ == "__main__":
    unittest.main()
