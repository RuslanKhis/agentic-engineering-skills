import unittest

from claims_agent.policy import check_cover


class CoverTests(unittest.TestCase):
    def test_covered(self):
        self.assertTrue(check_cover("KP-100231", "fire")["covered"])

    def test_unknown_policy(self):
        self.assertEqual(check_cover("KP-0", "fire")["status"], "not_found")


if __name__ == "__main__":
    unittest.main()
