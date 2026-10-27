"""FastAPI service: chat runs the agent in process; saved answers live beside the sessions."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.auth.transport import requests as google_requests
from google.genai import types
from google.oauth2 import id_token
from pydantic import BaseModel

from app import saved_answers
from app.agent import root_agent
from app.auth import Principal, Unauthenticated, principal_from_headers
from app.db import make_engine
from app.settings import Settings

settings = Settings.from_env()
app = FastAPI(title="Support assistant")
# ADK creates its session tables in this database on first use.
session_service = DatabaseSessionService(db_url=settings.database_url)
engine = make_engine(settings.database_url)
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
    async for event in runner.run_async(user_id=principal.user_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}


class SaveIn(BaseModel):
    question: str
    answer: str


@app.post("/api/saved-answers", status_code=201)
def save_answer(body: SaveIn, principal: Principal = Depends(current_principal)):
    answer_id = saved_answers.save(engine, principal.user_id, body.question, body.answer)
    return {"id": answer_id}


@app.get("/api/saved-answers")
def list_answers(principal: Principal = Depends(current_principal)):
    return {"items": saved_answers.list_for(engine, principal.user_id)}


@app.get("/api/saved-answers/{answer_id}")
def get_answer(answer_id: int, principal: Principal = Depends(current_principal)):
    record = saved_answers.get(engine, answer_id)
    if record is None:
        raise HTTPException(status_code=404, detail="saved answer not found")
    return record
