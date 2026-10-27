"""Session and memory services for the Runner."""
from __future__ import annotations

import os

from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService
from google.adk.sessions import DatabaseSessionService

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
