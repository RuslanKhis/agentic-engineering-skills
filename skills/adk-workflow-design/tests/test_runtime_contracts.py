"""OFFLINE real ADK orchestration; Gemini boundary substituted, network blocked.

The fixture contracts adapt the MIT-licensed companion's Runner test approach.
They contain no companion imports, real model ID, credentials or cloud calls.
"""

import asyncio
from collections.abc import AsyncGenerator
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

from google.adk import Context, Workflow
from google.adk.agents import LlmAgent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.genai import types
from pydantic import BaseModel


def response(text):
    return LlmResponse(
        content=types.Content(role="model", parts=[types.Part(text=text)])
    )


def tool_call(name, **args):
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=types.FunctionCall(name=name, args=args))],
        )
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

    async def run_root(self, root, responder, *, initial_state=None):
        runner = await self.make_runner(root, initial_state=initial_state)
        return await self.run_turn(runner, responder)

    async def make_runner(self, root, *, initial_state=None):
        runner = Runner(
            app_name="contract_fixture", agent=root, session_service=self.service
        )
        self.addAsyncCleanup(runner.close)
        await self.service.create_session(
            app_name="contract_fixture",
            user_id="synthetic-user",
            session_id="one",
            state=initial_state,
        )
        return runner

    async def run_turn(self, runner, responder):
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

    async def test_failed_second_turn_keeps_prior_output_key_in_same_session(self):
        """A stored final key is not proof of success for the current invocation.

        Gate consumption on this turn's completion and result provenance: a
        failed downstream step leaves the previous successful final key intact.
        """
        root = SequentialAgent(
            name="sequence",
            sub_agents=[
                self.agent("writer", "draft"),
                self.agent("reviewer", "final_copy", instruction="Review {draft}"),
            ],
        )
        runner = await self.make_runner(root)

        async def first_turn(name, request):
            if name == "writer":
                return response("first draft")
            self.assertIn("first draft", str(request.config.system_instruction))
            return response("first approved copy")

        await self.run_turn(runner, first_turn)
        self.assertEqual(
            await self.state(),
            {"draft": "first draft", "final_copy": "first approved copy"},
        )

        async def second_turn(name, request):
            if name == "writer":
                return response("second draft")
            self.assertIn("second draft", str(request.config.system_instruction))
            raise RuntimeError("synthetic second-turn review failure")

        with self.assertRaisesRegex(
            RuntimeError, "synthetic second-turn review failure"
        ):
            await self.run_turn(runner, second_turn)
        self.assertEqual(self.calls, ["writer", "reviewer", "writer", "reviewer"])
        self.assertEqual(
            await self.state(),
            {"draft": "second draft", "final_copy": "first approved copy"},
        )

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

    async def test_before_model_substitution_persists_output_and_state_delta(self):
        """Return LlmResponse; reassign copied state; drain before reading storage."""
        callback_calls = []

        def use_receipt(callback_context, llm_request):
            callback_calls.append(callback_context.agent_name)
            receipt = dict(callback_context.state["receipt"])
            receipt["status"] = "ready"
            # Mutating a nested dictionary alone does not register a state delta.
            callback_context.state["receipt"] = receipt
            return response("Synthetic receipt is ready.")

        root = self.agent(
            "receipt_reader", "confirmation", before_model_callback=use_receipt
        )

        async def unexpected_model(_name, _request):
            self.fail("before_model must bypass the Gemini boundary")

        events = await self.run_root(
            root,
            unexpected_model,
            initial_state={"receipt": {"id": "synthetic-receipt", "status": "pending"}},
        )
        expected_receipt = {"id": "synthetic-receipt", "status": "ready"}
        self.assertEqual(callback_calls, ["receipt_reader"])
        self.assertEqual(self.calls, [])
        self.assertEqual(
            events[-1].content.parts[0].text, "Synthetic receipt is ready."
        )
        self.assertTrue(
            any(
                event.actions.state_delta.get("receipt") == expected_receipt
                for event in events
            )
        )
        self.assertEqual(
            await self.state(),
            {
                "receipt": expected_receipt,
                "confirmation": "Synthetic receipt is ready.",
            },
        )

    async def test_before_tool_denies_repeated_calls_and_allows_control(self):
        """Nonempty denial stops a hook chain; None permits real tool dispatch.

        This synthetic allowlist exercises callback mechanics, not caller
        authentication, backend authorization, or idempotency of permitted calls.
        """
        effects, checked, observed = [], [], []
        denial = {"status": "denied", "reason": "fixture policy"}

        def write_record(record_id: str) -> dict:
            """Record a synthetic in-memory side effect."""
            effects.append(record_id)
            return {"status": "written", "record_id": record_id}

        def enforce_fixture_policy(tool, args, tool_context):
            self.assertEqual(tool.name, "write_record")
            checked.append(args["record_id"])
            if args["record_id"] != "allowed-record":
                return dict(denial)
            return None

        def observe_permitted_call(tool, args, tool_context):
            observed.append(args["record_id"])
            return None

        root = self.agent(
            "record_writer",
            "confirmation",
            tools=[write_record],
            before_tool_callback=[enforce_fixture_policy, observe_permitted_call],
        )
        scripted = iter(
            [
                tool_call("write_record", record_id="blocked-record"),
                tool_call("write_record", record_id="blocked-record"),
                tool_call("write_record", record_id="allowed-record"),
                response("Synthetic dispatch complete."),
            ]
        )

        async def respond(_name, _request):
            return next(scripted)

        events = await self.run_root(root, respond)
        results = [
            result.response
            for event in events
            for result in event.get_function_responses()
        ]
        self.assertEqual(
            checked, ["blocked-record", "blocked-record", "allowed-record"]
        )
        self.assertEqual(observed, ["allowed-record"])
        self.assertEqual(effects, ["allowed-record"])
        self.assertEqual(
            results,
            [denial, denial, {"status": "written", "record_id": "allowed-record"}],
        )
        self.assertEqual(self.calls, ["record_writer"] * 4)
        self.assertEqual(
            (await self.state())["confirmation"], "Synthetic dispatch complete."
        )

    async def test_empty_tool_override_is_overwritten_by_later_none_in_adk_2_8(self):
        """Pinned SDK trap, not a safe recipe: a later None replaces an empty {}.

        Keep the positive nonempty-denial test beside this version-specific
        behavior check; reconsider this expectation when deliberately upgrading.
        """
        effects, hooks = [], []

        def write_record(record_id: str) -> dict:
            """Record a synthetic in-memory side effect."""
            effects.append(record_id)
            return {"status": "written"}

        def empty_override(tool, args, tool_context):
            hooks.append("empty")
            return {}

        def later_observer(tool, args, tool_context):
            hooks.append("later")
            return None

        root = self.agent(
            "empty_override_writer",
            "confirmation",
            tools=[write_record],
            before_tool_callback=[empty_override, later_observer],
        )
        scripted = iter(
            [
                tool_call("write_record", record_id="synthetic-record"),
                response("Synthetic dispatch complete."),
            ]
        )

        async def respond(_name, _request):
            return next(scripted)

        events = await self.run_root(root, respond)
        self.assertEqual(hooks, ["empty", "later"])
        self.assertEqual(effects, ["synthetic-record"])
        self.assertEqual(
            [
                result.response
                for event in events
                for result in event.get_function_responses()
            ],
            [{"status": "written"}],
        )

    async def test_typed_workflow_consumes_empty_output_and_drains_past_progress(self):
        """Select the designated node's output using is not None; retain [].

        Text is progress here, not the result. Exhaust the stream before
        checking completion state; early text does not establish success.
        """

        class RecordBatch(BaseModel):
            record_ids: list[str]

        def prepare_batch(node_input: str) -> RecordBatch:
            return RecordBatch(record_ids=["synthetic-record"])

        async def select_records(
            ctx: Context, node_input: RecordBatch
        ) -> AsyncGenerator[types.Content | list[str], None]:
            self.assertIsInstance(node_input, RecordBatch)
            self.assertEqual(node_input.record_ids, ["synthetic-record"])
            yield types.Content(
                role="model", parts=[types.Part(text="Checking synthetic records.")]
            )
            # An empty selection is a valid, meaningful structured result.
            yield []
            ctx.state["selection_complete"] = True

        root = Workflow(
            name="typed_selection", edges=[("START", prepare_batch, select_records)]
        )

        async def unexpected_model(_name, _request):
            self.fail("The ordinary-code Workflow must not call Gemini")

        events = await self.run_root(root, unexpected_model)
        outputs, progress = [], []
        for event in events:
            # Plain Workflow nodes share the workflow author; node_info carries
            # the node identity. This fixture has one selection node/run.
            path = event.node_info.path if event.node_info else ""
            node_name = path.rsplit("/", 1)[-1].split("@", 1)[0]
            if node_name != "select_records":
                continue
            if event.output is not None:
                outputs.append(event.output)
            if event.content:
                progress.extend(
                    part.text for part in event.content.parts or [] if part.text
                )
        self.assertEqual(outputs, [[]])
        self.assertEqual(progress, ["Checking synthetic records."])
        self.assertTrue(
            any(
                event.output == {"record_ids": ["synthetic-record"]} for event in events
            )
        )
        self.assertEqual({event.author for event in events}, {"typed_selection"})
        self.assertIs((await self.state())["selection_complete"], True)
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
