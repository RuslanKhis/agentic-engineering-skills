import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from dataclasses import dataclass
from pathlib import Path


_LANGUAGES = ("English", "French", "Spanish", "Japanese")


def _validate_scope(scope: "UserScope") -> None:
    for field in (scope.app_name, scope.user_id):
        if not isinstance(field, str) or not field.strip():
            raise ValueError("Scope fields must be nonempty strings.")


@dataclass(frozen=True)
class UserScope:
    app_name: str
    user_id: str


class ProfileStore:
    """Exact, consented settings keyed by the trusted application and user."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS preferred_languages (
                    app_name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    PRIMARY KEY (app_name, user_id)
                )
                """
            )

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        # The transaction commits (or rolls back) before the connection closes.
        with closing(sqlite3.connect(self.path)) as connection:
            with connection:
                yield connection

    def save_preferred_language(self, scope: UserScope, language: str, *, consent: bool) -> None:
        _validate_scope(scope)
        if consent is not True:
            raise PermissionError("Explicit consent is required to save a preference.")
        if language not in _LANGUAGES:
            raise ValueError("Unsupported preferred language.")
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO preferred_languages (app_name, user_id, language)
                VALUES (?, ?, ?)
                ON CONFLICT (app_name, user_id)
                DO UPDATE SET language = excluded.language
                """,
                (scope.app_name, scope.user_id, language),
            )

    def get_preferred_language(self, scope: UserScope) -> str | None:
        _validate_scope(scope)
        with self._connection() as connection:
            row = connection.execute(
                """
                SELECT language FROM preferred_languages
                WHERE app_name = ? AND user_id = ?
                """,
                (scope.app_name, scope.user_id),
            ).fetchone()
        return row[0] if row is not None else None

    def forget_preferred_language(self, scope: UserScope) -> None:
        _validate_scope(scope)
        with self._connection() as connection:
            connection.execute(
                """
                DELETE FROM preferred_languages
                WHERE app_name = ? AND user_id = ?
                """,
                (scope.app_name, scope.user_id),
            )
