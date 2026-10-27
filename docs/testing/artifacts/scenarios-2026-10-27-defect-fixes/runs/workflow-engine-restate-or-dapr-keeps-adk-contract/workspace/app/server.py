"""FastAPI service for the refund desk. A manager approves a pending refund from the back office."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from pydantic import BaseModel

from app import services
from app.agent import RUN_CONFIG, app as adk_app
from app.approvals import OperationClosed, UnknownOperation
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.dapr_runtime import DaprApprovalGateway
from app.settings import Settings

settings = Settings.from_env()
gateway = DaprApprovalGateway()
services.get().approvals = gateway  # build_app() configured the rest at import


@asynccontextmanager
async def lifespan(_api: FastAPI):
    gateway.start()  # workflow worker: connects to the Dapr sidecar and takes work from any instance
    try:
        yield
    finally:
        gateway.stop()


api = FastAPI(title="Refund desk", lifespan=lifespan)
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
    operation_id: str
    approved: bool
    digest: str  # from GET /backoffice/approvals/{operation_id}: what the manager was shown


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


def require_approver(principal: Principal = Depends(current_principal)) -> Principal:
    if principal.email.lower() not in settings.approver_emails:
        raise HTTPException(status_code=403, detail="not a refund approver")
    return principal


@api.get("/backoffice/approvals/{operation_id}")
def approval_status(operation_id: str, principal: Principal = Depends(require_approver)):
    info = gateway.status(operation_id)
    if info is None:
        raise HTTPException(status_code=404, detail="unknown operation")
    return info


@api.post("/backoffice/approvals")
def approve(body: ApprovalIn, principal: Principal = Depends(require_approver)):
    """A manager decides a pending refund. The reviewer is the verified principal, never the body.
    The decision goes to the durable workflow, so it works on any pod and days after the request."""
    try:
        gateway.decide(body.operation_id, principal.user_id, body.approved, body.digest)
    except UnknownOperation:
        raise HTTPException(status_code=404, detail="unknown operation")
    except OperationClosed:
        raise HTTPException(status_code=409, detail="already decided or expired")
    return {"operation_id": body.operation_id, "accepted": True}
