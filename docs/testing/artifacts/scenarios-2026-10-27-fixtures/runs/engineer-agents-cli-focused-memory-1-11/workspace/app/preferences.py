"""Per-user response-language preference. No google.adk imports so the unit tests run without the SDK.

The preference is an exact user-controlled setting, so it is a deterministic profile value, not a
semantic memory. It lives in ADK `user:` state, which the Cloud SQL `DatabaseSessionService`
persists per (app_name, user_id) across sessions. The user ID is the verified staff ID; the model
supplies only the language name, which is checked against an allowlist before it is stored.
"""
from __future__ import annotations

STATE_KEY = "user:response_language"

# Allowlist of language names the agent may be told to answer in. Extend deliberately.
LANGUAGES = {
    "english", "french", "german", "spanish", "italian", "portuguese", "dutch", "polish",
    "welsh", "arabic", "hindi", "urdu", "bengali", "punjabi", "mandarin chinese", "japanese",
}
RESET_WORDS = {"", "default", "reset", "none"}


def set_response_language(language: str, tool_context) -> dict:
    """Save the caller's preferred language for future replies, in this and later conversations.

    Call only when the user asks to be answered in a language or to go back to the default.

    Args:
        language: The language name in English, for example "French". Use "default" to clear it.
    """
    name = (language or "").strip().lower()
    if name in RESET_WORDS:
        tool_context.state[STATE_KEY] = ""
        return {"status": "cleared"}
    if name not in LANGUAGES:
        return {"status": "error", "message": "unsupported language",
                "supported": sorted(LANGUAGES)}
    tool_context.state[STATE_KEY] = name
    return {"status": "saved", "language": name}


def language_directive(state) -> str:
    """Instruction text for the saved preference; empty when none is saved or the value is unknown."""
    name = state.get(STATE_KEY) or ""
    if name not in LANGUAGES:
        return ""
    return (f"\nThe caller's saved response language is {name}. Reply in {name}, keeping article "
            "IDs and ticket IDs unchanged.\n")
