import unittest

from app.tools import get_claim, missing_documents


class ToolTests(unittest.TestCase):
    def test_get_claim(self):
        self.assertEqual(get_claim("cl-2026-0412")["claim"]["policy"], "HP-88120")

    def test_unknown_claim(self):
        self.assertEqual(get_claim("CL-1")["status"], "not_found")

    def test_missing_documents_for_theft(self):
        self.assertEqual(missing_documents("CL-2026-0417")["missing"], ["police report"])


if __name__ == "__main__":
    unittest.main()
