"""Scripted-model Runner tests: no live model, no Google Cloud. Need google-adk installed."""
from __future__ import annotations

import asyncio
import importlib.util
import logging
import unittest

try:
    HAS_ADK = importlib.util.find_spec("google.adk") is not None
except ModuleNotFoundError:
    HAS_ADK = False


@unittest.skipUnless(HAS_ADK, "google-adk not installed")
class ConversationSinkTests(unittest.TestCase):
    def setUp(self):
        from google.adk.models import BaseLlm, LlmResponse
        from google.adk.runners import InMemoryRunner
        from google.genai import types

        from app import agent as agent_module
        from app.screening import screening
        from tests.fakes import configure_fakes
        from tests.runner.fake_screening import FakeArmor, FakeDlp

        self.types = types
        self.store, self.pay, self.mail = configure_fakes()
        screening._armor, screening._dlp = FakeArmor(), FakeDlp()
        self.requests = []
        script = self.script = []

        class ScriptedModel(BaseLlm):
            model: str = "scripted"

            async def generate_content_async(inner, llm_request, stream=False):
                self.requests.append(llm_request)
                yield script.pop(0) if script else LlmResponse(
                    content=types.Content(role="model", parts=[types.Part(text="Done.")]))

        self.LlmResponse = LlmResponse
        self.runner = InMemoryRunner(agent=agent_module.make_agent(ScriptedModel()), app_name="support")

    def run_turn(self, text, user_id="cust-ana"):
        async def go():
            session = await self.runner.session_service.create_session(app_name="support", user_id=user_id)
            msg = self.types.Content(role="user", parts=[self.types.Part(text=text)])
            events = [e async for e in self.runner.run_async(user_id=user_id, session_id=session.id,
                                                             new_message=msg)]
            return session, events
        return asyncio.run(go())

    def test_reply_canary_is_deidentified_before_it_is_stored(self):
        from tests.runner import canaries

        self.script.append(self.LlmResponse(content=self.types.Content(
            role="model", parts=[self.types.Part(text=f"I've noted {canaries.EMAIL} for the refund.")])))
        with self.assertLogs("support", level="INFO") as logs:
            logging.getLogger("support").info("turn start")
            _, events = self.run_turn("Please refund HO-10442")
        stored = " ".join(p.text or "" for e in events if e.content for p in e.content.parts or [])
        self.assertNotIn(canaries.EMAIL, stored)
        self.assertNotIn(canaries.EMAIL, "\n".join(logs.output))

    def test_refund_tool_call_carries_no_card_number(self):
        from tests.runner import canaries

        self.script.append(self.LlmResponse(content=self.types.Content(role="model", parts=[
            self.types.Part(function_call=self.types.FunctionCall(
                name="issue_refund", args={"order_id": "HO-10442", "amount_cents": 1000, "reason": "torn"}))])))
        self.run_turn(f"Refund HO-10442 to card {canaries.CARD}")
        self.assertTrue(self.pay.requests)
        self.assertNotIn(canaries.CARD, str(self.pay.requests))


if __name__ == "__main__":
    unittest.main()
