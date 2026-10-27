"""Per-user response-language preference. No google.adk imports so the unit tests run without the SDK.

An exact user setting, so it is a deterministic profile value, not semantic memory. It lives in
ADK `user:` state, which the Cloud SQL `DatabaseSessionService` keeps per (app_name, user_id)
across sessions and restarts. Only trusted code writes it, and only values from the allow-list.
"""
from __future__ import annotations

LANGUAGE_KEY = "user:response_language"

# Allow-list: the stored value is placed in the system instruction, so free text is never accepted.
# Keys are lower-case names or BCP-47 tags a user may say; values are the canonical stored name.
LANGUAGES = {
    "english": "English", "en": "English",
    "french": "French", "fr": "French",
    "german": "German", "de": "German",
    "spanish": "Spanish", "es": "Spanish",
    "italian": "Italian", "it": "Italian",
    "portuguese": "Portuguese", "pt": "Portuguese",
    "dutch": "Dutch", "nl": "Dutch",
    "polish": "Polish", "pl": "Polish",
    "ukrainian": "Ukrainian", "uk": "Ukrainian",
    "russian": "Russian", "ru": "Russian",
    "turkish": "Turkish", "tr": "Turkish",
    "arabic": "Arabic", "ar": "Arabic",
    "hindi": "Hindi", "hi": "Hindi",
    "chinese": "Chinese", "zh": "Chinese",
    "japanese": "Japanese", "ja": "Japanese",
    "korean": "Korean", "ko": "Korean",
}


def normalise_language(value: str) -> str | None:
    """Return the canonical language name, or None when the value is not on the allow-list."""
    if not isinstance(value, str):
        return None
    return LANGUAGES.get(value.strip().lower())


def stored_language(state) -> str | None:
    """Read the saved language, re-validating so a tampered or stale stored value is ignored."""
    return normalise_language(state.get(LANGUAGE_KEY))


def language_instruction(state) -> str:
    language = stored_language(state)
    if not language:
        return ""
    return (f"\nThe caller's saved response language is {language}. Write every reply in {language}, "
            "but keep article IDs, ticket IDs and product names unchanged.")
