from google.adk.agents import LlmAgent
from profile_store import ProfileStore, UserScope


def make_agent(store: ProfileStore, scope: UserScope) -> LlmAgent:
    return LlmAgent(
        name="language_helper",
        model="gemini-2.5-flash",
        instruction="Answer clearly and helpfully.",
    )
