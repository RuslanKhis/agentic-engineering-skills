"""Reply-language preference: the owner-keyed profile logic. No google.adk or fastapi imports.

The user ID is always the verified principal's (app/auth.py); nothing here accepts one from a body.
A missing preference and another customer's preference look the same: None / False (the route maps both to 404).
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from app.store import Store

STATE_KEY = "user:language"
RETENTION_DAYS = 30  # soft-deleted rows are kept this long, then purged
_LANGUAGE = re.compile(r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$")


class InvalidLanguage(ValueError):
    pass


def _stamp(now: datetime | None) -> str:
    return (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()


def validate_language(raw: str) -> str:
    value = (raw or "").strip()
    if not 2 <= len(value) <= 40 or not _LANGUAGE.match(value):
        raise InvalidLanguage("language must be 2-40 letters, e.g. 'Deutsch'")
    return value


def save(store: Store, user_id: str, raw: str, now: datetime | None = None) -> str:
    value = validate_language(raw)
    store.save_language(user_id, value, _stamp(now))
    return value


def get(store: Store, user_id: str) -> str | None:
    return store.get_language(user_id)


def forget(store: Store, user_id: str, now: datetime | None = None) -> bool:
    """Soft delete. False when there was nothing active to forget."""
    return store.forget_language(user_id, _stamp(now))


def purge_expired(store: Store, now: datetime | None = None, days: int = RETENTION_DAYS) -> int:
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=days)
    return store.purge_forgotten_before(_stamp(cutoff))


def session_state(store: Store, user_id: str) -> dict[str, str]:
    """Initial state for a new session. Always sets the key: an empty string overwrites a stale
    cached `user:` value, which ADK shares across the user's sessions."""
    return {STATE_KEY: store.get_language(user_id) or ""}
