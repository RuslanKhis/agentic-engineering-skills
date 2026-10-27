from google.adk.agents import LlmAgent

from app.library import search_policies

root_agent = LlmAgent(
    name="doc_assistant",
    model="gemini-3.5-flash",
    description="Answers staff questions from the policy library.",
    instruction=(
        "Answer staff questions about internal policies. Search with search_policies and cite the "
        "policy ID and section for every statement. If nothing relevant is found, say so."
    ),
    tools=[search_policies],
)
