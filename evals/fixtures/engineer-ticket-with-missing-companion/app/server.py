"""FastAPI app: /api/chat streams the agent's reply as SSE; the SPA is served from web/dist."""
from __future__ import annotations

import json

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from app.agent import root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers

app = FastAPI(title="Doc assistant")
sessions = InMemorySessionService()
runner = Runner(app_name="docs", agent=root_agent, session_service=sessions)


def current_principal(request: Request) -> Principal:
    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token

    def verify(assertion, audience):
        return id_token.verify_token(assertion, google_requests.Request(), audience=audience,
                                     certs_url="https://www.gstatic.com/iap/verify/public_key")
    try:
        return principal_from_headers(request.headers, verify, request.app.state.iap_audience)
    except Unauthenticated:
        raise HTTPException(401, "unauthenticated")


class ChatIn(BaseModel):
    session_id: str
    message: str


@app.post("/api/chat")
async def chat(body: ChatIn, principal: Principal = Depends(current_principal)):
    session = await sessions.get_session(app_name="docs", user_id=principal.user_id, session_id=body.session_id)
    if session is None:
        raise HTTPException(404, "not found")

    async def events():
        try:
            async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                                new_message=types.Content(role="user", parts=[types.Part(text=body.message)])):
                for part in (event.content.parts if event.content else []):
                    if part.text:
                        yield f"event: text\ndata: {json.dumps({'text': part.text})}\n\n"
            yield "event: completed\ndata: {}\n\n"
        except Exception:
            yield "event: failed\ndata: {\"message\": \"The assistant could not finish this reply.\"}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")
