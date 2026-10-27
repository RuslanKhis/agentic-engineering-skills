import unittest

from claims.tools.claims_tools import file_payout, read_document
from tests.fakes import install


class ToolTests(unittest.TestCase):
    def test_read_document(self):
        install({"doc-1": "Repair invoice EUR 820"})
        self.assertEqual(read_document("doc-1")["text"], "Repair invoice EUR 820")
        self.assertEqual(read_document("doc-9")["status"], "not_found")

    def test_file_payout_records_one_payout(self):
        wired = install({})
        file_payout("CLM-30418", 82_000, "DE89370400440532013000")
        self.assertEqual(len(wired["payouts"].filed), 1)


if __name__ == "__main__":
    unittest.main()
