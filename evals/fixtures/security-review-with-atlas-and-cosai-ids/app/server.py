"""FastAPI chat endpoint; the Runner runs in process."""
from __future__ import annotations

from fastapi import FastAPI, Request
from google.adk.agents.run_config import RunConfig
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import root_agent

app = FastAPI()
runner = InMemoryRunner(agent=root_agent, app_name="ops")


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_id = request.headers["x-goog-authenticated-user-email"].split(":")[-1]
    session_id = body.get("session_id")
    if not session_id:
        session_id = (await runner.session_service.create_session(app_name="ops", user_id=user_id)).id
    reply = []
    async for event in runner.run_async(user_id=user_id, session_id=session_id, run_config=RunConfig(),
                                        new_message=types.Content(role="user", parts=[types.Part(text=body["message"])])):
        if event.is_final_response() and event.content:
            reply += [p.text for p in event.content.parts if p.text]
    return {"session_id": session_id, "reply": "".join(reply)}
