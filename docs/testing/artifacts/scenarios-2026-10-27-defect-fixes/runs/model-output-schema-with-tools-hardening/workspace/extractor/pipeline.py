"""Runs the extractor for one claim and returns the record for the claims queue."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Optional

from pydantic import ValidationError

from extractor.schema import ClaimExtraction

MAX_ATTEMPTS = 3
APP_NAME = "claim_intake"

_FENCE = re.compile(r"```\w*\s*(.*?)\s*```", re.DOTALL)


@dataclass
class ExtractionResult:
    """status is "ok" or "failed"; a failed result carries no record and the last error."""
    status: str
    extraction: Optional[ClaimExtraction]
    attempts: int
    error: Optional[str] = None


def parse_extraction(raw) -> ClaimExtraction:
    """Accept the dict ADK saves, or a string (plain or fenced JSON), and validate it."""
    if isinstance(raw, str):
        text = raw.strip()
        fenced = _FENCE.fullmatch(text)
        raw = json.loads(fenced.group(1) if fenced else text)
    return ClaimExtraction.model_validate(raw)


def _retry_message(claim_text: str, error: str) -> str:
    return (f"{claim_text}\n\n[Previous attempt failed validation: {error}. "
            "Extract again and return a record that matches the schema.]")


async def _run_once(runner, message_text: str, user_id: str):
    from google.genai import types

    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=user_id)
    message = types.Content(role="user", parts=[types.Part(text=message_text)])
    async for _ in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
        pass
    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session.id)
    return session.state.get("extraction")


async def extract_with_runner(runner, claim_text: str, user_id: str = "intake",
                              max_attempts: int = MAX_ATTEMPTS) -> ExtractionResult:
    """Bounded retry: each attempt is a fresh session; the validation error is fed back verbatim."""
    error = None
    for attempt in range(1, max_attempts + 1):
        text = claim_text if error is None else _retry_message(claim_text, error)
        try:
            raw = await _run_once(runner, text, user_id)
            if raw is None:
                raise ValueError("agent finished without saving an extraction")
            return ExtractionResult("ok", parse_extraction(raw), attempt)
        except (ValidationError, ValueError) as exc:  # ValidationError is a ValueError; json errors too
            error = f"{type(exc).__name__}: {exc}"
    return ExtractionResult("failed", None, max_attempts, error)


async def extract(claim_text: str, user_id: str = "intake") -> ExtractionResult:
    from google.adk.runners import InMemoryRunner

    from extractor.agent import extraction_agent

    runner = InMemoryRunner(agent=extraction_agent, app_name=APP_NAME)
    return await extract_with_runner(runner, claim_text, user_id)
