"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

from app.a2a_card import fetch_verified_card
from app.agent import build_agent, root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

log = logging.getLogger(__name__)
settings = Settings.from_env()
session_service = InMemorySessionService()
runner = Runner(app_name="support", agent=root_agent, session_service=session_service)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Fetch the partner card and attach the partner agent only if its signature verifies."""
    global runner
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            card = await fetch_verified_card(settings.partner_card_url, settings.partner_jwks_url,
                                             settings.partner_kids, client)
        runner = Runner(app_name="support", agent=build_agent(settings, warranty_card=card),
                        session_service=session_service)
    except Exception:  # CardRefused, network, parse: stay up without the partner
        log.exception("partner agent card refused; running without warranty_partner")
    yield


app = FastAPI(title="Support assistant", lifespan=lifespan)


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
