import hashlib
import hmac
import unittest

from app.app_utils.identity import Unauthenticated, verify_staff_header

SECRET = b"test-secret"


def header(staff_id, ts, secret=SECRET):
    sig = hmac.new(secret, f"{staff_id}.{ts}".encode(), hashlib.sha256).hexdigest()
    return f"{staff_id}.{ts}.{sig}"


class IdentityTests(unittest.TestCase):
    def test_valid_header(self):
        self.assertEqual(verify_staff_header(header("s-100", 1000), SECRET, now=1010), "s-100")

    def test_forged_signature(self):
        with self.assertRaises(Unauthenticated):
            verify_staff_header(header("s-100", 1000, b"other"), SECRET, now=1010)

    def test_expired(self):
        with self.assertRaises(Unauthenticated):
            verify_staff_header(header("s-100", 1000), SECRET, now=5000)


if __name__ == "__main__":
    unittest.main()
