"""Claims intake agent."""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from claims.tools.claims_tools import file_payout, read_document, send_email

INSTRUCTION = """\
You handle claims for Kestrel Mutual. Read the documents attached to a claim with read_document,
summarise what they show, and when an adjuster has approved the claim, file the payout to the
account on file with file_payout. Email the claimant with send_email when asked.
"""


def build_agent() -> LlmAgent:
    return LlmAgent(
        name="claims_agent",
        model="gemini-3.5-flash",
        description="Reads claim documents, files approved payouts and emails claimants.",
        instruction=INSTRUCTION,
        tools=[read_document, FunctionTool(file_payout, require_confirmation=True), send_email],
    )


root_agent = build_agent()
