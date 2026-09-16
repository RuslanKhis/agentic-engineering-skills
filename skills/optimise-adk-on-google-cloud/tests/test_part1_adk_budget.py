"""Offline ADK nesting and aggregate logical-generation admission contracts.

Only deterministic BaseLlm implementations run. The in-memory admission helper is
test-only: it provides neither provider-attempt accounting nor durable,
multi-process or distributed budget coordination.
"""

import asyncio
from contextlib import ExitStack
import importlib.metadata
import unittest
from unittest.mock import patch


class AggregateLimitExceeded(RuntimeError):
    """The shared test allowance rejected a logical generation before dispatch."""


class PartOneAdkBudgetContract(unittest.TestCase):
    def setUp(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; this real-framework contract was not run")
        if version != "2.8.0":
            self.skipTest("This recorded contract requires ADK 2.8.0; preserve target pins")

    def exercise(self, *, framework_limit, aggregate_limit=None):
        events = []
        requests = []
        responses = []
        admission = []
        reserved = []
        dispatches = []
        saved = None

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
            from google.adk.agents.invocation_context import LlmCallsLimitExceededError
            from google.adk.agents.run_config import RunConfig
            from google.adk.apps import App
            from google.adk.models import BaseLlm
            from google.adk.models.llm_response import LlmResponse
            from google.adk.sessions import InMemorySessionService
            from google.adk.tools.agent_tool import AgentTool
            from google.genai import types

            def admit(name):
                admission.append((name, len(reserved)))
                if aggregate_limit is not None and len(reserved) >= aggregate_limit:
                    raise AggregateLimitExceeded("The shared test generation allowance is exhausted")
                # This synchronous check/reservation has no await or provider call
                # between them. Its scope is this single event-loop test only.
                reserved.append(name)

            class ScriptedModel(BaseLlm):
                model: str = "offline-part-one-budget"
                agent_name: str

                async def generate_content_async(self, llm_request, stream=False):
                    requests.append((self.agent_name, llm_request.model_copy(deep=True)))
                    admit(self.agent_name)
                    # Represents the substituted provider boundary. A rejected
                    # reservation must never reach this line or produce output.
                    dispatches.append((self.agent_name, len(reserved)))
                    if self.agent_name == "root_agent":
                        response = LlmResponse(
                            content=types.Content(role="model", parts=[
                                types.Part(function_call=types.FunctionCall(
                                    id="call_alpha", name="alpha_agent", args={"request": "Return ALPHA"}
                                )),
                                types.Part(function_call=types.FunctionCall(
                                    id="call_beta", name="beta_agent", args={"request": "Return BETA"}
                                )),
                            ]),
                            finish_reason=types.FinishReason.STOP,
                        )
                    else:
                        text = "ALPHA" if self.agent_name == "alpha_agent" else "BETA"
                        response = LlmResponse(
                            content=types.Content(role="model", parts=[types.Part(text=text)]),
                            finish_reason=types.FinishReason.STOP,
                        )
                    responses.append((self.agent_name, response))
                    yield response

            children = [
                Agent(name=name, model=ScriptedModel(agent_name=name))
                for name in ("alpha_agent", "beta_agent")
            ]
            root = Agent(
                name="root_agent",
                model=ScriptedModel(agent_name="root_agent"),
                tools=[AgentTool(agent=child) for child in children],
            )
            app = App(name="part_one_budget_contract", root_agent=root)

            async def run():
                nonlocal saved
                service = InMemorySessionService()
                runner = Runner(app=app, session_service=service)
                session = await service.create_session(app_name=app.name, user_id="synthetic-owner")
                try:
                    async for event in runner.run_async(
                        user_id=session.user_id,
                        session_id=session.id,
                        new_message=types.Content(role="user", parts=[types.Part(text="Ask both children")]),
                        run_config=RunConfig(max_llm_calls=framework_limit),
                    ):
                        events.append(event)
                finally:
                    saved = await service.get_session(
                        app_name=app.name, user_id=session.user_id, session_id=session.id
                    )
                    await runner.close()

            expected_error = (
                LlmCallsLimitExceededError if aggregate_limit is None else AggregateLimitExceeded
            )
            with self.assertRaises(expected_error):
                asyncio.run(run())

        return {
            "events": events,
            "requests": requests,
            "responses": responses,
            "admission": admission,
            "reserved": reserved,
            "dispatches": dispatches,
            "saved": saved,
            "expected_error_code": expected_error.__name__,
        }

    def assert_children_completed_before_root_was_blocked(self, result):
        self.assertCountEqual(
            [name for name, _ in result["dispatches"]],
            ["root_agent", "alpha_agent", "beta_agent"],
        )
        self.assertEqual(result["dispatches"][0], ("root_agent", 1))
        self.assertEqual([count for _, count in result["dispatches"]], [1, 2, 3])
        self.assertEqual(len(result["responses"]), 3)
        children = {
            name: response for name, response in result["responses"] if name != "root_agent"
        }
        self.assertEqual(set(children), {"alpha_agent", "beta_agent"})
        self.assertEqual(children["alpha_agent"].content.parts[0].text, "ALPHA")
        self.assertEqual(children["beta_agent"].content.parts[0].text, "BETA")
        self.assertTrue(all(response.finish_reason.value == "STOP" for response in children.values()))

        calls = [call for event in result["events"] for call in event.get_function_calls()]
        tool_results = [value for event in result["events"] for value in event.get_function_responses()]
        self.assertEqual({(call.id, call.name) for call in calls}, {
            ("call_alpha", "alpha_agent"), ("call_beta", "beta_agent")
        })
        self.assertEqual({(value.id, value.name) for value in tool_results}, {
            ("call_alpha", "alpha_agent"), ("call_beta", "beta_agent")
        })
        self.assertEqual(
            {value.name: value.response for value in tool_results},
            {"alpha_agent": {"result": "ALPHA"}, "beta_agent": {"result": "BETA"}},
        )
        # ADK marks a content-free error event as final too. Completion needs
        # error/status/content checks rather than is_final_response() alone.
        errors = [event for event in result["events"] if event.error_code]
        self.assertEqual([event.error_code for event in errors], [result["expected_error_code"]])
        self.assertTrue(all(event.is_final_response() for event in errors))
        self.assertTrue(all(event.content is None for event in errors))
        self.assertFalse(any(
            event.author == "root_agent" and event.is_final_response()
            and not event.error_code and event.content
            and any(part.text for part in event.content.parts or [])
            for event in result["events"]
        ))
        self.assertIsNotNone(result["saved"])
        saved_results = [value for event in result["saved"].events for value in event.get_function_responses()]
        self.assertEqual(
            [(value.id, value.name, value.response) for value in saved_results],
            [(value.id, value.name, value.response) for value in tool_results],
        )

    def test_framework_limit_is_not_an_aggregate_nested_generation_budget(self):
        result = self.exercise(framework_limit=1)
        self.assert_children_completed_before_root_was_blocked(result)
        self.assertEqual(len(result["requests"]), 3)
        self.assertEqual(len(result["admission"]), 3)
        self.assertEqual(len(result["reserved"]), 3)

    def test_shared_model_admission_rejects_next_generation_before_dispatch(self):
        result = self.exercise(framework_limit=10, aggregate_limit=3)
        self.assert_children_completed_before_root_was_blocked(result)
        self.assertEqual(len(result["requests"]), 4)
        self.assertEqual(result["admission"][-1], ("root_agent", 3))
        self.assertEqual(len(result["reserved"]), 3)
        self.assertEqual(len(result["dispatches"]), 3)
        # The blocked root continuation actually contains both completed tool
        # results; rejection was not caused by a missing prerequisite or routing.
        continuation = result["requests"][-1][1]
        self.assertEqual({
            part.function_response.name
            for content in continuation.contents
            for part in content.parts or []
            if part.function_response
        }, {"alpha_agent", "beta_agent"})


if __name__ == "__main__":
    unittest.main()
