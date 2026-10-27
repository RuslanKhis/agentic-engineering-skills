"""Session start: preload the customer's profile into session state so the first reply is fast."""
from __future__ import annotations

from app.preferences import LANGUAGE_KEY, Preferences

# Profile lookups hit SQLite on every new chat; keep the last value per user in process.
_PROFILE_CACHE: dict[str, dict] = {}


def initial_state(user_id: str, preferences: Preferences) -> dict:
    profile = _PROFILE_CACHE.get(user_id)
    if profile is None:
        profile = {"language": preferences.get(user_id)}
        _PROFILE_CACHE[user_id] = profile
    state: dict = {}
    if profile.get("language"):
        state[LANGUAGE_KEY] = profile["language"]
    return state
