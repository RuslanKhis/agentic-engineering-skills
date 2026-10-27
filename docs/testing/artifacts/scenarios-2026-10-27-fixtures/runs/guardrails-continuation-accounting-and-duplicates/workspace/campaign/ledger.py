"""Persistent campaign ledger: attempts, reservations, receipts and the observed provider balance."""
from __future__ import annotations

import json
from datetime import datetime, timezone
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
        started_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self.conn:
            self.conn.execute("INSERT INTO attempts (attempt_id, identity, stage, status, started_at) "
                              "VALUES (?, ?, ?, 'dispatched', ?)", (attempt_id, identity, stage, started_at))
        return attempt_id

    def finish_attempt(self, attempt_id: str, status: str, error: str | None = None) -> None:
        with self.conn:
            self.conn.execute("UPDATE attempts SET status = ?, error = ? WHERE attempt_id = ?",
                              (status, error, attempt_id))

    def attempts_for(self, identity: str) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM attempts WHERE identity = ?", (identity,))]

    def sends(self, stage: str | None = None) -> int:
        """Requests that left the building, whatever their outcome: a lost response was still sent."""
        sql = "SELECT COUNT(*) FROM attempts"
        args: tuple = ()
        if stage:
            sql += " WHERE stage = ?"
            args = (stage,)
        return self.conn.execute(sql, args).fetchone()[0]

    def has_receipt(self, identity: str) -> bool:
        """A provider receipt for any attempt of this identity means it was already charged."""
        return self.conn.execute(
            "SELECT 1 FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            "JOIN attempts a ON a.attempt_id = r.attempt_id WHERE a.identity = ? LIMIT 1",
            (identity,)).fetchone() is not None

    def _attempt_charges(self) -> list[dict]:
        """Per attempt: money committed = distinct receipt amounts + still-open reservations (a lost
        response or interrupted worker may yet be charged, so its hold stays counted)."""
        out = []
        for a in self.conn.execute("SELECT * FROM attempts").fetchall():
            receipts: dict[str, int] = {}
            held = 0
            for r in self.conn.execute("SELECT * FROM reservations WHERE attempt_id = ?", (a["attempt_id"],)):
                if r["state"] == "open":
                    held += r["amount_cents"]
                for rc in self.conn.execute("SELECT * FROM receipts WHERE reservation_id = ?", (r["reservation_id"],)):
                    receipts[rc["receipt_id"]] = rc["amount_cents"]
            out.append({"identity": a["identity"], "stage": a["stage"], "started_at": a["started_at"],
                        "cents": sum(receipts.values()) + held})
        return out

    def committed_cents(self, stage: str | None = None, since: str | None = None,
                        identities: set[str] | None = None) -> int:
        """Settled charges plus open holds. `since` keeps attempts started at/after it (unknown start counts)."""
        return sum(c["cents"] for c in self._attempt_charges()
                   if (stage is None or c["stage"] == stage)
                   and (since is None or c["started_at"] is None or c["started_at"] >= since)
                   and (identities is None or c["identity"] in identities))

    def count_attempts(self, stage: str, identities: set[str], since: str) -> int:
        return sum(1 for a in self.conn.execute("SELECT * FROM attempts WHERE stage = ?", (stage,))
                   if a["identity"] in identities and (a["started_at"] is None or a["started_at"] >= since))

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
        """Record a provider receipt once; a redelivered receipt_id is ignored. Returns whether it was new."""
        if self.conn.execute("SELECT 1 FROM receipts WHERE receipt_id = ?", (receipt["receipt_id"],)).fetchone():
            return False
        if not self.conn.execute("SELECT 1 FROM reservations WHERE reservation_id = ?",
                                 (receipt["reservation_id"],)).fetchone():
            raise ValueError(f"receipt {receipt['receipt_id']} names unknown reservation {receipt['reservation_id']}")
        with self.conn:
            self.conn.execute("INSERT INTO receipts VALUES (?, ?, ?)",
                              (receipt["receipt_id"], receipt["reservation_id"], receipt["amount_cents"]))
            self.conn.execute("UPDATE reservations SET state = 'settled' WHERE reservation_id = ?",
                              (receipt["reservation_id"],))
        return True

    def settled_cents(self, stage: str | None = None) -> int:
        sql = ("SELECT COALESCE(SUM(amount_cents), 0) FROM (SELECT rc.receipt_id, MAX(rc.amount_cents) AS amount_cents "
               "FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
               "JOIN attempts a ON a.attempt_id = r.attempt_id")
        args: tuple = ()
        if stage:
            sql += " WHERE a.stage = ?"
            args = (stage,)
        return self.conn.execute(sql + " GROUP BY rc.receipt_id)", args).fetchone()[0]

    def cheapest_charge(self, stage: str) -> int | None:
        row = self.conn.execute(
            "SELECT MIN(rc.amount_cents) FROM receipts rc JOIN reservations r ON r.reservation_id = rc.reservation_id "
            "JOIN attempts a ON a.attempt_id = r.attempt_id WHERE a.stage = ?", (stage,)).fetchone()
        return row[0]

    def observed_balance(self) -> dict:
        row = self.conn.execute("SELECT * FROM provider_balance ORDER BY observed_at DESC LIMIT 1").fetchone()
        return dict(row)

    def remaining_allowance(self, envelope_cents: int) -> int:
        """What we can still spend: the envelope less settled charges and open holds, capped by the provider
        balance as last observed less everything committed since that observation."""
        balance = self.observed_balance()
        since_observed = self.committed_cents(since=balance["observed_at"])
        return min(envelope_cents - self.committed_cents(), balance["remaining_cents"] - since_observed)
