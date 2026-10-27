"""Session and memory services for the Runner."""
from __future__ import annotations

import os
from functools import lru_cache

from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService
from google.adk.sessions import DatabaseSessionService

from fieldline.memory_adk import AdkMemoryBackend, GovernedMemoryService, in_memory_eraser_for
from fieldline.memory_governor import MemoryGovernor
from fieldline.memory_ledger import MemoryLedger

APP_NAME = "fieldline"


def session_service():
    return DatabaseSessionService(db_url=os.environ.get("SESSION_DB_URL", "sqlite+aiosqlite:///fieldline.db"))


def _raw_memory_service():
    engine_id = os.environ.get("AGENT_ENGINE_ID")
    if engine_id:
        return VertexAiMemoryBankService(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                                         location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
                                         agent_engine_id=engine_id)
    return InMemoryMemoryService()


@lru_cache(maxsize=1)
def governor() -> MemoryGovernor:
    """One governor per process, shared by the tools, the write callback and the read service."""
    raw = _raw_memory_service()
    ledger_path = os.environ.get("MEMORY_LEDGER_DB")
    if os.environ.get("AGENT_ENGINE_ID") and not ledger_path:
        # Consent and erasure records must outlive the process. Refuse to run deployed without a durable ledger.
        raise RuntimeError("MEMORY_LEDGER_DB must point at a durable, shared ledger when AGENT_ENGINE_ID is set")
    eraser = in_memory_eraser_for(raw, APP_NAME) if isinstance(raw, InMemoryMemoryService) else None
    return MemoryGovernor(MemoryLedger(ledger_path), AdkMemoryBackend(raw, APP_NAME, eraser))


def memory_service():
    """The read side the Runner and PreloadMemoryTool see: consent-gated, forgotten facts filtered out."""
    return GovernedMemoryService(governor())
