"""Classifies inbound emails before the support agent sees them."""
from google.adk.agents import LlmAgent

from app.prompts import TRIAGE_INSTRUCTION

triage_agent = LlmAgent(
    name="email_triage",
    model="gemini-2.5-pro",
    instruction=TRIAGE_INSTRUCTION,
)
