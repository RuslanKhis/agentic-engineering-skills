"""Tidewater claims assistant."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from claims.tools import add_note, get_claim

INSTRUCTION = """\
You help Tidewater Insurance policyholders with their own claims. Look claims up with get_claim
and add the policyholder's notes with add_note. Use what you remember from earlier conversations
about an open claim. Never say whether a claim will be paid or how much.
"""

root_agent = LlmAgent(
    name="claims_assistant",
    model=os.environ.get("MODEL_ID", "gemini-3.5-flash-001"),
    instruction=INSTRUCTION,
    tools=[get_claim, add_note, PreloadMemoryTool()],
)
