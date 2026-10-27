"""Reply-language preference: save, read and forget, keyed on the verified user ID."""
from __future__ import annotations

import datetime as dt

from app.store import Store

LANGUAGE_KEY = "user:language"
SUPPORTED = {"en", "de", "fr", "es", "it", "nl", "pl"}


class UnsupportedLanguage(ValueError):
    pass


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


class Preferences:
    def __init__(self, store: Store) -> None:
        self.store = store

    def save(self, user_id: str, language: str) -> None:
        language = language.strip().lower()
        if language not in SUPPORTED:
            raise UnsupportedLanguage(language)
        with self.store.conn:
            self.store.conn.execute(
                "INSERT INTO preferences (user_id, language, updated_at, deleted_at) VALUES (?, ?, ?, NULL) "
                "ON CONFLICT(user_id) DO UPDATE SET language = excluded.language, "
                "updated_at = excluded.updated_at, deleted_at = NULL",
                (user_id, language, _now()))

    def get(self, user_id: str) -> str | None:
        row = self.store.conn.execute(
            "SELECT language FROM preferences WHERE user_id = ? AND deleted_at IS NULL", (user_id,)).fetchone()
        return row["language"] if row else None

    def forget(self, user_id: str, state: dict | None = None) -> bool:
        """Soft delete: the row keeps deleted_at for 30 days; the session copy goes now."""
        with self.store.conn:
            cur = self.store.conn.execute(
                "UPDATE preferences SET deleted_at = ? WHERE user_id = ? AND deleted_at IS NULL",
                (_now(), user_id))
        if state is not None:
            state.pop(LANGUAGE_KEY, None)
        return cur.rowcount > 0

    def load_into_state(self, user_id: str, state: dict) -> None:
        language = self.get(user_id)
        if language:
            state[LANGUAGE_KEY] = language
        else:
            state.pop(LANGUAGE_KEY, None)
