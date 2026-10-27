"""The claims agent and its input-screening callback."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.models import LlmResponse
from google.genai import types

from claims_agent import config
from claims_agent.screening import ALLOW, screen_text

WITHHELD = "Sorry, I can't help with that message. A member of the claims team can."


def screen_customer_input(callback_context, llm_request):
    """before_model_callback: screen the customer's latest text before the model sees it."""
    if not llm_request.contents:
        return None
    latest = llm_request.contents[-1]
    if latest.role != "user":
        return None
    for part in latest.parts or []:
        if part.text:
            verdict = screen_text(part.text)
            if verdict.decision != ALLOW:
                return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=WITHHELD)]))
    return None


root_agent = LlmAgent(
    name="claims_assistant",
    model=config.MODEL_ID,
    instruction=(
        "You help Lindqvist Mutual policyholders report a home-insurance claim and follow it up. "
        "Use the photos and documents they attach to describe the damage. Never decide cover; "
        "say a claims handler will confirm."
    ),
    before_model_callback=screen_customer_input,
)
