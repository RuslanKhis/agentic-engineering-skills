"""Operation records for refunds: one row per refund attempt, keyed by its idempotency key."""
from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass

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


class RefundDenied(Exception):
    """A refund policy limit refused the request; nothing was recorded or sent."""


@dataclass(frozen=True)
class RefundLimits:
    """Hard limits, all integer cents. Pending and succeeded operations count; failed ones do not."""
    per_refund_cents: int = 15_000
    customer_daily_cents: int = 30_000
    customer_daily_count: int = 3
    global_daily_cents: int = 2_000_000


_LIVE = "status IN ('pending', 'succeeded')"
_DAY = "created_at >= datetime('now', '-1 day')"


class OperationStore:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.executescript(SCHEMA)

    def reserve(self, order: dict, amount_cents: int, reason: str, limits: RefundLimits) -> str:
        """Check every limit and insert the pending operation in one write transaction.

        BEGIN IMMEDIATE takes the write lock first, so two concurrent requests cannot both
        pass the check against the same remaining headroom. Raises RefundDenied.
        """
        if isinstance(amount_cents, bool) or not isinstance(amount_cents, int) or amount_cents <= 0:
            raise RefundDenied("Amount must be a whole number of cents, at least 1.")
        if amount_cents > limits.per_refund_cents:
            raise RefundDenied("Refunds above the per-refund limit go to a colleague.")
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            def one(sql: str, *args) -> int:
                return self.conn.execute(sql, args).fetchone()[0]

            on_order = one(f"SELECT COALESCE(SUM(amount_cents), 0) FROM refund_operations "
                           f"WHERE order_id = ? AND {_LIVE}", order["order_id"])
            if on_order + amount_cents > order["total_cents"]:
                raise RefundDenied("Amount exceeds what is left to refund on this order.")
            mine = ("FROM refund_operations r JOIN orders o ON o.order_id = r.order_id "
                    f"WHERE o.customer_id = ? AND r.{_LIVE} AND r.{_DAY}")
            if one(f"SELECT COALESCE(SUM(r.amount_cents), 0) {mine}", order["customer_id"]) + amount_cents \
                    > limits.customer_daily_cents:
                raise RefundDenied("Daily refund limit for this account reached; a colleague will follow up.")
            if one(f"SELECT COUNT(*) {mine}", order["customer_id"]) >= limits.customer_daily_count:
                raise RefundDenied("Daily refund count for this account reached; a colleague will follow up.")
            if one(f"SELECT COALESCE(SUM(amount_cents), 0) FROM refund_operations WHERE {_LIVE} AND {_DAY}") \
                    + amount_cents > limits.global_daily_cents:
                raise RefundDenied("Refunds are paused pending review; a colleague will follow up.")
            op_id = f"op_{uuid.uuid4().hex}"
            self.conn.execute("INSERT INTO refund_operations (op_id, order_id, amount_cents, reason, status) "
                              "VALUES (?, ?, ?, ?, 'pending')", (op_id, order["order_id"], amount_cents, reason))
            self.conn.execute("COMMIT")
            return op_id
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise

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
