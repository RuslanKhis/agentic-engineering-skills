from google.adk.agents import LlmAgent

from claims.tools import add_claim_note, claim_status

INSTRUCTION = """\
You help Coastline Insurance policyholders follow up their home-insurance claims. Check a
claim with claim_status and record new information with add_claim_note. Never promise a
payout or a decision; say who decides and when.
"""

root_agent = LlmAgent(
    name="coastline_claims",
    model="gemini-3.5-flash",
    instruction=INSTRUCTION,
    tools=[claim_status, add_claim_note],
)
