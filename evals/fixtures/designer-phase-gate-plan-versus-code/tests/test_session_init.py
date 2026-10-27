import unittest

from app import session_init
from app.preferences import LANGUAGE_KEY, Preferences
from app.store import Store


class SessionInitTests(unittest.TestCase):
    def setUp(self):
        session_init._PROFILE_CACHE.clear()
        self.prefs = Preferences(Store(":memory:"))

    def test_saved_language_preloaded(self):
        self.prefs.save("cust-ana", "de")
        self.assertEqual(session_init.initial_state("cust-ana", self.prefs), {LANGUAGE_KEY: "de"})

    def test_no_language_gives_empty_state(self):
        self.assertEqual(session_init.initial_state("cust-ben", self.prefs), {})

    def test_second_session_reads_from_cache(self):
        self.prefs.save("cust-ana", "nl")
        session_init.initial_state("cust-ana", self.prefs)
        self.assertIn("cust-ana", session_init._PROFILE_CACHE)


if __name__ == "__main__":
    unittest.main()
