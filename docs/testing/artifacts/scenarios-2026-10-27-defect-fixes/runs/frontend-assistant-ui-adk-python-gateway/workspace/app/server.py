"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

import asyncio
import json
import logging

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

from app import gateway
from app.agent import root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings.from_env()
app = FastAPI(title="Support assistant")
session_service = InMemorySessionService()
runner = Runner(app_name="support", agent=root_agent, session_service=session_service)


def _verify(assertion: str, audience: str):
    return id_token.verify_token(assertion, google_requests.Request(), audience=audience,
                                 certs_url="https://www.gstatic.com/iap/verify/public_key")


def current_principal(request: Request) -> Principal:
    try:
        return principal_from_headers(request.headers, _verify, settings.iap_audience)
    except Unauthenticated:
        raise HTTPException(status_code=401, detail="unauthenticated")


class ChatIn(BaseModel):
    session_id: str | None = None
    message: str


@app.post("/api/chat")
async def chat(body: ChatIn, principal: Principal = Depends(current_principal)):
    session = None
    if body.session_id:
        session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                    session_id=body.session_id)
    if session is None:
        session = await session_service.create_session(app_name="support", user_id=principal.user_id)
    reply = []
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}


# ---- assistant-ui gateway: /api/adk/* (rules live in app/gateway.py) ----

RUN_DEADLINE_SECONDS = 120
_session_locks: dict[str, asyncio.Lock] = {}  # one process; see the README before scaling out


def _public_error(exc: gateway.BadRequest) -> HTTPException:
    return HTTPException(status_code=exc.status, detail=exc.code)


async def _owned_session(principal: Principal, session_id: str):
    session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                session_id=session_id)
    if session is None:  # unknown and foreign sessions look the same
        raise HTTPException(status_code=404, detail="session_not_found")
    return session


@app.post("/api/adk/sessions")
async def create_adk_session(principal: Principal = Depends(current_principal)):
    session = await session_service.create_session(app_name="support", user_id=principal.user_id)
    return {"sessionId": session.id}


def _sse(payload: dict) -> bytes:
    return b"data: " + json.dumps(payload, separators=(",", ":")).encode() + b"\n\n"


@app.post("/api/adk/run")
async def adk_run(request: Request, principal: Principal = Depends(current_principal)):
    raw = await request.body()
    if len(raw) > 64_000:
        raise HTTPException(status_code=413, detail="request_too_large")
    try:
        turn = gateway.parse_request(json.loads(raw))
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="invalid_request")
    except gateway.BadRequest as exc:
        raise _public_error(exc)

    session = await _owned_session(principal, turn.session_id)  # before any agent or rewind call
    steps = gateway.summarize(session.events)
    rewind_to = None
    text = turn.text
    try:
        if turn.approvals:
            gateway.check_approvals(steps, turn.approvals)
        elif turn.checkpoint is not None:
            plan = gateway.plan_edit(steps, turn.checkpoint)
            rewind_to = plan.before_invocation_id
            text = text or plan.user_text  # a regenerate arrives with no text
            if not text:
                raise gateway.BadRequest(422, "empty_message")
    except gateway.BadRequest as exc:
        raise _public_error(exc)

    # google-adk 2.12.0 refuses function responses and text in one message: answers first, text after.
    messages = [types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id=a.call_id, name=gateway.CONFIRMATION_CALL, response={"confirmed": a.confirmed}))])
        for a in turn.approvals]
    if text:
        messages.append(types.Content(role="user", parts=[types.Part(text=text)]))

    async def stream():
        lock = _session_locks.setdefault(f"{principal.user_id}/{turn.session_id}", asyncio.Lock())
        try:
            async with asyncio.timeout(RUN_DEADLINE_SECONDS):  # lock wait counts against the deadline
                async with lock:
                    if rewind_to:
                        await runner.rewind_async(user_id=principal.user_id, session_id=turn.session_id,
                                                  rewind_before_invocation_id=rewind_to)
                    for message in messages:
                        events = runner.run_async(user_id=principal.user_id, session_id=turn.session_id,
                                                  new_message=message)
                        try:
                            async for event in events:
                                public = gateway.public_event(
                                    event.model_dump(mode="json", by_alias=True, exclude_none=True),
                                    root_agent.name)
                                if public:
                                    yield _sse(public)
                        finally:
                            await events.aclose()
        except Exception:  # includes the deadline; the client gets fixed copy, the log keeps the cause
            logger.exception("adk run failed")
            yield _sse(gateway.FIXED_ERROR)

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})
