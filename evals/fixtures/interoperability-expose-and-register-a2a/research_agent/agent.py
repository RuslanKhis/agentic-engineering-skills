"""Root research agent and its two single-turn specialists."""
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from research_agent.tools import search_reports, submit_procurement_request

MODEL = "gemini-3.5-flash"

market_analyst = LlmAgent(
    name="market_analyst",
    model=MODEL,
    mode="single_turn",
    description="Sizes markets and growth from published reports.",
    instruction="Answer the market question from the reports search_reports finds.",
    tools=[search_reports],
)

procurement_assistant = LlmAgent(
    name="procurement_assistant",
    model=MODEL,
    mode="single_turn",
    description="Opens a procurement request for a paid analyst report.",
    instruction="When the user wants a paid report, open a procurement request for it.",
    tools=[FunctionTool(submit_procurement_request, require_confirmation=True)],
)

root_agent = LlmAgent(
    name="research_lead",
    model=MODEL,
    description="Market and competitor research for the sales team.",
    instruction=(
        "You help the sales team with market research. Use market_analyst for sizing questions and "
        "procurement_assistant when the user asks to buy a report."
    ),
    sub_agents=[market_analyst, procurement_assistant],
)
