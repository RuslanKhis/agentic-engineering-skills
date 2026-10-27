import unittest

from app.a2a_card import CardRefused, check_rpc_origins, pinned_key_provider

CARD = "https://partner.example/.well-known/agent-card.json"

try:
    import jwt  # noqa: F401
    from cryptography.hazmat.primitives.asymmetric import ec
    HAVE_JWT = True
except ImportError:
    HAVE_JWT = False


class OriginTests(unittest.TestCase):
    def test_same_origin_https_passes(self):
        check_rpc_origins(["https://partner.example/a2a/warranty"], CARD)

    def test_other_host_is_refused(self):
        with self.assertRaises(CardRefused):
            check_rpc_origins(["https://evil.example/a2a"], CARD)

    def test_http_card_is_refused(self):
        with self.assertRaises(CardRefused):
            check_rpc_origins(["http://partner.example/a2a"], "http://partner.example/card.json")

    def test_no_interface_is_refused(self):
        with self.assertRaises(CardRefused):
            check_rpc_origins([], CARD)


@unittest.skipUnless(HAVE_JWT, "PyJWT and cryptography not installed")
class KeyProviderTests(unittest.TestCase):
    def setUp(self):
        from jwt.algorithms import ECAlgorithm
        key = ec.generate_private_key(ec.SECP256R1())
        import json
        jwk = json.loads(ECAlgorithm.to_jwk(key.public_key()))
        self.jwks = {"keys": [dict(jwk, kid="card-2026-10"), dict(jwk, kid="rogue")]}

    def test_known_kid_returns_key(self):
        provider = pinned_key_provider(self.jwks, ["card-2026-10"])
        self.assertIsNotNone(provider("card-2026-10", None))

    def test_jku_is_ignored(self):
        provider = pinned_key_provider(self.jwks, ["card-2026-10"])
        self.assertIsNotNone(provider("card-2026-10", "https://attacker.example/jwks.json"))

    def test_unknown_or_unlisted_kid_raises_pyjwt_error(self):
        provider = pinned_key_provider(self.jwks, ["card-2026-10"])
        for kid in ("card-2027-01", "rogue", None):
            with self.assertRaises(jwt.PyJWTError):
                provider(kid, None)


if __name__ == "__main__":
    unittest.main()
