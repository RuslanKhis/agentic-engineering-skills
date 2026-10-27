"""Back-office approvals: resume a paused refund invocation with the manager's answer."""
from __future__ import annotations

import os

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from app.workflow import app as adk_app

sessions = DatabaseSessionService(db_url=os.environ.get("SESSION_DB_URL",
                                                         "postgresql+asyncpg://refunds@localhost:5432/refunds"))
runner = Runner(app=adk_app, session_service=sessions)


async def answer(user_id: str, session_id: str, invocation_id: str, function_call_id: str,
                 approved: bool) -> list:
    """Called by the back office when a manager approves or rejects. Resumes the paused invocation."""
    reply = types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
        id=function_call_id, name="adk_request_confirmation", response={"confirmed": approved}))])
    events = []
    async for event in runner.run_async(user_id=user_id, session_id=session_id,
                                        invocation_id=invocation_id, new_message=reply):
        events.append(event)
    return events
