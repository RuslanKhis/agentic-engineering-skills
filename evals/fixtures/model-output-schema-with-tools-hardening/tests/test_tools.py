import unittest

from extractor.tools import lookup_policy, lookup_repairer


class ToolTests(unittest.TestCase):
    def test_active_policy(self):
        self.assertEqual(lookup_policy("mp-118204")["policy_status"], "active")

    def test_unknown_policy(self):
        self.assertEqual(lookup_policy("MP-000000"), {"status": "not_found"})

    def test_repairer_partial_name(self):
        names = [m["name"] for m in lookup_repairer("quay")["matches"]]
        self.assertEqual(names, ["Quayside Body Repairs", "Quay Autos"])

    def test_blank_repairer_matches_nothing(self):
        self.assertEqual(lookup_repairer("  ")["matches"], [])


if __name__ == "__main__":
    unittest.main()
