import os
import tempfile
import unittest

from app.auth import Principal
from app.profiles import ProfileNotFound, profile_view, rename
from app.store import Store


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")
        self.store.upsert_profile("cust-ana", "Ana")
        self.ana = Principal("cust-ana", "ana@example.com")
        self.ben = Principal("cust-ben", "ben@example.com")

    def test_own_profile(self):
        self.assertEqual(profile_view(self.store, self.ana)["display_name"], "Ana")

    def test_unknown_caller_has_no_profile(self):
        with self.assertRaises(ProfileNotFound):
            profile_view(self.store, self.ben)

    def test_rename_changes_only_the_callers_row(self):
        self.store.upsert_profile("cust-ben", "Ben")
        rename(self.store, self.ana, "Ana P")
        self.assertEqual(profile_view(self.store, self.ben)["display_name"], "Ben")

    def test_profile_survives_reopening_the_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "support.db")
            Store(path).upsert_profile("cust-ana", "Ana")
            self.assertEqual(profile_view(Store(path), self.ana)["display_name"], "Ana")


if __name__ == "__main__":
    unittest.main()
