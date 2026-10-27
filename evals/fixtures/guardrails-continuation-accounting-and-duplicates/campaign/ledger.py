"""Persistent campaign ledger: attempts, reservations, receipts and the observed provider balance."""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3
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
    def start_attempt(self, identity: str, stage: str) -> str:
        attempt_id = f"a-{uuid.uuid4().hex[:8]}"
        with self.conn:
            self.conn.execute("INSERT INTO attempts (attempt_id, identity, stage, status) VALUES (?, ?, ?, 'dispatched')",
                              (attempt_id, identity, stage))
        return attempt_id

    def finish_attempt(self, attempt_id: str, status: str, error: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE attempts SET status = ?, error = ? WHERE attempt_id = ?",
                              (status, error, attempt_id))

    def attempts_for(self, identity: str) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM attempts WHERE identity = ?", (identity,))]

    def sends(self, stage: str | None = None) -> int:
        sql = "SELECT COUNT(*) FROM attempts WHERE status = 'succeeded'"
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

    def settle(self, receipt: dict) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO receipts VALUES (?, ?, ?)",
                              (receipt["receipt_id"], receipt["reservation_id"], receipt["amount_cents"]))
            self.conn.execute("UPDATE reservations SET state = 'settled' WHERE reservation_id = ?",
                              (receipt["reservation_id"],))

    def settled_cents(self, stage: str | None = None) -> int:
        sql = ("SELECT COALESCE(SUM(rc.amount_cents), 0) FROM receipts rc "
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

    def observed_balance(self) -> dict:
        row = self.conn.execute("SELECT * FROM provider_balance ORDER BY observed_at DESC LIMIT 1").fetchone()
        return dict(row)

    def remaining_allowance(self, envelope_cents: int) -> int:
        """What we can still spend: the envelope less settled charges, capped by the provider's balance."""
        return min(envelope_cents - self.settled_cents(), self.observed_balance()["remaining_cents"])
