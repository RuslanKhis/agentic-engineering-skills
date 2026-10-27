"""FastAPI service: one app serves /api (Runner in process) and the built SPA."""
from __future__ import annotations

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.auth.transport import requests as google_requests
from google.genai import types
from google.oauth2 import id_token
from pydantic import BaseModel

from app.agent import root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.settings import Settings

settings = Settings.from_env()
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


api = APIRouter(prefix="/api", dependencies=[Depends(current_principal)])


class ChatIn(BaseModel):
    session_id: str | None = None
    message: str


@api.post("/chat")
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


@api.api_route("/{rest:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], include_in_schema=False)
async def api_not_found(rest: str):
    raise HTTPException(status_code=404, detail="not found")


app = FastAPI(title="Support assistant", docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(api)
app.frontend("/", directory="web/dist")
