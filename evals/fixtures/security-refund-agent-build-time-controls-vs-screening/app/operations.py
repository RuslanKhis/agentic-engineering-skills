"""Operation records for refunds: one row per refund attempt, keyed by its idempotency key."""
from __future__ import annotations

import sqlite3
import uuid

SCHEMA = """
CREATE TABLE IF NOT EXISTS refund_operations (
    op_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    provider_ref TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class OperationStore:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.executescript(SCHEMA)

    def start(self, order_id: str, amount_cents: int, reason: str) -> str:
        op_id = f"op_{uuid.uuid4().hex}"
        with self.conn:
            self.conn.execute("INSERT INTO refund_operations (op_id, order_id, amount_cents, reason, status) "
                              "VALUES (?, ?, ?, ?, 'pending')", (op_id, order_id, amount_cents, reason))
        return op_id

    def finish(self, op_id: str, status: str, provider_ref: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE refund_operations SET status = ?, provider_ref = ? WHERE op_id = ?",
                              (status, provider_ref, op_id))

    def get(self, op_id: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM refund_operations WHERE op_id = ?", (op_id,)).fetchone()
        return dict(row) if row else None
