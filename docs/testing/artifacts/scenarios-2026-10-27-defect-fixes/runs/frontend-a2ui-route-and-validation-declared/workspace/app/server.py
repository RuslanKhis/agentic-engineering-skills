"""FastAPI service: the chat endpoint runs the agent in process."""
from __future__ import annotations

import logging

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
from app.tools.a2ui import A2uiValidationError, for_tool_result

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
    widgets: dict[str, list[dict]] = {}  # one entry per surface; the last result of a turn wins
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
        # The only place A2UI is produced: converters run on tool results, never on model text.
        for response in event.get_function_responses():
            try:
                messages = for_tool_result(response.name, response.response or {})
            except A2uiValidationError:
                logger.exception("a2ui widget for %s refused", response.name)
                continue
            if messages:
                widgets[messages[0]["createSurface"]["surfaceId"]] = messages
    a2ui = [m for messages in widgets.values() for m in messages]
    return {"session_id": session.id, "reply": "".join(reply), "a2ui": a2ui}
