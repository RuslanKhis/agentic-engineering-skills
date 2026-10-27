"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

import time

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel

from app.agent import app as adk_app
from app.approval_policy import resolve_pending
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

settings = Settings.from_env()
api = FastAPI(title="Support assistant")
session_service = DatabaseSessionService(db_url=f"sqlite:///{settings.db_path}")
runner = Runner(app=adk_app, session_service=session_service)

CONFIRMATION_CALL = "adk_request_confirmation"
REASK_REPLY = "I'm still waiting on your confirmation of the refund. Please reply \"yes\" to go ahead or \"cancel\" to drop it."


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


def pending_confirmation(session) -> tuple[str, float] | None:
    """(function-call id, request time) of a confirmation request the customer has not answered yet."""
    answered = set()
    pending = None
    for event in session.events:
        for call in event.get_function_calls():
            if call.name == CONFIRMATION_CALL:
                pending = (call.id, event.timestamp)
        for response in event.get_function_responses():
            if response.name == CONFIRMATION_CALL:
                answered.add(response.id)
    return pending if pending and pending[0] not in answered else None


def confirmation_answer(call_id: str, confirmed: bool) -> types.Content:
    return types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id=call_id, name=CONFIRMATION_CALL, response={"confirmed": confirmed}))])


async def _run(user_id: str, session_id: str, message: types.Content) -> str:
    reply = []
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return "".join(reply)


@api.post("/api/chat")
async def chat(body: ChatIn, principal: Principal = Depends(current_principal)):
    session = None
    if body.session_id:
        session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                    session_id=body.session_id)
    if session is None:
        session = await session_service.create_session(app_name="support", user_id=principal.user_id)
    message = types.Content(role="user", parts=[types.Part(text=body.message)])
    pending = pending_confirmation(session)
    if pending:
        call_id, requested_at = pending
        action = resolve_pending(body.message, requested_at, time.time())
        if action == "ask_again":
            # No model call and no tool dispatch: the request stays pending until answered or expired.
            return {"session_id": session.id, "reply": REASK_REPLY}
        if action == "approve":
            message = confirmation_answer(call_id, True)
        else:
            # "decline" or "expired": resume with a decline so the tool never runs.
            declined = await _run(principal.user_id, session.id, confirmation_answer(call_id, False))
            if action == "decline":
                return {"session_id": session.id, "reply": declined}
            # expired: the message is a new request, not an answer.
    return {"session_id": session.id, "reply": await _run(principal.user_id, session.id, message)}
