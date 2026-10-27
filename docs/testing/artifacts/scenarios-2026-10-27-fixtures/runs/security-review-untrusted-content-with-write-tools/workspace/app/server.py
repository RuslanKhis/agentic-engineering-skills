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


class Confirmation(BaseModel):
    function_call_id: str
    confirmed: bool


class ChatIn(BaseModel):
    session_id: str | None = None
    message: str = ""
    confirmation: Confirmation | None = None  # the customer's answer to a pending refund


@app.post("/api/chat")
async def chat(body: ChatIn, principal: Principal = Depends(current_principal)):
    session = None
    if body.session_id:
        session = await session_service.get_session(app_name="support", user_id=principal.user_id,
                                                    session_id=body.session_id)
    if session is None:
        # The email comes from the verified assertion and lives in state the model cannot write to
        # through a tool argument; send_email and fetch_email compare against it.
        session = await session_service.create_session(
            app_name="support", user_id=principal.user_id, state={"principal_email": principal.email})
    if body.confirmation is not None:
        # Only this authenticated endpoint builds the confirmation, never the model or a tool result.
        part = types.Part(function_response=types.FunctionResponse(
            id=body.confirmation.function_call_id, name="adk_request_confirmation",
            response={"confirmed": body.confirmation.confirmed}))
    else:
        part = types.Part(text=body.message)
    reply = []
    pending = []
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user", parts=[part])):
        for call in event.get_function_calls():
            if call.name == "adk_request_confirmation":
                original = (call.args or {}).get("originalFunctionCall", {})
                pending.append({"function_call_id": call.id, "tool": original.get("name"),
                                "args": original.get("args")})
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply), "pending_confirmations": pending}
