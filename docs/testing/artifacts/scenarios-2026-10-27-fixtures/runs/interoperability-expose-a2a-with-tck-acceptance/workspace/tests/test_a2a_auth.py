import asyncio
import unittest

from triage.a2a_auth import (
    CARD_PATH, BearerAuthMiddleware, TokenInvalid, VerifierUnavailable,
)

SCOPE = "triage:invoke"


def verifier(token):
    if token == "good":
        return {"sub": "dealer-portal", "scope": f"{SCOPE} other"}
    if token == "noscope":
        return {"sub": "dealer-portal", "scope": "other"}
    if token == "nosub":
        return {"scope": SCOPE}
    if token == "outage":
        raise VerifierUnavailable("jwks down")
    raise TokenInvalid("bad")


async def downstream(scope, receive, send):
    user = scope.get("user")
    body = user.identity.encode() if user else b"anonymous"
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": body})


def call(path="/", method="POST", auth=None):
    headers = [(b"authorization", auth.encode())] if auth else []
    scope = {"type": "http", "method": method, "path": path, "headers": headers}
    sent = []

    async def send(message):
        sent.append(message)

    async def receive():
        return {"type": "http.request", "body": b""}

    app = BearerAuthMiddleware(downstream, verifier, SCOPE)
    asyncio.run(app(scope, receive, send))
    start, body = sent[0], sent[1]["body"]
    return start["status"], dict(start["headers"]), body


class AuthTests(unittest.TestCase):
    def test_missing_token_is_401_with_challenge(self):
        status, headers, _ = call()
        self.assertEqual(status, 401)
        self.assertIn(b"www-authenticate", headers)

    def test_invalid_token_is_401(self):
        self.assertEqual(call(auth="Bearer forged")[0], 401)

    def test_wrong_scheme_is_401(self):
        self.assertEqual(call(auth="Basic good")[0], 401)

    def test_token_without_subject_is_401(self):
        self.assertEqual(call(auth="Bearer nosub")[0], 401)

    def test_missing_scope_is_403(self):
        status, headers, _ = call(auth="Bearer noscope")
        self.assertEqual(status, 403)
        self.assertIn(b"insufficient_scope", headers[b"www-authenticate"])

    def test_verifier_outage_is_503_not_401(self):
        status, headers, _ = call(auth="Bearer outage")
        self.assertEqual(status, 503)
        self.assertNotIn(b"www-authenticate", headers)

    def test_valid_token_reaches_app_with_principal(self):
        self.assertEqual(call(auth="Bearer good"), (200, {}, b"dealer-portal"))

    def test_only_get_card_is_public(self):
        self.assertEqual(call(CARD_PATH, "GET")[0], 200)
        self.assertEqual(call(CARD_PATH, "POST")[0], 401)
        self.assertEqual(call("/.well-known/agent-card.json/x", "GET")[0], 401)


if __name__ == "__main__":
    unittest.main()
