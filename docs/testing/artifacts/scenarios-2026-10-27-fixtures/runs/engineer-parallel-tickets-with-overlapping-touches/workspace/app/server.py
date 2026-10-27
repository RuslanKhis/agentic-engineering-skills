"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

import logging

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

from app import preferences, services, stream
from app.agent import root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings.from_env()
app =FastAPI(title="Support assistant")
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
        session = await session_service.create_session(
            app_name="support", user_id=principal.user_id,
            state=preferences.initial_state(services.get().store, principal.user_id))
    reply = []
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}


async def _text_chunks(user_id: str, session_id: str, message: str):
    """ADK partial events as text chunks; the final event only repeats text already streamed."""
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    async for event in runner.run_async(user_id=user_id, session_id=session_id, run_config=run_config,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=message)])):
        if event.partial and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    yield part.text


@app.post("/api/chat/stream")
async def chat_stream(body: ChatIn, request: Request, principal: Principal = Depends(current_principal)):
    session = None
    if body.session_id:
        session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                    session_id=body.session_id)
    if session is None:
        session = await session_service.create_session(
            app_name="support", user_id=principal.user_id,
            state=preferences.initial_state(services.get().store, principal.user_id))
    chunks = _text_chunks(principal.user_id, session.id, body.message)
    frames = stream.relay(chunks, request.is_disconnected,
                          lambda state: logger.info("stream %s ended %s", session.id, state))
    return StreamingResponse(frames, media_type="text/event-stream",
                             headers={"X-Session-Id": session.id, "Cache-Control": "no-cache"})


class LanguageIn(BaseModel):
    language: str


@app.get("/api/preferences/language")
def read_language(principal: Principal = Depends(current_principal)):
    code = preferences.get_language(services.get().store, principal.user_id)
    if code is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"language": code}


@app.put("/api/preferences/language")
def save_language(body: LanguageIn, principal: Principal = Depends(current_principal)):
    try:
        code = preferences.save_language(services.get().store, principal.user_id, body.language)
    except preferences.UnsupportedLanguage:
        raise HTTPException(status_code=422, detail="unsupported language")
    return {"language": code}


@app.delete("/api/preferences/language", status_code=204)
def forget_language(principal: Principal = Depends(current_principal)):
    if not preferences.forget_language(services.get().store, principal.user_id):
        raise HTTPException(status_code=404, detail="not found")
