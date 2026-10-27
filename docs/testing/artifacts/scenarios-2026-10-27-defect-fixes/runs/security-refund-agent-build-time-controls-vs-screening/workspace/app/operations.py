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

    def committed_cents(self, order_id: str) -> int:
        """Cents promised or paid on this order: pending (outcome unknown) plus succeeded."""
        row = self.conn.execute("SELECT COALESCE(SUM(amount_cents), 0) FROM refund_operations "
                                "WHERE order_id = ? AND status IN ('pending', 'succeeded')",
                                (order_id,)).fetchone()
        return int(row[0])

    def reserve(self, order_id: str, amount_cents: int, reason: str, order_total_cents: int) -> str | None:
        """Aggregate bound keyed on the order: record a pending operation only if everything
        already committed plus this amount stays within the order total. The check and the insert
        share one write transaction, so concurrent attempts cannot both pass. None means refused."""
        self.conn.commit()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.committed_cents(order_id) + amount_cents > order_total_cents:
                self.conn.rollback()
                return None
            op_id = f"op_{uuid.uuid4().hex}"
            self.conn.execute("INSERT INTO refund_operations (op_id, order_id, amount_cents, reason, status) "
                              "VALUES (?, ?, ?, ?, 'pending')", (op_id, order_id, amount_cents, reason))
            self.conn.commit()
            return op_id
        except BaseException:
            self.conn.rollback()
            raise

    def finish(self, op_id: str, status: str, provider_ref: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE refund_operations SET status = ?, provider_ref = ? WHERE op_id = ?",
                              (status, provider_ref, op_id))

    def get(self, op_id: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM refund_operations WHERE op_id = ?", (op_id,)).fetchone()
        return dict(row) if row else None
