import unittest

from triage.tools import lookup_product, record_triage


class ToolTests(unittest.TestCase):
    def test_lookup(self):
        self.assertEqual(lookup_product("EB-2291-0042")["status"], "ok")

    def test_bad_category(self):
        self.assertEqual(record_triage("c1", "wheels", 2)["status"], "error")


if __name__ == "__main__":
    unittest.main()
