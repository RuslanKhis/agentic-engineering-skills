"""Memory write-back gated by the policyholder's account setting; recall is PreloadMemoryTool in claims/agent.py."""
from __future__ import annotations

import logging
from typing import Protocol

log = logging.getLogger(__name__)


class MemorySettings(Protocol):
    def memory_declined(self, user_id: str) -> bool: ...


class DictMemorySettings:
    def __init__(self, declined: set[str] | None = None):
        self.declined = declined or set()

    def memory_declined(self, user_id):
        return user_id in self.declined


_settings: MemorySettings | None = None


def use_memory_settings(settings: MemorySettings | None) -> None:
    global _settings
    _settings = settings


async def write_session_to_memory(callback_context) -> None:
    """after_agent_callback: write the session to Memory Bank unless the policyholder declined.

    Scope is the verified user ID the Runner was given. Unknown or unreadable setting writes nothing,
    and a failed write is logged without breaking the policyholder's reply.
    """
    if _settings is None:
        log.warning("memory settings not configured; session not written to memory")
        return None
    try:
        if _settings.memory_declined(callback_context.user_id):
            return None
        await callback_context.add_session_to_memory()
    except Exception:
        log.exception("memory write-back failed")
    return None
