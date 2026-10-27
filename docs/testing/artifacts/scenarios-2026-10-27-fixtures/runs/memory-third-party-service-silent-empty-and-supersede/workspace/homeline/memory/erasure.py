"""Erase what the assistant holds about one user: Mem0 memories and stored sessions."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


async def erase_user_data(*, memory_service, session_service, app_name: str, user_id: str) -> dict:
    """Run both erasures even if one fails; the result says which sinks are done.

    The caller must have authenticated ``user_id`` as the requester (or a support
    agent acting on a verified request) before calling this.
    """
    result = {"memories": "failed", "sessions": "failed", "sessions_deleted": 0}
    try:
        memory_service.erase_user(user_id)
        result["memories"] = "deleted"
    except Exception:
        logger.error("memory erasure incomplete", exc_info=True)
    try:
        listing = await session_service.list_sessions(app_name=app_name, user_id=user_id)
        for s in listing.sessions:
            await session_service.delete_session(app_name=app_name, user_id=user_id, session_id=s.id)
            result["sessions_deleted"] += 1
        remaining = await session_service.list_sessions(app_name=app_name, user_id=user_id)
        result["sessions"] = "deleted" if not remaining.sessions else "failed"
    except Exception:
        logger.error("session erasure incomplete", exc_info=True)
    return result
