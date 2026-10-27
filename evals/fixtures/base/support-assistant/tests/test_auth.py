import unittest

from app.auth import Unauthenticated, principal_from_headers


def verifier(claims=None, error=None):
    def verify(assertion, audience):
        if error:
            raise error
        return claims
    return verify


class AuthTests(unittest.TestCase):
    def test_valid_assertion_gives_principal(self):
        p = principal_from_headers({"x-goog-iap-jwt-assertion": "jwt"},
                                   verifier({"sub": "cust-ana", "email": "ana@example.com"}), "aud")
        self.assertEqual(p.user_id, "cust-ana")

    def test_missing_assertion_is_refused(self):
        with self.assertRaises(Unauthenticated):
            principal_from_headers({}, verifier({"sub": "x"}), "aud")

    def test_bad_signature_is_refused(self):
        with self.assertRaises(Unauthenticated):
            principal_from_headers({"x-goog-iap-jwt-assertion": "jwt"}, verifier(error=ValueError("sig")), "aud")


if __name__ == "__main__":
    unittest.main()
