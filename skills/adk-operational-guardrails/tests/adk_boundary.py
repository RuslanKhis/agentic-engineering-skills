"""Optional real-ADK, fake-model integration tests; no provider access.

Run explicitly with: python -m unittest discover -s tests -p adk_boundary.py -v
Requires the existing project environment with google-adk==2.8.0. No installation
or version change is performed. Test pattern adapted from the MIT companion;
see the skill's LICENSE and references/evidence.md.
"""

import asyncio
from contextlib import aclosing
from importlib import metadata
import importlib.util
from pathlib import Path
import unittest

if metadata.version("google-adk") != "2.8.0":
    raise RuntimeError("This integration fixture requires google-adk==2.8.0; adapt and validate for other pins.")

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import LlmCallsLimitExceededError
from google.adk.agents.run_config import RunConfig
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

SPEC = importlib.util.spec_from_file_location(
    "guard_asset", Path(__file__).resolve().parents[1] / "assets" / "invocation_guard.py"
)
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class ScriptedModel(BaseLlm):
    model: str = "offline-model"
    responses: list[LlmResponse]
    calls: int = 0
    stall: bool = False

    async def generate_content_async(self, llm_request, stream=False):
        self.calls += 1
        if self.stall:
            await asyncio.Event().wait()
        if self.calls > len(self.responses):
            raise AssertionError("Unexpected model dispatch")
        yield self.responses[self.calls - 1]


def calls(*identifiers):
    return LlmResponse(content=types.Content(role="model", parts=[
        types.Part(function_call=types.FunctionCall(
            id=f"call-{index}-{value}", name="lookup", args={"order_id": value},
        )) for index, value in enumerate(identifiers)
    ]))


class BoundaryTests(unittest.IsolatedAsyncioTestCase):
    async def runner(self, model, tool):
        sessions = InMemorySessionService()
        await sessions.create_session(app_name="offline", user_id="user", session_id="session")
        return Runner(
            app_name="offline", session_service=sessions,
            agent=LlmAgent(name="support", model=model, tools=[tool]),
        )

    async def consume(self, runner, *, model_calls=3, seconds=10):
        async with asyncio.timeout(seconds):
            async with aclosing(runner.run_async(
                user_id="user", session_id="session",
                new_message=types.Content(role="user", parts=[types.Part(text="Check the order")]),
                run_config=RunConfig(max_llm_calls=model_calls),
            )) as events:
                return [event async for event in events]

    async def test_terminal_repeat_stops_before_actual_second_execution(self):
        executions = []
        guard = GUARD.InvocationGuard(max_tool_calls=3, timeout_seconds=10)

        async def lookup(order_id: str) -> dict:
            """Look up the given order."""
            async def execute():
                executions.append(order_id)
                return {"status": "invalid_request"}
            return await guard.run(
                "lookup", {"order_id": order_id}, execute,
                classify=lambda result: "terminal_failure",
            )

        model = ScriptedModel(responses=[calls("invalid"), calls("invalid")])
        with self.assertRaisesRegex(GUARD.GuardStopped, "repeated_terminal_failure"):
            await self.consume(await self.runner(model, lookup))
        self.assertEqual(executions, ["invalid"])
        self.assertEqual(model.calls, 2)

    async def test_model_bound_is_separate_from_tool_allowance(self):
        executions = []
        guard = GUARD.InvocationGuard(max_tool_calls=10, timeout_seconds=10)

        async def lookup(order_id: str) -> dict:
            """Look up the given order."""
            async def execute():
                executions.append(order_id)
                return {"status": "found"}
            return await guard.run("lookup", {"order_id": order_id}, execute)

        model = ScriptedModel(responses=[calls("one"), calls("two"), calls("three")])
        with self.assertRaises(LlmCallsLimitExceededError):
            await self.consume(await self.runner(model, lookup), model_calls=2)
        self.assertEqual(model.calls, 2)
        self.assertEqual(executions, ["one", "two"])

    async def test_parallel_batch_admits_only_remaining_capacity(self):
        executions = []
        guard = GUARD.InvocationGuard(max_tool_calls=1, timeout_seconds=10)

        async def lookup(order_id: str) -> dict:
            """Look up the given order."""
            async def execute():
                executions.append(order_id)
                return {"status": "found"}
            return await guard.run("lookup", {"order_id": order_id}, execute)

        model = ScriptedModel(responses=[calls("one", "two")])
        with self.assertRaisesRegex(GUARD.GuardStopped, "tool_call_limit"):
            await self.consume(await self.runner(model, lookup))
        self.assertEqual(len(executions), 1)

    async def test_outer_deadline_stops_model_before_first_event(self):
        executions = []

        async def lookup(order_id: str) -> dict:
            """Look up the given order."""
            executions.append(order_id)
            return {"status": "found"}

        model = ScriptedModel(responses=[], stall=True)
        with self.assertRaises(TimeoutError):
            await asyncio.wait_for(
                self.consume(await self.runner(model, lookup), seconds=0.02), timeout=1,
            )
        self.assertEqual(executions, [])
        self.assertEqual(model.calls, 1)


if __name__ == "__main__":
    unittest.main()
