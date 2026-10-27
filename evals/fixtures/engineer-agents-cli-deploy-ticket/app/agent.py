"""Claims helper agent for claims handlers."""
import os

from google.adk.agents import Agent
from google.adk.apps import App

from app.tools import get_claim, missing_documents

MODEL = os.environ.get("MODEL_ID", "gemini-3.5-flash")

root_agent = Agent(
    name="claims_helper",
    model=MODEL,
    description="Answers claims handlers' questions about open home-insurance claims.",
    instruction=(
        "You help claims handlers. Look claims up with get_claim and list outstanding documents "
        "with missing_documents. Never change a claim; you have no tool for that."
    ),
    tools=[get_claim, missing_documents],
)

app = App(name="app", root_agent=root_agent)
