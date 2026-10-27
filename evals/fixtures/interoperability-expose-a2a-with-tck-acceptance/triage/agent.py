"""The triage agent."""
from google.adk.agents import LlmAgent

from triage.tools import lookup_product, record_triage

root_agent = LlmAgent(
    name="warranty_triage",
    model="gemini-3.5-flash",
    description="Classifies warranty claims by product, fault category and urgency.",
    instruction=(
        "Read the claim, look the product up by serial, choose one category and an urgency from 1 to 3, "
        "and record the triage."
    ),
    tools=[lookup_product, record_triage],
)
