"""SSE endpoint the React app reads; relays ADK events as JSON lines."""
from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel

from insights.agent import root_agent

app = FastAPI()
runner = InMemoryRunner(agent=root_agent, app_name="insights")


class Ask(BaseModel):
    user_id: str
    session_id: str
    text: str


@app.post("/api/run_sse")
async def run_sse(body: Ask):
    async def stream():
        async for event in runner.run_async(user_id=body.user_id, session_id=body.session_id,
                                            new_message=types.Content(role="user", parts=[types.Part(text=body.text)])):
            yield "data: " + event.model_dump_json(exclude_none=True) + "\n\n"
    return StreamingResponse(stream(), media_type="text/event-stream")
