"""Runner wiring: Mem0 for long-term memory, sessions in SQLite, memory written after each turn."""
from __future__ import annotations

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from homeline.agent import root_agent
from homeline.memory.mem0_service import Mem0MemoryService

APP_NAME = "homeline"

memory_service = Mem0MemoryService()
session_service = DatabaseSessionService(db_url="sqlite+aiosqlite:///homeline_sessions.db")


async def save_to_memory(callback_context):
    session = callback_context._invocation_context.session
    await memory_service.add_session_to_memory(session)


root_agent.after_agent_callback = save_to_memory

runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service,
                memory_service=memory_service)
