"""FastAPI service for the refund desk. A manager approves a pending refund from the back office."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from pydantic import BaseModel

from app import refund_ops
from app.agent import RUN_CONFIG, app as adk_app
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.clients.restate import ReviewEngineError
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


class DecisionIn(BaseModel):
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


@api.post("/backoffice/refunds/{op_id}/decision")
async def decide(op_id: str, body: DecisionIn, principal: Principal = Depends(current_principal)):
    """A manager decides a pending refund. The ADK session is not involved: the decision is stored
    on the operation and the Restate workflow that waits on it carries on, so it does not matter
    which pod, or whether any pod, handled the customer's chat."""
    try:
        return refund_ops.review(op_id, body.approved, principal.user_id, principal.email)
    except refund_ops.ReviewRefused as refused:
        raise HTTPException(status_code={"not_found": 404}.get(refused.code, 403), detail=refused.code)
    except ReviewEngineError:
        # The decision is stored; repeating the request wakes the workflow again.
        raise HTTPException(status_code=503, detail="decision saved; review engine unavailable, repeat the request")


@api.get("/api/refunds/{op_id}")
async def refund_status(op_id: str, principal: Principal = Depends(current_principal)):
    found = refund_ops.status(op_id, principal.user_id, principal.email)
    if found is None:
        raise HTTPException(status_code=404, detail="not_found")
    return found
