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
from app import preferences, profile_api, services
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

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


app.include_router(profile_api.router)
app.dependency_overrides[profile_api._principal] = current_principal


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
            state=preferences.initial_session_state(services.get().store, principal))
    reply = []
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}
