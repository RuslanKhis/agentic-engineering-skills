"""Agent callbacks that route input and output through app.screening.

Typed loosely so they can be unit-tested with duck-typed stand-ins.
"""
from __future__ import annotations

import logging

from app.screening import screening

log = logging.getLogger("support.agent")
REFUSAL = "Sorry, I can't help with that message. A member of the team will follow up."


def screen_input(callback_context, llm_request):
    """before_model_callback: refuse when Model Armor flags the customer's latest message."""
    latest = llm_request.contents[-1] if llm_request.contents else None
    if latest is None or latest.role != "user":
        return None
    text = " ".join(p.text for p in latest.parts or [] if getattr(p, "text", None))
    if text and not screening.input_allowed(text):
        log.info("input refused by screening for session %s", callback_context.state.get("session_ref"))
        from google.adk.models import LlmResponse
        from google.genai import types

        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=REFUSAL)]))
    return None


def deidentify_reply(callback_context, llm_response):
    """after_model_callback: de-identify reply text before it is stored or streamed."""
    if llm_response.content is None:
        return None
    for part in llm_response.content.parts or []:
        if getattr(part, "text", None):
            part.text = screening.deidentify(part.text)
    return llm_response
