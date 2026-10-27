"""Follow-up memory over MCP, on both protocol eras. Needs google-adk and mcp 2.x.

CI sets REQUIRE_ADK=1 so a missing dependency fails instead of skipping.
"""
import json
import os
import unittest

try:
    import mcp
    from google.adk.agents import LlmAgent
    from google.adk.models.base_llm import BaseLlm
    from google.adk.models.llm_response import LlmResponse
    from google.genai import types

    from triage.mcp_server import build_server

    HAVE_DEPS = True
except ImportError:
    if os.environ.get("REQUIRE_ADK"):
        raise
    HAVE_DEPS = False


if HAVE_DEPS:

    class TurnCounter(BaseLlm):
        """Answers with how many user turns the model was shown."""

        model: str = "turn-counter"

        async def generate_content_async(self, llm_request, stream: bool = False):
            turns = sum(
                1 for c in llm_request.contents if c.role == "user" and any(p.text for p in c.parts)
            )
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=f"user_turns={turns}")]))


def _result(call) -> dict:
    if call.structured_content:
        return call.structured_content
    return json.loads(call.content[0].text)


@unittest.skipUnless(HAVE_DEPS, "google-adk / mcp not installed")
class FollowUpTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        agent = LlmAgent(name="warranty_triage", model=TurnCounter(), description="Triage.")
        self.server = build_server(agent)

    async def _two_calls(self, **client_kwargs):
        async with mcp.Client(self.server, **client_kwargs) as client:
            first = _result(await client.call_tool("warranty_triage", {"request": "Triage claim C-881"}))
            second = _result(
                await client.call_tool(
                    "warranty_triage",
                    {"request": "Why urgency 3?", "conversation_id": first["conversation_id"]},
                )
            )
        return first, second

    async def test_follow_up_remembered_modern(self):
        # Default client negotiates 2026-07-28: no connection, so the handle must carry state.
        first, second = await self._two_calls()
        self.assertEqual(first["answer"], "user_turns=1")
        self.assertEqual(second["answer"], "user_turns=2")

    async def test_follow_up_remembered_legacy(self):
        first, second = await self._two_calls(mode="legacy")
        self.assertEqual(second["answer"], "user_turns=2")

    async def test_without_id_starts_new_conversation(self):
        async with mcp.Client(self.server) as client:
            a = _result(await client.call_tool("warranty_triage", {"request": "one"}))
            b = _result(await client.call_tool("warranty_triage", {"request": "two"}))
        self.assertNotEqual(a["conversation_id"], b["conversation_id"])
        self.assertEqual(b["answer"], "user_turns=1")

    async def test_unknown_id_is_refused(self):
        async with mcp.Client(self.server) as client:
            call = await client.call_tool("warranty_triage", {"request": "x", "conversation_id": "nope"})
        self.assertTrue(call.is_error)
        self.assertIn("unknown or expired", call.content[0].text)


if __name__ == "__main__":
    unittest.main()
