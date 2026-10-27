"""Claims intake agent."""
from google.adk.agents import LlmAgent

from claims_agent.policy import check_cover

root_agent = LlmAgent(
    name="claims_intake",
    model="gemini-2.5-flash",
    instruction=(
        "Help the claims handler draft a first-notice-of-loss summary. Check cover with check_cover. "
        "Never promise a payout."
    ),
    tools=[check_cover],
)
