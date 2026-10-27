"""Session and memory services for the Runner."""
from __future__ import annotations

import functools
import os

from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService
from google.adk.sessions import DatabaseSessionService

from fieldline.memory_controls import DEFAULT_TTL_DAYS, MemoryControls
from fieldline.tools import SITES

APP_NAME = "fieldline"


def session_service():
    return DatabaseSessionService(db_url=os.environ.get("SESSION_DB_URL", "sqlite+aiosqlite:///fieldline.db"))


def memory_service():
    engine_id = os.environ.get("AGENT_ENGINE_ID")
    if engine_id:
        return VertexAiMemoryBankService(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                                         location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
                                         agent_engine_id=engine_id)
    return InMemoryMemoryService()


@functools.cache
def memory_controls() -> MemoryControls:
    """Consent, fact records and the outbox. The ':memory:' default forgets consent on restart, which fails
    closed (nothing is saved or recalled), but a multi-instance deploy needs a shared durable store."""
    return MemoryControls(db_path=os.environ.get("MEMORY_CONTROL_DB", ":memory:"),
                          ttl_days=int(os.environ.get("MEMORY_FACT_TTL_DAYS", DEFAULT_TTL_DAYS)),
                          known_sites=SITES)
