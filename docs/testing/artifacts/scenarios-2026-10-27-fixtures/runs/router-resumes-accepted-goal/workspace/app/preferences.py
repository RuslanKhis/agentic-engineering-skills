"""The customer's saved reply language: an exact setting they control (design D1)."""
from __future__ import annotations

import re

from app.auth import Principal
from app.store import Store

STATE_KEY = "user:language"
_LANGUAGE = re.compile(r"^[^\W\d_](?:[^\W\d_]|[ \-]){0,38}[^\W\d_]$")


class PreferenceNotFound(Exception):
    pass


def get_language(store: Store, principal: Principal) -> dict:
    """The caller's own language. Only ever the caller's own row."""
    language = store.get_language(principal.user_id)
    if language is None:
        raise PreferenceNotFound(principal.user_id)
    return {"language": language}


def save_language(store: Store, principal: Principal, language: str) -> dict:
    value = " ".join(language.split())
    if not _LANGUAGE.match(value):
        raise ValueError("language must be 2 to 40 letters, spaces or hyphens")
    store.set_language(principal.user_id, value)
    return get_language(store, principal)


def forget_language(store: Store, principal: Principal) -> None:
    if not store.delete_language(principal.user_id):
        raise PreferenceNotFound(principal.user_id)


def initial_session_state(store: Store, principal: Principal) -> dict[str, str]:
    """State for a new session. Always sets the key: the session service keeps `user:` state
    across sessions, so after a forget the empty value must overwrite the old one."""
    return {STATE_KEY: store.get_language(principal.user_id) or ""}
