"""Session store construction and failure mapping.

No `google.adk` import at module level, so the unit tests can import this
without the SDK; the SDK class is imported when the service is built.
"""
from __future__ import annotations

from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class SessionStoreUnavailable(Exception):
    """The session database could not be reached or failed during an operation."""


def build_session_service(db_url: str):
    from google.adk.sessions import DatabaseSessionService

    return DatabaseSessionService(db_url=db_url)


def _store_errors() -> tuple[type[BaseException], ...]:
    try:
        from sqlalchemy.exc import SQLAlchemyError
    except ImportError:
        return (OSError,)
    return (SQLAlchemyError, OSError)


@contextmanager
def store_guard():
    """Map database failures to SessionStoreUnavailable; other errors pass through."""
    try:
        yield
    except _store_errors() as exc:
        logger.error("session store failure: %s", type(exc).__name__)
        raise SessionStoreUnavailable() from exc
