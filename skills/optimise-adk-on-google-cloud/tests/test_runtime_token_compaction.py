"""ADK 2.8 token compaction through real Runner/model-request boundaries.

Synthetic usage and deterministic BaseLlm responses exercise framework control
flow only. These tests do not verify provider token counting, summary quality,
managed sessions, hosted execution or a hard context-size budget.
"""

import asyncio
from contextlib import ExitStack
import importlib.metadata
import unittest
from unittest.mock import patch


class RuntimeTokenCompactionContract(unittest.TestCase):
    def setUp(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; this real-framework contract was not run")
        if version != "2.8.0":
            self.skipTest("This recorded contract requires ADK 2.8.0; preserve target pins")

    def exercise(self, scenario):
        requests = []
        summaries = []
        timeline = []
        snapshots = []
        invocations = []

        with ExitStack() as guards:
            for target in (
                "socket.socket.connect",
                "socket.socket.connect_ex",
                "socket.socket.sendto",
                "socket.create_connection",
                "socket.getaddrinfo",
                "socket.gethostbyname",
                "socket.gethostbyname_ex",
                "socket.gethostbyaddr",
            ):
                guards.enter_context(patch(target, side_effect=AssertionError("Network is prohibited")))

            from google.adk import Agent, Runner
            from google.adk.apps import App
            from google.adk.apps.app import EventsCompactionConfig
            from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
            from google.adk.models import BaseLlm
            from google.adk.models.llm_response import LlmResponse
            from google.adk.sessions import InMemorySessionService
            from google.genai import types

            class AnswerModel(BaseLlm):
                model: str = "offline-token-compaction-answer"

                async def generate_content_async(self, llm_request, stream=False):
                    requests.append(llm_request.model_copy(deep=True))
                    timeline.append("answer")
                    first_call = len(requests) == 1
                    if scenario == "tool" and first_call:
                        part = types.Part(function_call=types.FunctionCall(
                            id="call-exact-invoice", name="read_invoice",
                            args={"invoice_id": "INV-PAIR-ARGUMENT"},
                        ))
                    else:
                        part = types.Part(text="The invoice issue is recorded.")
                    # A short first request is below the character estimate;
                    # synthetic observed usage independently crosses the trigger.
                    observed_usage = 100 if first_call and scenario != "oversized" else 1
                    yield LlmResponse(
                        content=types.Content(role="model", parts=[part]),
                        finish_reason=types.FinishReason.STOP,
                        usage_metadata=types.GenerateContentResponseUsageMetadata(
                            prompt_token_count=observed_usage,
                        ),
                    )

            class SummaryModel(BaseLlm):
                model: str = "offline-token-compaction-summary"

                async def generate_content_async(self, llm_request, stream=False):
                    summaries.append(llm_request.model_copy(deep=True))
                    timeline.append("summary")
                    yield LlmResponse(
                        content=types.Content(role="model", parts=[
                            types.Part(text="COMPACTED_ISSUE: invoice INV-CONTEXT needs checking.")
                        ]),
                        finish_reason=types.FinishReason.STOP,
                        usage_metadata=types.GenerateContentResponseUsageMetadata(
                            prompt_token_count=1,
                        ),
                    )

            async def read_invoice(invoice_id: str) -> dict:
                """Read one synthetic invoice without network or storage."""
                self.assertEqual(invoice_id, "INV-PAIR-ARGUMENT")
                return {"invoice_id": invoice_id, "status": "PAIR_RESPONSE_OK"}

            app = App(
                name="runtime_token_contract",
                root_agent=Agent(
                    name="support_agent",
                    model=AnswerModel(),
                    tools=[read_invoice] if scenario == "tool" else [],
                ),
                events_compaction_config=EventsCompactionConfig(
                    token_threshold=100,
                    event_retention_size=1,
                    summarizer=LlmEventSummarizer(llm=SummaryModel()),
                ),
            )
            messages = (
                ["OVERSIZED_FIRST_INPUT:" + "x" * 4096]
                if scenario == "oversized"
                else ["RAW_ISSUE_MARKER: check invoice INV-CONTEXT."]
            )
            if scenario == "usage":
                messages.append("What invoice needs checking?")

            async def run():
                service = InMemorySessionService()
                runner = Runner(app=app, session_service=service)
                session = await service.create_session(
                    app_name=app.name, user_id="synthetic-owner",
                )
                try:
                    for message in messages:
                        events = [event async for event in runner.run_async(
                            user_id=session.user_id,
                            session_id=session.id,
                            new_message=types.Content(role="user", parts=[types.Part(text=message)]),
                        )]
                        invocations.append(events)
                        saved = await service.get_session(
                            app_name=app.name, user_id=session.user_id, session_id=session.id,
                        )
                        self.assertIsNotNone(saved)
                        snapshots.append(saved.model_copy(deep=True))
                finally:
                    await runner.close()

            asyncio.run(run())

        for events in invocations:
            self.assertFalse(any(event.error_code or event.error_message for event in events))
            answers = [event for event in events if event.is_final_response() and event.content]
            self.assertEqual(len(answers), 1)
            self.assertEqual(answers[0].finish_reason.value, "STOP")
        return requests, summaries, snapshots, timeline, messages

    @staticmethod
    def text(request):
        return "\n".join(
            part.text for content in request.contents for part in content.parts or [] if part.text
        )

    def test_observed_usage_compacts_short_history_before_next_model_request(self):
        requests, summaries, snapshots, timeline, _ = self.exercise("usage")
        self.assertEqual(timeline, ["answer", "summary", "answer"])
        self.assertEqual(len(summaries), 1)
        self.assertIn("RAW_ISSUE_MARKER", self.text(requests[0]))
        self.assertIn("RAW_ISSUE_MARKER", self.text(summaries[0]))
        self.assertNotIn("RAW_ISSUE_MARKER", self.text(requests[1]))
        self.assertIn("COMPACTED_ISSUE", self.text(requests[1]))
        compactions = [event for event in snapshots[0].events if event.actions.compaction]
        self.assertEqual(len(compactions), 1)
        original = next(event for event in snapshots[0].events if event.author == "user" and event.content)
        self.assertIn(original.id, {event.id for event in snapshots[1].events})
        self.assertEqual(compactions[0].actions.compaction.start_timestamp, original.timestamp)
        self.assertEqual(compactions[0].actions.compaction.end_timestamp, original.timestamp)

    def test_token_threshold_does_not_reject_oversized_first_input(self):
        requests, summaries, snapshots, timeline, messages = self.exercise("oversized")
        self.assertGreater(len(messages[0]) // 4, 100)
        self.assertEqual(timeline, ["answer"])
        self.assertEqual(self.text(requests[0]), messages[0])
        self.assertEqual(summaries, [])
        self.assertFalse(any(event.actions.compaction for event in snapshots[0].events))

    def test_retention_keeps_function_call_with_response_in_next_request(self):
        requests, summaries, snapshots, timeline, _ = self.exercise("tool")
        self.assertEqual(timeline, ["answer", "summary", "answer"])
        self.assertEqual(len(summaries), 1)
        next_parts = [part for content in requests[1].contents for part in content.parts or []]
        calls = [part.function_call for part in next_parts if part.function_call]
        responses = [part.function_response for part in next_parts if part.function_response]
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(responses), 1)
        self.assertEqual(calls[0].id, responses[0].id)
        self.assertEqual(calls[0].name, "read_invoice")
        self.assertEqual(responses[0].response["status"], "PAIR_RESPONSE_OK")
        self.assertIn("COMPACTED_ISSUE", self.text(requests[1]))
        self.assertNotIn("RAW_ISSUE_MARKER", self.text(requests[1]))
        self.assertIn("RAW_ISSUE_MARKER", self.text(summaries[0]))
        self.assertNotIn("INV-PAIR-ARGUMENT", self.text(summaries[0]))
        saved = snapshots[0]
        compactions = [event for event in saved.events if event.actions.compaction]
        self.assertEqual(len(compactions), 1)
        raw_tool_events = [event for event in saved.events if event.get_function_calls() or event.get_function_responses()]
        self.assertEqual(len(raw_tool_events), 2)
        # Although retention_size is one, both protocol events remain outside
        # the compacted prefix and reach the actual continuation request.
        self.assertTrue(all(
            event.timestamp > compactions[0].actions.compaction.end_timestamp
            for event in raw_tool_events
        ))


if __name__ == "__main__":
    unittest.main()
