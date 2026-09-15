"""OFFLINE real ADK orchestration; Gemini boundary substituted, network blocked.

The fixture contracts adapt the MIT-licensed companion's Runner test approach.
They contain no companion imports, real model ID, credentials or cloud calls.
"""

import asyncio
import importlib.metadata
import os
import re
import socket
import tempfile
import unittest
from unittest.mock import patch

if importlib.metadata.version("google-adk") != "2.8.0":
    raise RuntimeError(
        "Runtime contract fixture requires google-adk==2.8.0; preserve target pins."
    )

from google.adk.agents import LlmAgent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types


def response(text):
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=text)])
    )


class RuntimeContracts(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)

        def forbidden(*_args, **_kwargs):
            raise AssertionError("Network forbidden in OFFLINE contract tests")

        self.enterContext(
            patch.dict(
                os.environ,
                {
                    "GOOGLE_APPLICATION_CREDENTIALS": self.temp.name + "/absent.json",
                    "CLOUDSDK_CONFIG": self.temp.name + "/cloud-config",
                    "PYTHON_DOTENV_DISABLED": "1",
                    "GOOGLE_API_KEY": "",
                    "GEMINI_API_KEY": "",
                    "GOOGLE_CLOUD_PROJECT": "",
                    "GOOGLE_GENAI_USE_ENTERPRISE": "false",
                    "GOOGLE_GENAI_USE_VERTEXAI": "false",
                },
            )
        )
        for name in ("connect", "connect_ex"):
            self.enterContext(patch.object(socket.socket, name, forbidden))
        for name in ("create_connection", "getaddrinfo"):
            self.enterContext(patch.object(socket, name, forbidden))
        self.service = InMemorySessionService()
        self.calls = []

    async def run_root(self, root, responder):
        runner = Runner(
            app_name="contract_fixture", agent=root, session_service=self.service
        )
        self.addAsyncCleanup(runner.close)
        await self.service.create_session(
            app_name="contract_fixture", user_id="synthetic-user", session_id="one"
        )
        calls = self.calls

        async def generate(_model, request, stream=False):
            match = re.search(
                r'Your internal name is "([^"]+)"',
                str(request.config.system_instruction),
            )
            if match is None:
                raise AssertionError("Unexpected model boundary")
            name = match.group(1)
            calls.append(name)
            yield await responder(name, request)

        with patch.object(Gemini, "generate_content_async", generate):
            events = [
                event
                async for event in runner.run_async(
                    user_id="synthetic-user",
                    session_id="one",
                    new_message=types.Content(
                        role="user", parts=[types.Part(text="synthetic request")]
                    ),
                )
            ]
        return events

    async def state(self):
        session = await self.service.get_session(
            app_name="contract_fixture", user_id="synthetic-user", session_id="one"
        )
        return session.state

    def agent(self, name, output_key, **kwargs):
        return LlmAgent(
            name=name,
            model="gemini-offline-fixture",
            output_key=output_key,
            instruction=kwargs.pop("instruction", "Return the fixture result."),
            **kwargs
        )

    async def test_parallel_overlaps_and_preserves_both_populated_outputs(self):
        started, barrier = set(), asyncio.Event()
        root = ParallelAgent(
            name="parallel",
            sub_agents=[self.agent("a", "result_a"), self.agent("b", "result_b")],
        )

        async def respond(name, _request):
            started.add(name)
            if len(started) == 2:
                barrier.set()
            await asyncio.wait_for(barrier.wait(), timeout=2)
            return response("populated-" + name)

        await self.run_root(root, respond)
        self.assertCountEqual(self.calls, ["a", "b"])
        self.assertEqual(
            await self.state(), {"result_a": "populated-a", "result_b": "populated-b"}
        )

    async def test_sequence_propagates_failure_without_repeating_completed_work(self):
        root = SequentialAgent(
            name="sequence",
            sub_agents=[
                self.agent("writer", "draft"),
                self.agent("reviewer", "final_copy", instruction="Review {draft}"),
            ],
        )

        async def respond(name, request):
            if name == "writer":
                return response("actual draft")
            self.assertIn("actual draft", str(request.config.system_instruction))
            raise RuntimeError("synthetic downstream failure")

        with self.assertRaisesRegex(RuntimeError, "synthetic downstream failure"):
            await self.run_root(root, respond)
        self.assertEqual(self.calls, ["writer", "reviewer"])
        self.assertEqual(await self.state(), {"draft": "actual draft"})

    async def test_loop_executes_real_exit_tool_and_skips_reviser(self):
        effects = []

        def exit_loop(tool_context: ToolContext) -> dict:
            """Stop when the synthetic draft meets the fixture's criteria."""
            effects.append("exit")
            tool_context.actions.escalate = True
            return {}

        root = SequentialAgent(
            name="refine",
            sub_agents=[
                self.agent("writer", "draft"),
                LoopAgent(
                    name="loop",
                    max_iterations=5,
                    sub_agents=[
                        self.agent("critic", "criticism", tools=[exit_loop]),
                        self.agent("reviser", "draft"),
                    ],
                ),
            ],
        )
        critic_turns = 0

        async def respond(name, _request):
            nonlocal critic_turns
            if name == "writer":
                return response("retained artefact")
            self.assertEqual(name, "critic", "Reviser ran after approval")
            critic_turns += 1
            if critic_turns == 1:
                return LlmResponse(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part(
                                function_call=types.FunctionCall(
                                    name="exit_loop", args={}
                                )
                            )
                        ],
                    )
                )
            return response("Approved")

        await self.run_root(root, respond)
        self.assertEqual(effects, ["exit"])
        self.assertEqual(self.calls, ["writer", "critic", "critic"])
        self.assertEqual((await self.state())["draft"], "retained artefact")


if __name__ == "__main__":
    unittest.main()
