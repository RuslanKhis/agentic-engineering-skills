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
CREATE TABLE IF NOT EXISTS preferences (
    user_id TEXT PRIMARY KEY,
    language TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT
);
"""


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

    # preferences: a forgotten row is soft-deleted (deleted_at set) and kept until purged
    def save_language(self, user_id: str, language: str, now: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO preferences (user_id, language, updated_at, deleted_at) "
                              "VALUES (?, ?, ?, NULL) ON CONFLICT(user_id) DO UPDATE SET "
                              "language = excluded.language, updated_at = excluded.updated_at, deleted_at = NULL",
                              (user_id, language, now))

    def get_language(self, user_id: str) -> str | None:
        row = self.conn.execute("SELECT language FROM preferences WHERE user_id = ? AND deleted_at IS NULL",
                                (user_id,)).fetchone()
        return row["language"] if row else None

    def forget_language(self, user_id: str, now: str) -> bool:
        with self.conn:
            cur = self.conn.execute("UPDATE preferences SET deleted_at = ? "
                                    "WHERE user_id = ? AND deleted_at IS NULL", (now, user_id))
        return cur.rowcount > 0

    def purge_forgotten_before(self, cutoff: str) -> int:
        with self.conn:
            cur = self.conn.execute("DELETE FROM preferences WHERE deleted_at IS NOT NULL AND deleted_at < ?",
                                    (cutoff,))
        return cur.rowcount

    def preference_row(self, user_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,)).fetchone()
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
