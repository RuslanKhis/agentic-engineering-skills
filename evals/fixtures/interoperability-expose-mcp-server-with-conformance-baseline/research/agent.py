"""The research agent."""
from google.adk.agents import LlmAgent

from research.tools import get_abstract, search_papers

root_agent = LlmAgent(
    name="paper_research",
    model="gemini-3.5-flash",
    description="Answers questions about published papers in the team's index.",
    instruction=(
        "You answer questions about papers in the index. Search with search_papers, read abstracts "
        "with get_abstract, and cite paper ids. Never invent a paper."
    ),
    tools=[search_papers, get_abstract],
)
