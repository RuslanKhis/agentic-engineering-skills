"""Builds the travel agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent

from travel_agent import tools

INSTRUCTION = """You book flights for staff. Search, confirm the choice with the traveller, book it
with a fresh idempotency key, and send the confirmation. Never claim a booking you did not make."""


def build_agent(before_tool_callback=None) -> LlmAgent:
    return LlmAgent(name="travel_agent", model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
                    instruction=INSTRUCTION,
                    tools=[tools.search_flights, tools.book_flight, tools.send_confirmation],
                    before_tool_callback=before_tool_callback)
