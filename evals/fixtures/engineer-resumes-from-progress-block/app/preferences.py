"""The customer's reply-language preference (design D1: an exact setting, not memory)."""
from __future__ import annotations

from app.store import Store

LANGUAGE = "language"
SUPPORTED = {"en": "English", "de": "Deutsch", "fr": "Français", "es": "Español", "nl": "Nederlands"}
STATE_KEY = "user:language"


class UnsupportedLanguage(ValueError):
    pass


def save_language(store: Store, user_id: str, code: str) -> str:
    code = code.strip().lower()
    if code not in SUPPORTED:
        raise UnsupportedLanguage(code)
    store.set_preference(user_id, LANGUAGE, code)
    return code


def get_language(store: Store, user_id: str) -> str | None:
    return store.get_preference(user_id, LANGUAGE)


def forget_language(store: Store, user_id: str) -> bool:
    return store.delete_preference(user_id, LANGUAGE)


def initial_state(store: Store, user_id: str) -> dict:
    """State for a new session: the saved language, if any, under user:language."""
    code = get_language(store, user_id)
    return {STATE_KEY: SUPPORTED[code]} if code else {}
