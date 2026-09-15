from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext

from profile_store import ProfileStore, UserScope


def make_agent(store: ProfileStore, scope: UserScope) -> LlmAgent:
    def instruction(context: ReadonlyContext) -> str:
        # Identity comes only from the server-owned scope, never session state.
        language = store.get_preferred_language(scope)
        text = "Answer clearly and helpfully."
        if language is not None:
            text += f" Answer in {language}."
        return text

    return LlmAgent(
        name="language_helper",
        model="gemini-2.5-flash",
        instruction=instruction,
    )
