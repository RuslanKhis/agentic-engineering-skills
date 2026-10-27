import unittest

from app import preferences
from app.store import Store


class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")

    def test_saved_language_is_used_next_session(self):
        preferences.save_language(self.store, "cust-ana", "DE")
        self.assertEqual(preferences.initial_state(self.store, "cust-ana"), {"user:language": "Deutsch"})

    def test_other_customer_does_not_see_it(self):
        preferences.save_language(self.store, "cust-ana", "de")
        self.assertIsNone(preferences.get_language(self.store, "cust-ben"))
        self.assertFalse(preferences.forget_language(self.store, "cust-ben"))
        self.assertEqual(preferences.get_language(self.store, "cust-ana"), "de")

    def test_forgotten_language_is_not_used_next_session(self):
        preferences.save_language(self.store, "cust-ana", "fr")
        self.assertTrue(preferences.forget_language(self.store, "cust-ana"))
        self.assertEqual(preferences.initial_state(self.store, "cust-ana"), {})

    def test_unsupported_language_is_refused(self):
        with self.assertRaises(preferences.UnsupportedLanguage):
            preferences.save_language(self.store, "cust-ana", "klingon")


if __name__ == "__main__":
    unittest.main()
