"""FastAPI service for the refund desk. A manager approves a pending refund from the back office."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from pydantic import BaseModel

from app.agent import RUN_CONFIG, app as adk_app
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

settings = Settings.from_env()
api = FastAPI(title="Refund desk")
sessions = DatabaseSessionService(db_url=settings.db_url)
runner = Runner(app=adk_app, session_service=sessions)


def current_principal(request: Request) -> Principal:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests

    def verify(assertion, audience):
        return id_token.verify_token(assertion, google_requests.Request(), audience=audience,
                                     certs_url="https://www.gstatic.com/iap/verify/public_key")
    try:
        return principal_from_headers(request.headers, verify, settings.iap_audience)
    except Unauthenticated:
        raise HTTPException(status_code=401, detail="unauthenticated")


class ChatIn(BaseModel):
    session_id: str
    message: str


class ApprovalIn(BaseModel):
    session_id: str
    user_id: str
    function_call_id: str
    approved: bool


async def _run(user_id: str, session_id: str, message: types.Content) -> list[dict]:
    out = []
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message,
                                        run_config=RUN_CONFIG):
        if event.content and event.content.parts:
            out.extend({"author": event.author, "text": p.text} for p in event.content.parts if p.text)
    return out


@api.post("/api/chat")
async def chat(body: ChatIn, principal: Principal = Depends(current_principal)):
    msg = types.Content(role="user", parts=[types.Part(text=body.message)])
    return {"events": await _run(principal.user_id, body.session_id, msg)}


@api.post("/backoffice/approvals")
async def approve(body: ApprovalIn, principal: Principal = Depends(current_principal)):
    """A manager answers the pending confirmation; the flow resumes from where it paused."""
    reply = types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id=body.function_call_id, name="adk_request_confirmation", response={"confirmed": body.approved}))])
    return {"events": await _run(body.user_id, body.session_id, reply)}
