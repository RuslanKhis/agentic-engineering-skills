from google.adk.agents import LlmAgent
from google.genai import types

from expense_agent import tools
from expense_agent.prompts import INSTRUCTION
from expense_agent.store import ClaimStore

tools.configure(ClaimStore("claims.db"))

root_agent = LlmAgent(
    name="expense_triage",
    model="gemini-3.5-flash",
    description="Triages expense claims: decide or escalate to finance review.",
    instruction=INSTRUCTION,
    tools=[tools.decide_claim, tools.escalate_claim],
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
)
