"""SQLite store for orders, customer profiles and refunds."""
from __future__ import annotations

import sqlite3
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    placed_on TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
    user_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS refunds (
    refund_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    amount_cents INTEGER NOT NULL,
    provider_ref TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS refund_ops (
    op_id TEXT PRIMARY KEY,
    base_key TEXT NOT NULL,
    generation INTEGER NOT NULL,
    customer_id TEXT NOT NULL,
    order_id TEXT NOT NULL REFERENCES orders(order_id),
    amount_cents INTEGER NOT NULL,
    reason TEXT NOT NULL,
    state TEXT NOT NULL,
    approver TEXT,
    provider_ref TEXT,
    refund_id TEXT,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    decided_at TEXT,
    UNIQUE (base_key, generation)
);
"""

# A refund operation moves pending -> approved | rejected | expired; approved -> executing ->
# completed | failed | outcome_unknown. Rejected and expired operations let the customer ask again.
REOPENABLE = ("rejected", "expired")


class Store:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    # orders
    def add_order(self, order_id: str, customer_id: str, status: str, total_cents: int,
                  placed_on: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                              (order_id, customer_id, status, total_cents, placed_on))

    def get_order(self, order_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
        return dict(row) if row else None

    def orders_for(self, customer_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM orders WHERE customer_id = ? ORDER BY placed_on DESC",
                                 (customer_id,)).fetchall()
        return [dict(r) for r in rows]

    # profiles
    def upsert_profile(self, user_id: str, display_name: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO profiles (user_id, display_name) VALUES (?, ?) "
                              "ON CONFLICT(user_id) DO UPDATE SET display_name = excluded.display_name",
                              (user_id, display_name))

    def get_profile(self, user_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    # refunds
    def record_refund(self, refund_id: str, order_id: str, amount_cents: int,
                      provider_ref: str | None) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO refunds (refund_id, order_id, amount_cents, provider_ref) "
                              "VALUES (?, ?, ?, ?)", (refund_id, order_id, amount_cents, provider_ref))

    def refunds_for(self, order_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM refunds WHERE order_id = ?", (order_id,)).fetchall()
        return [dict(r) for r in rows]

    # refund operations: the durable review record. Every transition is a conditional UPDATE, so
    # of two competing writers exactly one wins and the other reads the winner's state.
    def get_refund_op(self, op_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM refund_ops WHERE op_id = ?", (op_id,)).fetchone()
        return dict(row) if row else None

    def create_refund_op(self, base_key: str, customer_id: str, order_id: str, amount_cents: int,
                         reason: str, now: str, expires_at: str) -> tuple[dict[str, Any], bool]:
        """Return (operation, created). A repeat of a live or finished request returns the existing
        operation; only a rejected or expired one is followed by a new generation."""
        latest = self.conn.execute(
            "SELECT * FROM refund_ops WHERE base_key = ? ORDER BY generation DESC LIMIT 1",
            (base_key,)).fetchone()
        if latest is not None and latest["state"] not in REOPENABLE:
            return dict(latest), False
        generation = (latest["generation"] + 1) if latest is not None else 1
        op_id = f"{base_key}-{generation}"
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO refund_ops (op_id, base_key, generation, customer_id, order_id, "
                    "amount_cents, reason, state, created_at, expires_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)",
                    (op_id, base_key, generation, customer_id, order_id, amount_cents, reason, now, expires_at))
        except sqlite3.IntegrityError:  # a competing request inserted this generation first
            return self.get_refund_op(op_id), False
        return self.get_refund_op(op_id), True

    def _transition(self, op_id: str, sql: str, params: tuple) -> dict[str, Any]:
        with self.conn:
            self.conn.execute(sql, params)
        return self.get_refund_op(op_id)

    def decide_refund_op(self, op_id: str, approved: bool, approver: str, now: str) -> dict[str, Any]:
        """pending -> approved | rejected while unexpired; otherwise the current state is returned."""
        return self._transition(
            op_id,
            "UPDATE refund_ops SET state = ?, approver = ?, decided_at = ? "
            "WHERE op_id = ? AND state = 'pending' AND expires_at > ?",
            ("approved" if approved else "rejected", approver, now, op_id, now))

    def expire_refund_op(self, op_id: str, now: str) -> dict[str, Any]:
        return self._transition(
            op_id, "UPDATE refund_ops SET state = 'expired', decided_at = ? "
                   "WHERE op_id = ? AND state = 'pending' AND expires_at <= ?", (now, op_id, now))

    def claim_refund_op(self, op_id: str) -> dict[str, Any] | None:
        """approved -> executing. An operation already executing is returned too: the engine re-runs
        the step after a crash and the provider key makes the repeat safe. None when not approved."""
        op = self._transition(op_id, "UPDATE refund_ops SET state = 'executing' "
                                     "WHERE op_id = ? AND state = 'approved'", (op_id,))
        return op if op and op["state"] == "executing" else None

    def finish_refund_op(self, op_id: str, state: str, provider_ref: str | None = None,
                         refund_id: str | None = None) -> dict[str, Any]:
        """executing -> completed | failed | outcome_unknown; completion also writes the refunds row."""
        with self.conn:
            cur = self.conn.execute(
                "UPDATE refund_ops SET state = ?, provider_ref = ?, refund_id = ? "
                "WHERE op_id = ? AND state = 'executing'", (state, provider_ref, refund_id, op_id))
            if cur.rowcount and state == "completed":
                op = self.get_refund_op(op_id)
                self.conn.execute("INSERT INTO refunds (refund_id, order_id, amount_cents, provider_ref) "
                                  "VALUES (?, ?, ?, ?)", (refund_id, op["order_id"], op["amount_cents"], provider_ref))
        return self.get_refund_op(op_id)
