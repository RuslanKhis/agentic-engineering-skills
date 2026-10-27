"""Promptfoo Python provider: runs the ADK agent in process against the test fakes.

Needs a model key (GOOGLE_API_KEY), so it runs in the nightly job only. Payments and mail are the
fakes from tests/fakes.py; nothing here reaches a real provider. The customer is a fixture chosen
by the test (`vars.customer`), standing in for the verified principal.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Tool arguments are on ADK's spans only when content capture is on. Set before google.adk loads.
os.environ.setdefault("ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS", "true")
os.environ.setdefault("SUPPORT_DB_PATH", ":memory:")
OTLP_ENDPOINT = os.environ.get("PROMPTFOO_OTLP_ENDPOINT", "http://127.0.0.1:4318/v1/traces")

_provider_ready = False


def _setup_tracing():
    """Export ADK's native spans to Promptfoo's OTLP receiver; return the tracer."""
    global _provider_ready
    from opentelemetry import trace
    if not _provider_ready:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        provider = TracerProvider()
        provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT)))
        trace.set_tracer_provider(provider)
        _provider_ready = True
    return trace.get_tracer("support-assistant-evals"), trace.get_tracer_provider()


async def _run(prompt: str, customer: str) -> dict:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    from app.agent import build_agent
    from tests.fakes import configure_fakes

    agent = build_agent()
    # build_agent wires the real clients; swap in the fakes before the first tool call.
    _store, pay, mail = configure_fakes()
    sessions = InMemorySessionService()
    runner = Runner(app_name="support-eval", agent=agent, session_service=sessions)
    session = await sessions.create_session(app_name="support-eval", user_id=customer)
    calls, text = [], []
    async for event in runner.run_async(
        user_id=customer, session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
    ):
        calls.extend({"name": c.name, "args": dict(c.args or {})} for c in event.get_function_calls())
        if event.is_final_response() and event.content and event.content.parts:
            text.extend(p.text for p in event.content.parts if p.text)
    return {
        "reply": "".join(text),
        "tool_calls": calls,
        "payments_requests": len(pay.requests),
        "mail_requests": len(mail.requests),
        "model": agent.model if isinstance(agent.model, str) else str(agent.model),
    }


def call_api(prompt, options, context):
    from opentelemetry import trace
    from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

    tracer, tracer_provider = _setup_tracing()
    customer = (context.get("vars") or {}).get("customer", "cust-ana")
    parent = TraceContextTextMapPropagator().extract({"traceparent": context.get("traceparent", "")})
    try:
        with tracer.start_as_current_span("support-assistant-provider", context=parent):
            payload = asyncio.run(_run(prompt, customer))
    finally:
        tracer_provider.force_flush()
    return {"output": json.dumps(payload)}
