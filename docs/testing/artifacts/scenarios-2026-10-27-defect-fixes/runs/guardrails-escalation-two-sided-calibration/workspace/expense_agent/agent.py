from google.adk.agents import LlmAgent
from google.genai import types

from expense_agent import tools
from expense_agent.policy import forced_escalation_reason
from expense_agent.prompts import INSTRUCTION
from expense_agent.store import ClaimStore

tools.configure(ClaimStore("claims.db"))


def route_forced_escalations(callback_context):
    """Send code-forced cases to review without a model call; otherwise let the model run."""
    claim = callback_context.state.get("claim")
    if not isinstance(claim, dict):
        claim = {}  # unreadable claim: fail closed
    reason = forced_escalation_reason(claim)
    if reason is None:
        return None
    tools.escalate_claim(claim.get("claim_id", ""), reason)
    return types.Content(role="model", parts=[types.Part(text=f"Sent to finance review: {reason}.")])


root_agent = LlmAgent(
    name="expense_triage",
    model="gemini-3.5-flash",
    description="Triages expense claims: decide or escalate to finance review.",
    instruction=INSTRUCTION,
    before_agent_callback=route_forced_escalations,
    tools=[tools.decide_claim, tools.escalate_claim],
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
)
