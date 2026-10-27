"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

from app.agent import root_agent
from app import services
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.preferences import Preferences, UnsupportedLanguage
from app.settings import Settings

settings = Settings.from_env()
app = FastAPI(title="Support assistant")
session_service = InMemorySessionService()
runner = Runner(app_name="support", agent=root_agent, session_service=session_service)
preferences = Preferences(services.get().store)


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
        state: dict = {}
        preferences.load_into_state(principal.user_id, state)
        session = await session_service.create_session(app_name="support", user_id=principal.user_id,
                                                       state=state)
    reply = []
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}


class LanguageIn(BaseModel):
    language: str


@app.get("/api/preferences/language")
def get_language(principal: Principal = Depends(current_principal)):
    language = preferences.get(principal.user_id)
    if language is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"language": language}


@app.put("/api/preferences/language", status_code=204)
def put_language(body: LanguageIn, principal: Principal = Depends(current_principal)):
    try:
        preferences.save(principal.user_id, body.language)
    except UnsupportedLanguage:
        raise HTTPException(status_code=422, detail="unsupported language")


@app.delete("/api/preferences/language", status_code=204)
async def forget_language(session_id: str | None = None, principal: Principal = Depends(current_principal)):
    state = None
    if session_id:
        session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                    session_id=session_id)
        state = session.state if session else None
    if not preferences.forget(principal.user_id, state):
        raise HTTPException(status_code=404, detail="not found")
