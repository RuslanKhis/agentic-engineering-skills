import unittest

from expense_agent import tools
from tests.fakes import FakeToolContext
from tests.fixture_db import fresh_db


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.conn = fresh_db()

    def test_file_expense_writes_claim_and_line(self):
        result = tools.file_expense("MEAL", 4200, "EUR", "2026-10-12", "Client lunch", "ana/2026-10-12.pdf",
                                    FakeToolContext("emp-101"))
        self.assertEqual(result["status"], "filed")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM expense_lines").fetchone()[0], 1)

    def test_policy_limit(self):
        self.assertEqual(tools.get_policy_limit("MEAL", FakeToolContext("emp-101"))["limit_cents"], 6000)

    def test_schema_has_fourteen_tables(self):
        tables = self.conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' "
                                   "AND name NOT LIKE 'sqlite_%'").fetchone()[0]
        self.assertEqual(tables, 14)


if __name__ == "__main__":
    unittest.main()
