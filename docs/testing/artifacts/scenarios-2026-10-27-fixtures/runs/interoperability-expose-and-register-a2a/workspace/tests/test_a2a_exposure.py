"""Offline tests. The auth tests need no ADK; the agent-surface tests skip when google-adk is absent."""
import asyncio
import importlib.util
import unittest

from research_agent.a2a_auth import CARD_PATH, CallerAuthMiddleware

ADK = importlib.util.find_spec("google.adk") is not None
OK = {"email": "service-1@gcp-sa-discoveryengine.iam.gserviceaccount.com", "email_verified": True}


def call(app, path="/", headers=None):
    sent = []

    async def send(msg):
        sent.append(msg)

    async def receive():
        return {"type": "http.request"}

    scope = {"type": "http", "path": path, "headers": [(k.encode(), v.encode()) for k, v in (headers or {}).items()]}
    asyncio.run(app(scope, receive, send))
    return sent[0]["status"]


async def inner(scope, receive, send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b""})


def mw(verifier):
    return CallerAuthMiddleware(inner, audience="https://x", allowed_emails={OK["email"]}, verifier=verifier)


class AuthTests(unittest.TestCase):
    def test_missing_token_401(self):
        self.assertEqual(call(mw(lambda t, a: OK)), 401)

    def test_invalid_token_401(self):
        def bad(t, a):
            raise ValueError("bad")
        self.assertEqual(call(mw(bad), headers={"authorization": "Bearer x"}), 401)

    def test_unlisted_principal_403(self):
        self.assertEqual(call(mw(lambda t, a: {**OK, "email": "evil@example.com"}), headers={"authorization": "Bearer x"}), 403)

    def test_unverified_email_403(self):
        self.assertEqual(call(mw(lambda t, a: {**OK, "email_verified": False}), headers={"authorization": "Bearer x"}), 403)

    def test_verifier_outage_503(self):
        def down(t, a):
            raise ConnectionError()
        self.assertEqual(call(mw(down), headers={"authorization": "Bearer x"}), 503)

    def test_allowed_caller_and_serverless_header(self):
        self.assertEqual(call(mw(lambda t, a: OK), headers={"x-serverless-authorization": "Bearer x"}), 200)

    def test_card_is_public(self):
        self.assertEqual(call(mw(lambda t, a: OK), path=CARD_PATH), 200)


@unittest.skipUnless(ADK, "google-adk not installed")
class SurfaceTests(unittest.TestCase):
    def test_a2a_agent_has_no_procurement_or_confirmable_tool(self):
        from research_agent.a2a_app import build_a2a_agent

        def walk(agent):
            yield agent
            for s in agent.sub_agents:
                yield from walk(s)

        for a in walk(build_a2a_agent()):
            for t in a.tools:
                name = getattr(t, "name", getattr(t, "__name__", ""))
                self.assertNotIn("procurement", name)
                self.assertFalse(getattr(t, "_require_confirmation", False))


class CardTests(unittest.TestCase):
    @unittest.skipUnless(ADK, "google-adk not installed")
    def test_card_declares_auth_and_no_purchase_skill(self):
        from research_agent.a2a_app import build_card

        card = build_card("https://svc.run.app/")
        self.assertEqual(card["url"], "https://svc.run.app")
        self.assertTrue(card["security"] and card["securitySchemes"])
        self.assertNotIn("procure", str(card["skills"]).lower())


if __name__ == "__main__":
    unittest.main()
