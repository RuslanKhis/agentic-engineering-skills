"""Conversation export for the support team's weekly review."""
from __future__ import annotations

import csv
import io

from app import services


def export_conversations(since: str, tool_context) -> dict:
    """Export saved conversations started on or after a date as CSV.

    Args:
        since: ISO date, e.g. "2026-10-01".

    Returns:
        {"status": "ok", "csv": "<conversation_id,user_id,started_at,transcript rows>"}.
    """
    store = services.get().store
    rows = store.conn.execute(
        "SELECT conversation_id, user_id, started_at, transcript FROM conversations WHERE started_at >= ? "
        "ORDER BY started_at", (since,)).fetchall()
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["conversation_id", "user_id", "started_at", "transcript"])
    for row in rows:
        writer.writerow([row["conversation_id"], row["user_id"], row["started_at"], row["transcript"]])
    return {"status": "ok", "csv": out.getvalue()}
