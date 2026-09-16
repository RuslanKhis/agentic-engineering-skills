"""OFFLINE ADK 2.8 contract probe; run in an isolated test process.

From this skill directory, using the target's existing environment:
  PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
    python -m pytest -q -p no:cacheprovider assets/test_adk_contract.py

Requires pytest, ADK 2.8.0, GenAI, google-auth and Pydantic already installed.
No application or companion imports, installations, credentials or cloud calls.
Real Agent/Workflow/Runner/Gemini/GenAI serialization is retained. HTTP responses,
metadata and execution results are synthetic. This is not a SQL-policy test,
model-quality evaluation, live connectivity check or latency benchmark.

The private SDK HTTP seam is deliberate: fail if it changes; do not replace the
serializer or Agent with a fake to obtain a passing compatibility result.

Adapted from Chapter 10's MIT-licensed author/workflow contract tests.
Copyright (c) 2026 RuslanKhis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import asyncio
import importlib.metadata
import json
import os
import socket
from types import SimpleNamespace
from typing import Literal

import pytest
from pydantic import BaseModel, ConfigDict, Field


PHYSICAL_TABLE = "offline-project.synthetic.approved_table"
MODEL = "gemini-3.5-flash"  # Request label only; no availability claim.
REQUIRED_KEYS = {"status", "explore_name", "tables", "sql", "parameters", "message"}


class Selection(BaseModel):
    route: Literal["FAST", "SLOW", "NO_QUERY"]
    table_names: list[str]


class Candidate(BaseModel):
    status: Literal["READY", "NEEDS_CLARIFICATION", "UNSUPPORTED"]
    explore_name: str | None = None
    tables: list[str]
    sql: str | None = None
    parameters: list[dict[str, str]]
    message: str = Field(min_length=1)


class WireCandidate(Candidate):
    model_config = ConfigDict(json_schema_extra={"required": sorted(REQUIRED_KEYS)})


@pytest.fixture
def offline_runtime(monkeypatch):
    """Install guards before Google imports/provider construction; restore on exit."""
    attempts = []

    def blocked(*args, **kwargs):
        attempts.append("blocked_external_operation")
        raise AssertionError("offline_guard_blocked_external_operation")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    for name in tuple(os.environ):
        if name.startswith(("GOOGLE_", "GEMINI_", "GCLOUD_", "OTEL_")):
            monkeypatch.delenv(name)
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    monkeypatch.setenv("OTEL_SDK_DISABLED", "true")
    monkeypatch.setenv("ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS", "false")

    assert importlib.metadata.version("google-adk") == "2.8.0", "probe_requires_adk_2_8_0"
    import google.auth
    import google.auth._default
    from google.auth.credentials import AnonymousCredentials

    monkeypatch.setattr(google.auth, "default", blocked)
    monkeypatch.setattr(google.auth._default, "default", blocked)
    monkeypatch.setattr(AnonymousCredentials, "refresh", blocked)

    from google.adk import Agent, Event as AdkEvent, Workflow
    from google.adk.agents.run_config import RunConfig
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import Client, types

    # ADK resolves function annotations against module globals.
    global Event
    Event = AdkEvent
    runtime = SimpleNamespace(
        Agent=Agent, Workflow=Workflow, RunConfig=RunConfig, Gemini=Gemini,
        Runner=Runner, Sessions=InMemorySessionService, Client=Client, types=types,
        AnonymousCredentials=AnonymousCredentials, auth=google.auth,
        attempts=attempts, deliberate_blocks=0,
    )
    yield runtime
    assert len(attempts) == runtime.deliberate_blocks, "unexpected_external_operation_attempt"


def ready_payload():
    return {
        "status": "READY", "explore_name": "synthetic", "tables": ["approved_table"],
        "sql": f"SELECT COUNT(*) AS case_count FROM `{PHYSICAL_TABLE}`",
        "parameters": [], "message": "Count synthetic cases.",
    }


def run_graph(runtime, monkeypatch, *, route="SLOW", payload=None,
              callback=True, metadata_failure=False):
    """Run genuine orchestration; all provider data and execution are synthetic."""
    payload = ready_payload() if payload is None else payload
    responses = [{"route": route, "table_names": ["approved_table"]}, payload]
    requests, candidates, final_messages = [], [], []
    calls = {"metadata": 0, "execution": 0}
    client = runtime.Client(
        enterprise=True, project="offline-project", location="global",
        credentials=runtime.AnonymousCredentials(),
    )
    assert callable(getattr(client._api_client, "async_request", None)), "sdk_http_seam_changed"

    async def http_response(http_method, path, request_dict, http_options=None):
        assert len(requests) < len(responses), "unexpected_provider_request"
        requests.append(request_dict)
        return runtime.types.HttpResponse(headers={}, body=json.dumps({
            "candidates": [{
                "content": {"role": "model", "parts": [{"text": json.dumps(responses[len(requests) - 1])}]},
                "finishReason": "STOP",
            }],
        }))

    monkeypatch.setattr(client._api_client, "async_request", http_response)

    def wire_schema(callback_context, llm_request):
        llm_request.set_output_schema(WireCandidate)

    router = runtime.Agent(
        name="probe_router", model=runtime.Gemini(model=MODEL, client=client),
        instruction="Select the synthetic probe route.", output_schema=Selection,
        mode="single_turn",
    )
    author = runtime.Agent(
        name="probe_author", model=runtime.Gemini(model=MODEL, client=client),
        instruction="Return a candidate using the supplied fully_qualified_name in the sql field.",
        output_schema=Candidate, before_model_callback=wire_schema if callback else None,
        mode="single_turn",
    )

    def dispatch(node_input: Selection) -> Event:
        assert isinstance(node_input, Selection), "router_handoff_not_typed"
        return Event(route=node_input.route, output=node_input)

    def collect(node_input: Selection) -> Event:
        calls["metadata"] += 1
        if metadata_failure:
            return Event(route="NO_QUERY", output={"status": "ERROR"})
        assert node_input.table_names == ["approved_table"], "unexpected_metadata_selection"
        return Event(route="READY", output={
            "status": "READY", "explore_name": "synthetic",
            "schema_tool_result": {"tables": {"approved_table": {
                "fully_qualified_name": PHYSICAL_TABLE,
                "columns": [{"name": "case_id", "type": "STRING"}],
                "description": "synthetic_metadata_sentinel",
            }}},
        })

    def fast(node_input: Selection) -> Event:
        calls["execution"] += 1
        return Event(output={"status": "OK", "rows": [{"case_count": 2}]})

    def refuse(node_input: Selection) -> Event:
        return Event(output={"status": "UNSUPPORTED"})

    def accept_candidate(node_input: Candidate) -> Event:
        assert isinstance(node_input, Candidate), "author_handoff_not_typed"
        candidates.append(node_input)
        if node_input.status != "READY":
            return Event(output={"status": node_input.status})
        if not node_input.sql or not node_input.explore_name:
            return Event(output={"status": "POLICY_REJECTED"})
        # A spy, NOT an SQL policy or a warehouse adapter. Never execute this SQL.
        calls["execution"] += 1
        return Event(output={"status": "OK", "rows": [{"case_count": 2}]})

    def format_result(node_input: dict) -> Event:
        return Event(message="PROBE_FINAL " + json.dumps(node_input, sort_keys=True))

    workflow = runtime.Workflow(name="offline_contract_probe", edges=[
        ("START", router, dispatch),
        (dispatch, {"FAST": fast, "SLOW": collect, "NO_QUERY": refuse}),
        (collect, {"READY": author, "NO_QUERY": format_result}),
        (author, accept_candidate, format_result),
        (fast, format_result), (refuse, format_result),
    ])

    async def consume():
        try:
            sessions = runtime.Sessions()
            await sessions.create_session(app_name="offline_contract_probe", user_id="synthetic", session_id="case")
            runner = runtime.Runner(agent=workflow, app_name="offline_contract_probe", session_service=sessions)
            async for event in runner.run_async(
                user_id="synthetic", session_id="case",
                new_message=runtime.types.Content(role="user", parts=[runtime.types.Part(text="Count synthetic cases.")]),
                run_config=runtime.RunConfig(max_llm_calls=4),
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts or []:
                        if part.text and part.text.startswith("PROBE_FINAL "):
                            final_messages.append(part.text)
        finally:
            await client.aio.aclose()

    try:
        asyncio.run(consume())
    finally:
        client.close()
    assert len(final_messages) == 1, "missing_or_duplicate_final_formatter_event"
    assert not runtime.attempts, "external_operation_was_attempted"
    return SimpleNamespace(
        requests=requests, candidates=candidates, calls=calls,
        final=json.loads(final_messages[0].removeprefix("PROBE_FINAL ")),
    )


def assert_author_wire(request):
    schema = request["generationConfig"]["responseSchema"]
    assert REQUIRED_KEYS <= set(schema.get("required", [])), "provider_required_keys_missing"
    assert schema["properties"]["sql"]["nullable"] is True, "sql_must_be_nullable"
    assert schema["properties"]["explore_name"]["nullable"] is True, "explore_must_be_nullable"
    assert request["generationConfig"]["responseMimeType"] == "application/json"


@pytest.mark.parametrize("route,failure,model_count,metadata_count,execution_count,status", [
    ("FAST", False, 1, 0, 1, "OK"),
    ("SLOW", False, 2, 1, 1, "OK"),
    ("NO_QUERY", False, 1, 0, 0, "UNSUPPORTED"),
    ("SLOW", True, 1, 1, 0, "ERROR"),
])
def test_public_workflow_branches_and_final_event(offline_runtime, monkeypatch, route, failure,
                                                model_count, metadata_count, execution_count, status):
    result = run_graph(offline_runtime, monkeypatch, route=route, metadata_failure=failure)
    assert len(result.requests) == model_count
    assert result.calls == {"metadata": metadata_count, "execution": execution_count}
    assert result.final["status"] == status
    if status == "OK":
        assert result.final["rows"] == [{"case_count": 2}]


def test_actual_wire_schema_and_exact_metadata_handoff(offline_runtime, monkeypatch):
    result = run_graph(offline_runtime, monkeypatch)
    assert_author_wire(result.requests[1])
    serialized_context = json.dumps(result.requests[1]["contents"])
    assert PHYSICAL_TABLE in serialized_context
    assert "synthetic_metadata_sentinel" in serialized_context
    assert result.candidates[0].sql == ready_payload()["sql"]


@pytest.mark.parametrize("status", ["NEEDS_CLARIFICATION", "UNSUPPORTED"])
def test_null_refusal_survives_runtime_validation(offline_runtime, monkeypatch, status):
    result = run_graph(offline_runtime, monkeypatch, payload={
        "status": status, "explore_name": None, "tables": [], "sql": None,
        "parameters": [], "message": "Synthetic refusal.",
    })
    assert_author_wire(result.requests[1])
    assert result.candidates[0].sql is None and result.candidates[0].explore_name is None
    assert result.calls["execution"] == 0
    assert result.final["status"] == status


def test_incomplete_ready_is_rejected_after_real_handoff(offline_runtime, monkeypatch):
    payload = ready_payload()
    payload.pop("sql")  # Intentionally emulate a provider violating the requested schema.
    result = run_graph(offline_runtime, monkeypatch, payload=payload)
    assert_author_wire(result.requests[1])
    assert result.calls["execution"] == 0
    assert result.final["status"] == "POLICY_REJECTED"


def test_negative_control_detects_removed_wire_callback(offline_runtime, monkeypatch):
    result = run_graph(offline_runtime, monkeypatch, callback=False)
    # A good scripted answer can still hide a defective outgoing provider contract.
    assert result.final["status"] == "OK"
    with pytest.raises(AssertionError, match="provider_required_keys_missing"):
        assert_author_wire(result.requests[1])


def test_guards_reject_adc_and_network_before_use(offline_runtime):
    offline_runtime.deliberate_blocks = 2
    with pytest.raises(AssertionError, match="offline_guard_blocked_external_operation"):
        offline_runtime.auth.default()
    with pytest.raises(AssertionError, match="offline_guard_blocked_external_operation"):
        socket.create_connection(("unused.invalid", 443))
