"""Root research agent with two specialist agents exposed as tools."""
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

GATEWAY = "https://llm-gateway.internal.example/v1"
RETRIES = types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=2))


def _model(name: str) -> LiteLlm:
    return LiteLlm(model=f"openai/{name}", api_base=GATEWAY, http_options=RETRIES)


scout = LlmAgent(
    name="literature_scout",
    model=_model("o-mini-2"),
    description="Finds and summarises published sources for a research question.",
    instruction="Find up to five relevant published sources and summarise each in two sentences.",
)

analyst = LlmAgent(
    name="numbers_analyst",
    model=_model("o-reasoner-2"),
    description="Works through market-size and growth calculations step by step.",
    instruction="Reason through the calculation and return the figures with their assumptions.",
)

root_agent = LlmAgent(
    name="research_lead",
    model=_model("o-reasoner-2"),
    instruction=(
        "Plan the research turn. Use literature_scout for sources and numbers_analyst for "
        "calculations, then write a short answer with citations."
    ),
    tools=[AgentTool(agent=scout), AgentTool(agent=analyst)],
)
