import unittest

from app.preferences import LANGUAGE_KEY, Preferences, UnsupportedLanguage
from app.store import Store


class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")
        self.prefs = Preferences(self.store)

    def test_saved_language_is_loaded_next_session(self):
        self.prefs.save("cust-ana", "DE")
        state = {}
        self.prefs.load_into_state("cust-ana", state)
        self.assertEqual(state[LANGUAGE_KEY], "de")

    def test_other_user_cannot_read_or_forget(self):
        self.prefs.save("cust-ana", "de")
        self.assertIsNone(self.prefs.get("cust-ben"))
        self.assertFalse(self.prefs.forget("cust-ben"))
        self.assertEqual(self.prefs.get("cust-ana"), "de")

    def test_forget_clears_row_and_session_copy(self):
        self.prefs.save("cust-ana", "fr")
        state = {LANGUAGE_KEY: "fr"}
        self.assertTrue(self.prefs.forget("cust-ana", state))
        self.assertNotIn(LANGUAGE_KEY, state)
        fresh = {}
        self.prefs.load_into_state("cust-ana", fresh)
        self.assertEqual(fresh, {})

    def test_forgotten_row_is_kept_with_deleted_at(self):
        self.prefs.save("cust-ana", "fr")
        self.prefs.forget("cust-ana")
        row = self.store.conn.execute("SELECT deleted_at FROM preferences WHERE user_id = 'cust-ana'").fetchone()
        self.assertIsNotNone(row["deleted_at"])

    def test_unsupported_language_is_refused(self):
        with self.assertRaises(UnsupportedLanguage):
            self.prefs.save("cust-ana", "klingon")


if __name__ == "__main__":
    unittest.main()
