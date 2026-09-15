"""Real ADK compaction orchestration with deterministic model boundaries only.

This checks local context selection and retained storage, not summary quality,
provider execution, managed sessions or hosted Agent Runtime behaviour.
"""

import asyncio
import importlib.metadata
import unittest
from unittest.mock import patch


class RuntimeCompactionContract(unittest.TestCase):
    def setUp(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; standard-library checks remain available")
        if version != "2.8.0":
            self.skipTest("This recorded runtime contract requires ADK 2.8.0; preserve target pins")

    def exercise(self, *, preserve_app):
        from google.adk import Agent, Runner
        from google.adk.apps import App
        from google.adk.apps.app import EventsCompactionConfig
        from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
        from google.adk.models import BaseLlm
        from google.adk.models.llm_response import LlmResponse
        from google.adk.sessions import InMemorySessionService
        from google.genai import types
        from pydantic import Field

        class RecordedModel(BaseLlm):
            model: str = "offline-runtime-contract"
            reply: str
            requests: list[list[str]] = Field(default_factory=list)

            async def generate_content_async(self, llm_request, stream=False):
                self.requests.append([
                    part.text
                    for content in llm_request.contents
                    for part in content.parts or []
                    if part.text
                ])
                yield LlmResponse(
                    content=types.Content(role="model", parts=[types.Part(text=self.reply)]),
                    finish_reason=types.FinishReason.STOP,
                )

        answer_model = RecordedModel(reply="The issue is recorded.")
        summary_model = RecordedModel(
            reply="COMPACTED_POLICY_CONTEXT: invoice INV-QA-4812 was charged twice for 49 AUD."
        )
        app = App(
            name="runtime_contract",
            root_agent=Agent(name="support_agent", model=answer_model),
            events_compaction_config=EventsCompactionConfig(
                compaction_interval=2,
                overlap_size=0,
                summarizer=LlmEventSummarizer(llm=summary_model),
            ),
        )

        async def run():
            service = InMemorySessionService()
            runner = (
                Runner(app=app, session_service=service)
                if preserve_app
                else Runner(agent=app.root_agent, app_name=app.name, session_service=service)
            )
            session = await service.create_session(app_name=app.name, user_id="synthetic-owner")
            original_ids = set()
            try:
                for index, message in enumerate((
                    "IRRELEVANT_GREETING_MARKER. Invoice INV-QA-4812 was charged twice for 49 AUD.",
                    "Please retain the invoice and disputed amount.",
                    "Which invoice and amount were disputed?",
                )):
                    events = [event async for event in runner.run_async(
                        user_id="synthetic-owner",
                        session_id=session.id,
                        new_message=types.Content(role="user", parts=[types.Part(text=message)]),
                    )]
                    answers = [event for event in events if event.is_final_response()]
                    self.assertEqual(len(answers), 1)
                    self.assertEqual(answers[0].finish_reason, types.FinishReason.STOP)
                    saved = await service.get_session(
                        app_name=app.name, user_id="synthetic-owner", session_id=session.id
                    )
                    self.assertIsNotNone(saved)
                    if index == 0:
                        original_ids = {event.id for event in saved.events}
                        self.assertEqual(len(original_ids), 2)
                        self.assertEqual(summary_model.requests, [])
                    else:
                        self.assertTrue(original_ids.issubset({event.id for event in saved.events}))
                return saved
            finally:
                await runner.close()

        # The doubles replace both generation boundaries. An accidental socket
        # connection fails the test instead of reaching credentials or providers.
        with patch("socket.socket.connect", side_effect=AssertionError("Network is prohibited")):
            saved = asyncio.run(run())
        return answer_model, summary_model, saved

    def test_app_compacts_real_adk_context_without_deleting_original_events(self):
        answers, summaries, saved = self.exercise(preserve_app=True)
        self.assertEqual(len(answers.requests), 3)
        self.assertEqual(len(summaries.requests), 1)
        self.assertIn("INV-QA-4812", "\n".join(summaries.requests[0]))
        self.assertIn("IRRELEVANT_GREETING_MARKER", "\n".join(summaries.requests[0]))
        compactions = [event for event in saved.events if event.actions.compaction]
        self.assertEqual(len(compactions), 1)
        self.assertIn("COMPACTED_POLICY_CONTEXT", str(compactions[0].actions.compaction.compacted_content))
        next_request = "\n".join(answers.requests[2])
        self.assertIn("COMPACTED_POLICY_CONTEXT", next_request)
        self.assertIn("INV-QA-4812", next_request)
        self.assertIn("49 AUD", next_request)
        self.assertNotIn("IRRELEVANT_GREETING_MARKER", next_request)
        self.assertTrue(any(
            "IRRELEVANT_GREETING_MARKER" in (part.text or "")
            for event in saved.events if event.content
            for part in event.content.parts or []
        ))

    def test_agent_only_runner_does_not_inherit_the_apps_compaction(self):
        answers, summaries, saved = self.exercise(preserve_app=False)
        self.assertEqual(summaries.requests, [])
        self.assertFalse(any(event.actions.compaction for event in saved.events))
        next_request = "\n".join(answers.requests[2])
        self.assertIn("IRRELEVANT_GREETING_MARKER", next_request)
        self.assertNotIn("COMPACTED_POLICY_CONTEXT", next_request)


if __name__ == "__main__":
    unittest.main()
