"""Application tables in the same PostgreSQL database as the ADK sessions.

Production: DATABASE_URL=postgresql+psycopg://...@/support?host=/cloudsql/<instance>
Local tests: sqlite:///:memory:
"""
from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text, create_engine, func

metadata = MetaData()

saved_answers = Table(
    "saved_answers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String(128), nullable=False, index=True),
    Column("question", Text, nullable=False),
    Column("answer", Text, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)


def make_engine(url: str):
    engine = create_engine(url, pool_pre_ping=True)
    metadata.create_all(engine)
    return engine
