import json
import unittest

from app.card_trust import CardRefused, PinnedKeyProvider, check_interface_origins

try:
    import jwt
    from cryptography.hazmat.primitives.asymmetric import ec
except ImportError:  # SDK extras not installed
    jwt = None

CARD = "https://partner.example/.well-known/agent-card.json"


def make_key(kid):
    key = ec.generate_private_key(ec.SECP256R1())
    jwk = json.loads(jwt.algorithms.ECAlgorithm.to_jwk(key.public_key()))
    jwk.update(kid=kid, use="sig", alg="ES256")
    return key, jwk


class OriginTests(unittest.TestCase):
    def test_same_origin_https_passes(self):
        check_interface_origins(["https://partner.example/a2a/warranty"], CARD)

    def test_other_host_refused(self):
        with self.assertRaises(CardRefused):
            check_interface_origins(["https://evil.example/a2a"], CARD)

    def test_http_refused(self):
        with self.assertRaises(CardRefused):
            check_interface_origins(["http://partner.example/a2a"], CARD)

    def test_no_interface_refused(self):
        with self.assertRaises(CardRefused):
            check_interface_origins([], CARD)


@unittest.skipIf(jwt is None, "PyJWT/cryptography not installed")
class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.k1, self.j1 = make_key("card-2026-10")
        self.k2, self.j2 = make_key("card-2027-01")
        self.rogue, self.jr = make_key("card-2026-10")
        self.allowed = {"card-2026-10", "card-2027-01"}

    def sign(self, key, kid):
        return jwt.encode({"x": 1}, key, algorithm="ES256", headers={"kid": kid})

    def verify(self, provider, token):
        header = jwt.get_unverified_header(token)
        return jwt.decode(token, provider(header["kid"], header.get("jku")), algorithms=["ES256"])

    def test_both_rotation_keys_verify(self):
        p = PinnedKeyProvider({"keys": [self.j1, self.j2]}, self.allowed)
        self.assertEqual(self.verify(p, self.sign(self.k1, "card-2026-10")), {"x": 1})
        self.assertEqual(self.verify(p, self.sign(self.k2, "card-2027-01")), {"x": 1})

    def test_attacker_key_with_pinned_kid_fails(self):
        p = PinnedKeyProvider({"keys": [self.j1]}, self.allowed)
        with self.assertRaises(jwt.InvalidSignatureError):
            self.verify(p, self.sign(self.rogue, "card-2026-10"))

    def test_unknown_kid_raises_pyjwt_error_subclass(self):
        p = PinnedKeyProvider({"keys": [self.j1]}, self.allowed)
        with self.assertRaises(jwt.PyJWTError):
            p("card-2099-01", None)

    def test_jku_is_ignored(self):
        p = PinnedKeyProvider({"keys": [self.j1]}, self.allowed)
        with self.assertRaises(jwt.InvalidSignatureError):
            self.verify(p, jwt.encode({"x": 1}, self.rogue, algorithm="ES256",
                                      headers={"kid": "card-2026-10", "jku": "https://cdn.evil.example/jwks.json"}))

    def test_kid_not_in_allowlist_is_not_loaded(self):
        with self.assertRaises(CardRefused):
            PinnedKeyProvider({"keys": [self.j2]}, {"card-2026-10"})

    def test_missing_file_refuses(self):
        with self.assertRaises(CardRefused):
            PinnedKeyProvider.from_file("/nonexistent/jwks.json", self.allowed)


if __name__ == "__main__":
    unittest.main()
