"""Persistent campaign ledger: attempts, reservations, receipts and the observed provider balance."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import threading
import uuid

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    attempt_id TEXT PRIMARY KEY,
    identity TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT,
    error TEXT
);
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id TEXT PRIMARY KEY,
    attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
    amount_cents INTEGER NOT NULL,
    state TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS receipts (
    receipt_id TEXT NOT NULL,
    reservation_id TEXT NOT NULL REFERENCES reservations(reservation_id),
    amount_cents INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS approval_uses (
    attempt_id TEXT PRIMARY KEY REFERENCES attempts(attempt_id),
    approval_id TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS provider_balance (
    observed_at TEXT NOT NULL,
    remaining_cents INTEGER NOT NULL,
    source TEXT
);
"""


class Ledger:
    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.lock = threading.RLock()  # held by dispatch across admit -> start_attempt -> reserve

    @classmethod
    def from_seed(cls, seed_path: Path, path: str = ":memory:") -> "Ledger":
        ledger = cls(path)
        seed = json.loads(Path(seed_path).read_text(encoding="utf-8"))
        with ledger.conn:
            for a in seed["attempts"]:
                ledger.conn.execute("INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?)",
                                    (a["attempt_id"], a["identity"], a["stage"], a["status"],
                                     a.get("started_at"), a.get("error")))
            for r in seed["reservations"]:
                ledger.conn.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)",
                                    (r["reservation_id"], r["attempt_id"], r["amount_cents"], r["state"]))
            for rc in seed["receipts"]:
                ledger.conn.execute("INSERT INTO receipts VALUES (?, ?, ?)",
                                    (rc["receipt_id"], rc["reservation_id"], rc["amount_cents"]))
            b = seed["provider_balance"]
            ledger.conn.execute("INSERT INTO provider_balance VALUES (?, ?, ?)",
                                (b["observed_at"], b["remaining_cents"], b.get("source")))
        return ledger

    # attempts
    def start_attempt(self, identity: str, stage: str, approval_id: str | None = None) -> str:
        """Record the attempt (and the approval it consumes) before anything is sent."""
        attempt_id = f"a-{uuid.uuid4().hex[:8]}"
        started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self.conn:
            self.conn.execute("INSERT INTO attempts (attempt_id, identity, stage, status, started_at) "
                              "VALUES (?, ?, ?, 'dispatched', ?)", (attempt_id, identity, stage, started_at))
            if approval_id:
                self.conn.execute("INSERT INTO approval_uses VALUES (?, ?)", (attempt_id, approval_id))
        return attempt_id

    def approval_uses(self, approval_id: str) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM approval_uses WHERE approval_id = ?",
                                 (approval_id,)).fetchone()[0]

    def approval_spend_cents(self, approval_id: str) -> int:
        """Receipts where they exist, otherwise the held reservation, for attempts under this approval."""
        return self.conn.execute(
            "SELECT COALESCE(SUM(COALESCE((SELECT SUM(amount_cents) FROM (SELECT DISTINCT receipt_id, reservation_id, "
            "amount_cents FROM receipts) rc WHERE rc.reservation_id = r.reservation_id), "
            "CASE r.state WHEN 'released' THEN 0 ELSE r.amount_cents END)), 0) "
            "FROM approval_uses u JOIN reservations r ON r.attempt_id = u.attempt_id WHERE u.approval_id = ?",
            (approval_id,)).fetchone()[0]

    def has_receipt_for(self, identity: str) -> bool:
        """True if the provider has charged for any attempt of this identity, whatever its status says."""
        return self.conn.execute(
            "SELECT 1 FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            "JOIN attempts a ON a.attempt_id = r.attempt_id WHERE a.identity = ? LIMIT 1",
            (identity,)).fetchone() is not None

    def finish_attempt(self, attempt_id: str, status: str, error: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE attempts SET status = ?, error = ? WHERE attempt_id = ?",
                              (status, error, attempt_id))

    def attempts_for(self, identity: str) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM attempts WHERE identity = ?", (identity,))]

    def sends(self, stage: str | None = None) -> int:
        """Attempts that may have reached the provider: every attempt, not only the ones that answered."""
        sql = "SELECT COUNT(*) FROM attempts WHERE 1 = 1"
        args: tuple = ()
        if stage:
            sql += " AND stage = ?"
            args = (stage,)
        return self.conn.execute(sql, args).fetchone()[0]

    # money
    def reserve(self, attempt_id: str, amount_cents: int) -> str:
        reservation_id = f"r-{uuid.uuid4().hex[:8]}"
        with self.conn:
            self.conn.execute("INSERT INTO reservations VALUES (?, ?, ?, 'open')",
                              (reservation_id, attempt_id, amount_cents))
        return reservation_id

    def release(self, reservation_id: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE reservations SET state = 'released' WHERE reservation_id = ?",
                              (reservation_id,))

    def settle(self, receipt: dict) -> bool:
        """Record a receipt once. A redelivered receipt is a no-op (False); a conflicting one is an error."""
        key = (receipt["receipt_id"], receipt["reservation_id"], receipt["amount_cents"])
        with self.conn:
            if self.conn.execute("SELECT 1 FROM reservations WHERE reservation_id = ?", (key[1],)).fetchone() is None:
                raise ValueError(f"receipt {key[0]} names unknown reservation {key[1]}")
            existing = self.conn.execute("SELECT reservation_id, amount_cents FROM receipts WHERE receipt_id = ?",
                                         (key[0],)).fetchone()
            if existing:
                if (existing[0], existing[1]) != (key[1], key[2]):
                    raise ValueError(f"receipt {key[0]} redelivered with different contents")
                return False
            self.conn.execute("INSERT INTO receipts VALUES (?, ?, ?)", key)
            self.conn.execute("UPDATE reservations SET state = 'settled' WHERE reservation_id = ?", (key[1],))
        return True

    def open_reserved_cents(self) -> int:
        """Held for attempts that may still be charged (no answer, no receipt yet)."""
        return self.conn.execute("SELECT COALESCE(SUM(amount_cents), 0) FROM reservations "
                                 "WHERE state = 'open'").fetchone()[0]

    def committed_since(self, observed_at: str) -> int:
        """Settled charges plus open holds for attempts started at or after observed_at (unknown start counts)."""
        recent = "(a.started_at IS NULL OR a.started_at >= ?)"
        settled = self.conn.execute(
            "SELECT COALESCE(SUM(rc.amount_cents), 0) FROM (SELECT DISTINCT receipt_id, reservation_id, amount_cents "
            "FROM receipts) rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            f"JOIN attempts a ON a.attempt_id = r.attempt_id WHERE {recent}", (observed_at,)).fetchone()[0]
        held = self.conn.execute(
            "SELECT COALESCE(SUM(r.amount_cents), 0) FROM reservations r JOIN attempts a ON a.attempt_id = r.attempt_id "
            f"WHERE r.state = 'open' AND {recent}", (observed_at,)).fetchone()[0]
        return settled + held

    def settled_cents(self, stage: str | None = None) -> int:
        sql = ("SELECT COALESCE(SUM(rc.amount_cents), 0) FROM "
               "(SELECT DISTINCT receipt_id, reservation_id, amount_cents FROM receipts) rc "
               "JOIN reservations r ON r.reservation_id = rc.reservation_id "
               "JOIN attempts a ON a.attempt_id = r.attempt_id")
        args: tuple = ()
        if stage:
            sql += " WHERE a.stage = ?"
            args = (stage,)
        return self.conn.execute(sql, args).fetchone()[0]

    def cheapest_charge(self, stage: str) -> int | None:
        row = self.conn.execute(
            "SELECT MIN(rc.amount_cents) FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            "JOIN attempts a ON a.attempt_id = r.attempt_id WHERE a.stage = ?", (stage,)).fetchone()
        return row[0]

    def priciest_charge(self, stage: str) -> int | None:
        row = self.conn.execute(
            "SELECT MAX(rc.amount_cents) FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            "JOIN attempts a ON a.attempt_id = r.attempt_id WHERE a.stage = ?", (stage,)).fetchone()
        return row[0]

    def observed_balance(self) -> dict:
        row = self.conn.execute("SELECT * FROM provider_balance ORDER BY observed_at DESC LIMIT 1").fetchone()
        return dict(row)

    def remaining_allowance(self, envelope_cents: int) -> int:
        """What we can still spend: the envelope less settled charges and open holds, capped by the provider's
        balance as last observed less everything committed since that reading (the reading is already stale)."""
        balance = self.observed_balance()
        envelope_left = envelope_cents - self.settled_cents() - self.open_reserved_cents()
        balance_left = balance["remaining_cents"] - self.committed_since(balance["observed_at"])
        return min(envelope_left, balance_left)
