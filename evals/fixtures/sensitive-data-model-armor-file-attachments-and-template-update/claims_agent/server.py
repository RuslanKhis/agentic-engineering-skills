"""HTTP routes: chat and attachment upload."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, UploadFile
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel

from claims_agent.agent import root_agent
from claims_agent.attachments import AttachmentRejected, accept_attachment, to_part

app = FastAPI(title="Claims assistant")
runner = InMemoryRunner(agent=root_agent, app_name="claims")
pending: dict[str, list] = {}


@app.post("/api/sessions/{session_id}/attachments")
async def upload(session_id: str, file: UploadFile):
    data = await file.read()
    try:
        attachment = accept_attachment(file.filename or "upload", file.content_type or "", data)
    except AttachmentRejected as exc:
        raise HTTPException(status_code=415, detail=str(exc))
    pending.setdefault(session_id, []).append(attachment)
    return {"accepted": attachment.filename}


class ChatIn(BaseModel):
    user_id: str
    message: str


@app.post("/api/sessions/{session_id}/chat")
async def chat(session_id: str, body: ChatIn):
    parts = [types.Part(text=body.message)] + [to_part(a) for a in pending.pop(session_id, [])]
    reply = []
    async for event in runner.run_async(user_id=body.user_id, session_id=session_id,
                                        new_message=types.Content(role="user", parts=parts)):
        if event.is_final_response() and event.content:
            reply.extend(p.text for p in event.content.parts or [] if p.text)
    return {"reply": "".join(reply)}
