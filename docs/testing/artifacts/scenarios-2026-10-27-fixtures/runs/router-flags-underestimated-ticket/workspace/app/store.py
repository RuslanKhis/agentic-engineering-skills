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
CREATE TABLE IF NOT EXISTS gmail_connections (
    user_id TEXT PRIMARY KEY,
    provider_account TEXT NOT NULL,
    scopes TEXT NOT NULL,
    secret_ref TEXT,
    status TEXT NOT NULL,
    revision INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS oauth_transactions (
    state_hash TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    browser_hash TEXT NOT NULL,
    code_verifier TEXT NOT NULL,
    redirect_uri TEXT NOT NULL,
    scopes TEXT NOT NULL,
    expires_at INTEGER NOT NULL,
    consumed INTEGER NOT NULL DEFAULT 0
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

    # gmail connections: metadata and a secret reference only, never a token
    def add_oauth_transaction(self, state_hash: str, user_id: str, browser_hash: str,
                              code_verifier: str, redirect_uri: str, scopes: str, expires_at: int) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO oauth_transactions (state_hash, user_id, browser_hash, "
                              "code_verifier, redirect_uri, scopes, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (state_hash, user_id, browser_hash, code_verifier, redirect_uri, scopes,
                               expires_at))

    def consume_oauth_transaction(self, state_hash: str, user_id: str, browser_hash: str,
                                  now: int) -> dict[str, Any] | None:
        """Atomically mark a live transaction used; None unless state, principal and browser all match."""
        with self.conn:
            cur = self.conn.execute(
                "UPDATE oauth_transactions SET consumed = 1 WHERE state_hash = ? AND user_id = ? "
                "AND browser_hash = ? AND consumed = 0 AND expires_at > ?",
                (state_hash, user_id, browser_hash, now))
            if cur.rowcount != 1:
                return None
        row = self.conn.execute("SELECT * FROM oauth_transactions WHERE state_hash = ?",
                                (state_hash,)).fetchone()
        return dict(row)

    def get_gmail_connection(self, user_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM gmail_connections WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def publish_gmail_connection(self, user_id: str, provider_account: str, scopes: str,
                                 secret_ref: str) -> int:
        """Create or replace the user's connection as connected; returns the new revision."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO gmail_connections (user_id, provider_account, scopes, secret_ref, status, "
                "revision) VALUES (?, ?, ?, ?, 'connected', 1) ON CONFLICT(user_id) DO UPDATE SET "
                "provider_account = excluded.provider_account, scopes = excluded.scopes, "
                "secret_ref = excluded.secret_ref, status = 'connected', revision = revision + 1",
                (user_id, provider_account, scopes, secret_ref))
        return self.get_gmail_connection(user_id)["revision"]

    def disconnect_gmail_connection(self, user_id: str) -> dict[str, Any] | None:
        """Block new calls first: status and revision change before any remote cleanup.
        Returns the connection as it was (with its secret_ref) or None if none was connected."""
        before = self.get_gmail_connection(user_id)
        if before is None or before["status"] != "connected":
            return None
        with self.conn:
            self.conn.execute("UPDATE gmail_connections SET status = 'disconnected', revision = revision + 1 "
                              "WHERE user_id = ? AND revision = ?", (user_id, before["revision"]))
        return before

    # refunds
    def record_refund(self, refund_id: str, order_id: str, amount_cents: int,
                      provider_ref: str | None) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO refunds (refund_id, order_id, amount_cents, provider_ref) "
                              "VALUES (?, ?, ?, ?)", (refund_id, order_id, amount_cents, provider_ref))

    def refunds_for(self, order_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM refunds WHERE order_id = ?", (order_id,)).fetchall()
        return [dict(r) for r in rows]
