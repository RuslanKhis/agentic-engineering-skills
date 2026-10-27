"""Durable record of each refund operation, so a restart can tell what was already attempted."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS refund_operations (
    operation_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    payload_sha256 TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('pending', 'succeeded', 'failed')),
    attempts INTEGER NOT NULL DEFAULT 0,
    provider_refund_id TEXT,
    last_error TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def payload_hash(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class OperationStore:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def begin(self, operation_id: str, order_id: str, amount_cents: int, payload: dict) -> dict[str, Any]:
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO refund_operations (operation_id, order_id, amount_cents, payload_sha256, state) "
                "VALUES (?, ?, ?, ?, 'pending')", (operation_id, order_id, amount_cents, payload_hash(payload)))
        return self.get(operation_id)

    def get(self, operation_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM refund_operations WHERE operation_id = ?",
                                (operation_id,)).fetchone()
        return dict(row) if row else None

    def record_attempt(self, operation_id: str, error: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE refund_operations SET attempts = attempts + 1, last_error = ?, "
                              "updated_at = CURRENT_TIMESTAMP WHERE operation_id = ?", (error, operation_id))

    def succeed(self, operation_id: str, provider_refund_id: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE refund_operations SET state = 'succeeded', provider_refund_id = ?, "
                              "updated_at = CURRENT_TIMESTAMP WHERE operation_id = ?",
                              (provider_refund_id, operation_id))

    def fail(self, operation_id: str, error: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE refund_operations SET state = 'failed', last_error = ?, "
                              "updated_at = CURRENT_TIMESTAMP WHERE operation_id = ?", (error, operation_id))
