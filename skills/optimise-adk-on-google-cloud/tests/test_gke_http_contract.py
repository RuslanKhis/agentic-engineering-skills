"""Real ADK HTTP/session/SSE orchestration with a deterministic model boundary.

This portable test owns its temporary agent directory and in-memory sessions.
It checks serialized events, not network timing, proxy/browser delivery, cloud
storage or caller authentication. No companion source is imported.
"""

import importlib.metadata
import json
import os
import tempfile
import unittest
from contextlib import asynccontextmanager
from unittest.mock import patch


APP_NAME = "synthetic_http_app"
ANSWER_AUTHOR = "synthetic_answer_agent"
SESSION_ROOT = f"/apps/{APP_NAME}/users/synthetic-owner/sessions"


class GkeHttpContract(unittest.TestCase):
    def setUp(self):
        try:
            version = importlib.metadata.version("google-adk")
        except importlib.metadata.PackageNotFoundError:
            self.skipTest("ADK is absent; preserve target dependencies")
        if version != "2.8.0":
            self.skipTest("This recorded HTTP contract requires ADK 2.8.0; preserve target pins")

        guard = patch.dict(os.environ, {"OTEL_SDK_DISABLED": "true"}, clear=True)
        guard.start()
        self.addCleanup(guard.stop)
        for target in (
            "socket.socket.connect", "socket.socket.connect_ex",
            "socket.create_connection", "socket.getaddrinfo", "google.auth.default",
        ):
            guard = patch(target, side_effect=AssertionError("External access is prohibited"))
            guard.start()
            self.addCleanup(guard.stop)

        from fastapi.testclient import TestClient
        from google.adk import Agent
        from google.adk.apps import App
        from google.adk.cli.fast_api import get_fast_api_app
        from google.adk.cli.utils.base_agent_loader import BaseAgentLoader
        from google.adk.models import BaseLlm
        from google.adk.models.llm_response import LlmResponse
        from google.genai import types
        from pydantic import Field

        class DeterministicModel(BaseLlm):
            model: str = "offline-http-contract"
            streams: list[bool] = Field(default_factory=list)
            fail_after_partial: bool = False

            async def generate_content_async(self, llm_request, stream=False):
                self.streams.append(stream)
                results = [
                    part.function_response
                    for content in llm_request.contents
                    for part in content.parts or []
                    if part.function_response
                ]
                if not results:
                    yield LlmResponse(content=types.Content(role="model", parts=[
                        types.Part(function_call=types.FunctionCall(
                            id="synthetic-route-call", name="route_ticket", args={}
                        ))
                    ]))
                    return
                if stream:
                    for text in ("The ticket ", "belongs to billing."):
                        yield LlmResponse(
                            content=types.Content(role="model", parts=[types.Part(text=text)]),
                            partial=True,
                        )
                    if self.fail_after_partial:
                        raise RuntimeError("synthetic model failure")
                yield LlmResponse(
                    content=types.Content(role="model", parts=[
                        types.Part(text="The ticket belongs to billing.")
                    ]),
                    finish_reason=types.FinishReason.STOP,
                )

        def route_ticket() -> dict:
            """Return the synthetic routing result."""
            return {"status": "success", "queue": "billing"}

        self.model = DeterministicModel()
        agentic_app = App(name=APP_NAME, root_agent=Agent(
            name=ANSWER_AUTHOR, model=self.model, tools=[route_ticket]
        ))

        class SyntheticLoader(BaseAgentLoader):
            def load_agent(self, agent_name):
                if agent_name != APP_NAME:
                    raise ValueError("Unknown synthetic application")
                return agentic_app

            def list_agents(self):
                return [APP_NAME]

        directory = tempfile.TemporaryDirectory(prefix="adk-http-contract-")
        self.addCleanup(directory.cleanup)
        def make_app(lifespan=None):
            return get_fast_api_app(
                agents_dir=directory.name,
                agent_loader=SyntheticLoader(),
                session_service_uri="memory://",
                use_local_storage=False,
                web=False,
                reload_agents=False,
                trace_to_cloud=False,
                otel_to_cloud=False,
                lifespan=lifespan,
            )

        self.make_app = make_app
        self.http = self.enterContext(TestClient(make_app()))

    def create(self, session_id="s-contract"):
        path = f"{SESSION_ROOT}/{session_id}"
        response = self.http.post(path, json={"synthetic_state": "retained"})
        self.assertEqual(response.status_code, 200, response.text)
        return path

    def run_request(self, session_id="s-contract"):
        return {
            "appName": APP_NAME, "userId": "synthetic-owner", "sessionId": session_id,
            "newMessage": {"role": "user", "parts": [{"text": "Route this synthetic ticket."}]},
        }

    def decode_sse(self, response):
        self.assertEqual(response.status_code, 200, response.text)
        self.assertTrue(response.headers["content-type"].startswith("text/event-stream"))
        # Parse the full SDK response only. TestClient can buffer delivery; these
        # frames establish serialization and stream selection, not real TTFT.
        frames = response.text.replace("\r\n", "\n").split("\n\n")
        payloads = ["\n".join(
            line[5:].removeprefix(" ") for line in frame.splitlines()
            if line.startswith("data:")
        ) for frame in frames]
        return [json.loads(payload) for payload in payloads if payload]

    def test_session_creation_routes_have_different_state_body_contracts(self):
        explicit = self.create()
        response = self.http.post(SESSION_ROOT, json={
            "sessionId": "s-collection", "state": {"synthetic_state": "collection"},
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.http.get(explicit).json()["state"], {"synthetic_state": "retained"})
        self.assertEqual(response.json()["state"], {"synthetic_state": "collection"})
        self.assertEqual(self.http.get(explicit.replace("synthetic-owner", "another-user")).status_code, 404)
        # Route-key separation has no trusted caller here. Supplying the original
        # owner key still succeeds, so this is not an authorization test.
        self.assertEqual(self.http.get(explicit).status_code, 200)
        for path in (explicit, f"{SESSION_ROOT}/s-collection"):
            self.assertEqual(self.http.delete(path).status_code, 200)
            self.assertEqual(self.http.get(path).status_code, 404)

    def test_run_uses_real_tool_and_persists_events_under_app_not_answer_author(self):
        path = self.create()
        response = self.http.post("/run", json=self.run_request())
        self.assertEqual(response.status_code, 200, response.text)
        events = response.json()
        parts = [part for event in events for part in (event.get("content") or {}).get("parts", [])]
        call = next(part["functionCall"] for part in parts if "functionCall" in part)
        result = next(part["functionResponse"] for part in parts if "functionResponse" in part)
        self.assertEqual(result["id"], call["id"])
        self.assertEqual(result["response"], {"status": "success", "queue": "billing"})
        self.assertEqual(events[-1]["author"], ANSWER_AUTHOR)
        self.assertEqual(events[-1]["finishReason"], "STOP")
        self.assertEqual(self.model.streams, [False, False])
        stored = self.http.get(path).json()
        self.assertEqual(stored["appName"], APP_NAME)
        self.assertTrue({event["id"] for event in events}.issubset(
            {event["id"] for event in stored["events"]}
        ))
        self.assertEqual(self.http.post("/run", json={}).status_code, 422)

    def test_sse_route_requires_streaming_flag_for_partial_model_delivery(self):
        for flag in (None, False, True):
            with self.subTest(streaming=flag):
                session_id = f"s-stream-{flag}"
                self.create(session_id)
                request = self.run_request(session_id)
                if flag is not None:
                    request["streaming"] = flag
                before = len(self.model.streams)
                events = self.decode_sse(self.http.post("/run_sse", json=request))
                self.assertEqual(self.model.streams[before:], [bool(flag), bool(flag)])
                partials = [event for event in events if event.get("partial")]
                self.assertEqual(len(partials), 2 if flag else 0)
                self.assertEqual(events[-1]["finishReason"], "STOP")
                self.assertEqual(events[-1]["author"], ANSWER_AUTHOR)
                self.assertFalse(any("error" in event for event in events))

    def test_late_model_failure_is_an_error_frame_after_http_200_and_partials(self):
        self.create()
        self.model.fail_after_partial = True
        events = self.decode_sse(self.http.post("/run_sse", json={
            **self.run_request(), "streaming": True,
        }))
        self.assertEqual(len([event for event in events if event.get("partial")]), 2)
        self.assertIn("synthetic model failure", events[-1]["error"])
        self.assertFalse(any(event.get("finishReason") == "STOP" for event in events))

    def test_supplied_lifespan_exits_before_framework_closes_cached_runner(self):
        from fastapi.testclient import TestClient
        from google.adk import Runner

        order = []

        @asynccontextmanager
        async def custom_lifespan(app):
            order.append("custom-start")
            try:
                yield
            finally:
                order.append("custom-stop")

        original_close = Runner.close

        async def observed_close(runner, *args, **kwargs):
            order.append("runner-close")
            return await original_close(runner, *args, **kwargs)

        # Observe, then execute, the real Runner closure. The injected lifespan
        # must not dispose a service still needed by this later framework step.
        with patch.object(Runner, "close", observed_close):
            with TestClient(self.make_app(lifespan=custom_lifespan)) as http:
                response = http.post(f"{SESSION_ROOT}/s-lifecycle", json={})
                self.assertEqual(response.status_code, 200, response.text)
                response = http.post("/run", json=self.run_request("s-lifecycle"))
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(order, ["custom-start"])
            self.assertEqual(order, ["custom-start", "custom-stop", "runner-close"])


if __name__ == "__main__":
    unittest.main()
