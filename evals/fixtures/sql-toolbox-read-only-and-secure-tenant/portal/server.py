"""Customer portal chat endpoint."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from analytics.portal_agent import portal_agent
from portal.identity import claims_from_iap_header, customer_id_for

DIRECTORY = json.loads((Path(__file__).with_name("directory.json")).read_text())

app = FastAPI(title="Fernhill customer portal")
sessions = InMemorySessionService()
runner = Runner(app_name="portal", agent=portal_agent, session_service=sessions)


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None


@app.post("/api/chat")
async def chat(body: ChatIn, request: Request):
    claims = claims_from_iap_header(dict(request.headers))
    customer_id = customer_id_for(claims, DIRECTORY)
    if not customer_id:
        raise HTTPException(status_code=403, detail="no customer account")
    session = await sessions.create_session(app_name="portal", user_id=claims["email"],
                                            state={"customer_id": customer_id})
    reply = []
    async for event in runner.run_async(user_id=claims["email"], session_id=session.id,
                                        new_message=types.Content(role="user", parts=[types.Part(text=body.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"reply": "".join(reply)}
