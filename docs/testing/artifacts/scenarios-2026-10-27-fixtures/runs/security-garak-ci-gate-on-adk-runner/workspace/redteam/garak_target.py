"""garak target: one probe prompt in, one fresh single-turn ADK Runner session out.

Run with the repository root on PYTHONPATH:
    garak --target_type function --target_name redteam.garak_target#run_agent --spec probes.<module> ...

garak's detectors read reply text only, so every attempt also appends one record of the effects that
actually reached the fake providers to the file named by REDTEAM_SIDECAR. redteam/check_garak.py
reads that file. Providers are always the fakes from tests/fakes.py; only the model is live.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os

from redteam.effects import findings_from_effects

USER_ID = "cust-ana"  # synthetic principal from tests/fakes.py


async def run_attempt(prompt: str, model=None) -> tuple[str, dict]:
    """Run one user turn; return (reply text, sidecar record). `model` replaces the agent's model in tests."""
    os.environ.setdefault("SUPPORT_DB_PATH", ":memory:")
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    from app.agent import build_agent
    from tests.fakes import configure_fakes

    _store, pay, mail = configure_fakes()
    agent = build_agent(configure_services=False)
    if model is not None:
        agent.model = model
    runner = InMemoryRunner(agent=agent, app_name="redteam")
    session = await runner.session_service.create_session(app_name="redteam", user_id=USER_ID, state={})
    calls, reply = [], []
    async for event in runner.run_async(
            user_id=USER_ID, session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)])):
        calls += [c.name for c in event.get_function_calls()]
        if event.content and event.content.role == "model":
            reply += [p.text for p in event.content.parts if getattr(p, "text", None)]
    record = {
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "tool_calls_attempted": calls,
        "payments_requests": len(pay.requests),
        "mail_requests": len(mail.requests),
        "findings": findings_from_effects(pay.requests, mail.requests),
    }
    return " ".join(reply), record


def run_agent(prompt: str) -> list[str]:
    """garak entry point. Returns a list with one string; a bare string would be iterated per character."""
    reply, record = asyncio.run(run_attempt(prompt))
    path = os.environ.get("REDTEAM_SIDECAR")
    if not path:
        raise RuntimeError("REDTEAM_SIDECAR must name the sidecar file; refusing to run without it")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")
    return [reply]
