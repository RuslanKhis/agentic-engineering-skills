"""Runs the extractor for one claim and returns the record for the claims queue."""
from __future__ import annotations

import json

from google.adk.runners import InMemoryRunner
from google.genai import types

from extractor.agent import extraction_agent
from extractor.schema import ClaimExtraction

runner = InMemoryRunner(agent=extraction_agent, app_name="claim_intake")


async def extract(claim_text: str, user_id: str = "intake") -> ClaimExtraction:
    session = await runner.session_service.create_session(app_name="claim_intake", user_id=user_id)
    message = types.Content(role="user", parts=[types.Part(text=claim_text)])
    async for _ in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
        pass
    session = await runner.session_service.get_session(app_name="claim_intake", user_id=user_id,
                                                       session_id=session.id)
    raw = session.state["extraction"]
    if isinstance(raw, str):
        raw = json.loads(raw)
    return ClaimExtraction.model_validate(raw)
