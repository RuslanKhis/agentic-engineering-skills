import unittest

from app.auth import Unauthenticated, principal_from_headers
from app.library import search_policies


class LibraryTests(unittest.TestCase):
    def test_search_returns_cited_sections(self):
        result = search_policies("can I work remotely abroad")
        self.assertEqual(result["status"], "ok")
        self.assertTrue(all("id" in s and "section" in s for s in result["sections"]))
        self.assertIn("HR-04", {s["id"] for s in result["sections"]})


class AuthTests(unittest.TestCase):
    def test_missing_assertion_is_refused(self):
        with self.assertRaises(Unauthenticated):
            principal_from_headers({}, lambda a, b: {"sub": "x"}, "aud")

    def test_verified_subject_is_the_user(self):
        p = principal_from_headers({"x-goog-iap-jwt-assertion": "t"}, lambda a, b: {"sub": "u-1"}, "aud")
        self.assertEqual(p.user_id, "u-1")


if __name__ == "__main__":
    unittest.main()
