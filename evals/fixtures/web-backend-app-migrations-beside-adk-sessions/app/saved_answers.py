"""Saved answers: a customer can keep an assistant answer to read later."""
from __future__ import annotations

from sqlalchemy import insert, select

from app.db import saved_answers


def save(engine, user_id: str, question: str, answer: str) -> int:
    with engine.begin() as conn:
        result = conn.execute(insert(saved_answers).values(user_id=user_id, question=question, answer=answer))
        return int(result.inserted_primary_key[0])


def get(engine, answer_id: int) -> dict | None:
    with engine.connect() as conn:
        row = conn.execute(select(saved_answers).where(saved_answers.c.id == answer_id)).mappings().first()
        return dict(row) if row else None


def list_for(engine, user_id: str) -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(select(saved_answers).where(saved_answers.c.user_id == user_id)
                            .order_by(saved_answers.c.created_at.desc())).mappings().all()
        return [dict(r) for r in rows]
