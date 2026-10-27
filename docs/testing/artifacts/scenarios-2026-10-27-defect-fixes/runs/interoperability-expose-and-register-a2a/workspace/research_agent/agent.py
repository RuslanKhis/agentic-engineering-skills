"""Root research agent and its two single-turn specialists."""
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from research_agent.a2a_guard import block_gated_tools
from research_agent.tools import search_reports, submit_procurement_request

MODEL = "gemini-3.5-flash"


def _market_analyst() -> LlmAgent:
    # An agent can have one parent, so each root builds its own instance.
    return LlmAgent(
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
    sub_agents=[_market_analyst(), procurement_assistant],
)

# Root served over A2A. It has no procurement sub-agent, so nothing a remote caller sends
# (including a message that claims approval) can reach submit_procurement_request.
# before_tool_callback is a second layer in case a gated tool is added later.
a2a_root_agent = LlmAgent(
    name="research_lead",
    model=MODEL,
    description="Market and competitor research for the sales team.",
    instruction=(
        "You help the sales team with market research. Use market_analyst for sizing questions. "
        "You cannot buy reports; if asked, say that purchases are made in the research app."
    ),
    sub_agents=[_market_analyst()],
    before_tool_callback=block_gated_tools,
)
