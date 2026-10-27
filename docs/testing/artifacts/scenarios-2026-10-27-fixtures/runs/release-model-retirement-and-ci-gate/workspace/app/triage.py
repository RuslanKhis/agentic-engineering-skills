"""Classifies inbound emails before the support agent sees them."""
from google.adk.agents import LlmAgent

from app.prompts import TRIAGE_INSTRUCTION
from app.settings import Settings

triage_agent = LlmAgent(
    name="email_triage",
    model=Settings.from_env().model_id,
    instruction=TRIAGE_INSTRUCTION,
)
