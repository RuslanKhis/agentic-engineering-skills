"""FastAPI service for the travel desk assistant."""
from fastapi import FastAPI
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from app.agent import root_agent

app = FastAPI()
sessions = InMemorySessionService()
runner = Runner(app_name="travel-desk", agent=root_agent, session_service=sessions)


class Message(BaseModel):
    tenant_id: str
    traveller_id: str
    message: str
    session_id: str | None = None


@app.post("/chat")
async def chat(msg: Message):
    session = None
    if msg.session_id:
        session = await sessions.get_session(app_name="travel-desk", user_id=msg.traveller_id,
                                             session_id=msg.session_id)
    if session is None:
        session = await sessions.create_session(app_name="travel-desk", user_id=msg.traveller_id,
                                                state={"tenant_id": msg.tenant_id})
    reply = []
    async for event in runner.run_async(user_id=msg.traveller_id, session_id=session.id,
                                        new_message=types.Content(role="user",
                                                                  parts=[types.Part(text=msg.message)])):
        if event.is_final_response() and event.content and event.content.parts:
            reply.extend(p.text for p in event.content.parts if p.text)
    return {"session_id": session.id, "reply": "".join(reply)}
