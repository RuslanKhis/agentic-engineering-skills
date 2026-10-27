import unittest

from app.auth import Unauthenticated, principal_from_headers


def verifier(claims=None, error=None):
    def verify(token, audience):
        if error:
            raise error
        return claims
    return verify


class AuthTests(unittest.TestCase):
    def test_valid_token_gives_principal(self):
        p = principal_from_headers({"authorization": "Bearer tok"},
                                   verifier({"sub": "cust-ana", "email": "ana@example.com"}), "proj")
        self.assertEqual(p.user_id, "cust-ana")

    def test_missing_token_is_refused(self):
        with self.assertRaises(Unauthenticated):
            principal_from_headers({}, verifier({"sub": "x"}), "proj")

    def test_bad_signature_is_refused(self):
        with self.assertRaises(Unauthenticated):
            principal_from_headers({"authorization": "Bearer tok"}, verifier(error=ValueError("sig")), "proj")


if __name__ == "__main__":
    unittest.main()
