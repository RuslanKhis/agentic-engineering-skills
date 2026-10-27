"""Durable record of what is remembered about each engineer, and who agreed. No google.adk imports.

The ledger is the application's source of truth for consent, for "what do you keep about me" and for
erasure. The memory backend (Memory Bank or in-memory) holds the searchable copy; the ledger says
what that copy is allowed to contain. Every query is keyed by user_id, so one engineer's rows are
unreachable by another's id.
"""
from __future__ import annotations

import hashlib
import os
import sqlite3
import threading
from datetime import datetime, timedelta, timezone

POLICY_VERSION = "2026-10-v1"  # bump to require fresh consent after the policy text changes
RETENTION_DAYS = int(os.environ.get("MEMORY_RETENTION_DAYS", "180"))
MAX_ATTEMPTS = 5

# fact statuses
STAGED, WRITING, ACCEPTED, FAILED, INDETERMINATE = "staged", "writing", "accepted", "failed", "indeterminate"
TOMBSTONED, ERASED = "tombstoned", "erased"  # tombstoned: forgotten, provider copy not yet confirmed gone
LIVE = (STAGED, WRITING, ACCEPTED, FAILED, INDETERMINATE)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS consent (
  user_id TEXT PRIMARY KEY, state TEXT NOT NULL, policy_version TEXT NOT NULL,
  changed_at TEXT NOT NULL, source TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS facts (
  id TEXT PRIMARY KEY, user_id TEXT NOT NULL, topic TEXT NOT NULL, site_id TEXT,
  text TEXT, text_hash TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
  replaces TEXT, created_at TEXT NOT NULL, expires_at TEXT NOT NULL, last_error TEXT);
CREATE INDEX IF NOT EXISTS facts_user ON facts (user_id, status);
"""


def now() -> datetime:
    return datetime.now(timezone.utc)


def text_hash(text: str) -> str:
    return hashlib.sha256(" ".join(text.lower().split()).encode()).hexdigest()


class MemoryLedger:
    def __init__(self, path: str | None = None):
        path = path or os.environ.get("MEMORY_LEDGER_DB", ":memory:")
        self._db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        with self._lock:
            self._db.executescript(_SCHEMA)

    def _q(self, sql: str, args: tuple = ()) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._db.execute(sql, args).fetchall()]

    def _x(self, sql: str, args: tuple = ()) -> int:
        with self._lock:
            return self._db.execute(sql, args).rowcount

    # --- consent -------------------------------------------------------------------------
    def consent_state(self, user_id: str) -> str:
        """'granted' only when the engineer opted in under the current policy version and is not mid-erasure."""
        rows = self._q("SELECT state, policy_version FROM consent WHERE user_id=?", (user_id,))
        if not rows:
            return "none"
        if rows[0]["state"] == "granted" and rows[0]["policy_version"] != POLICY_VERSION:
            return "stale"
        return rows[0]["state"]

    def set_consent(self, user_id: str, state: str, source: str) -> None:
        assert state in ("granted", "withdrawn", "erasing")
        self._x("INSERT INTO consent VALUES (?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET state=excluded.state,"
                " policy_version=excluded.policy_version, changed_at=excluded.changed_at, source=excluded.source",
                (user_id, state, POLICY_VERSION, now().isoformat(), source))

    def consent_record(self, user_id: str) -> dict | None:
        rows = self._q("SELECT * FROM consent WHERE user_id=?", (user_id,))
        return rows[0] if rows else None

    # --- facts ---------------------------------------------------------------------------
    def stage(self, fact_id: str, user_id: str, topic: str, site_id: str | None, text: str,
              replaces: str | None = None) -> bool:
        """Insert a candidate unless consent is not granted. Same fact_id twice is a no-op (retry-safe)."""
        with self._lock:
            if self.consent_state(user_id) != "granted":
                return False
            created = now()
            self._x("INSERT OR IGNORE INTO facts (id,user_id,topic,site_id,text,text_hash,status,replaces,created_at,"
                    "expires_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (fact_id, user_id, topic, site_id, text, text_hash(text), STAGED, replaces,
                     created.isoformat(), (created + timedelta(days=RETENTION_DAYS)).isoformat()))
            return True

    def get(self, user_id: str, fact_id: str) -> dict | None:
        rows = self._q("SELECT * FROM facts WHERE id=? AND user_id=?", (fact_id, user_id))
        return rows[0] if rows else None

    def list_live(self, user_id: str) -> list[dict]:
        marks = ",".join("?" * len(LIVE))
        return self._q(f"SELECT * FROM facts WHERE user_id=? AND status IN ({marks}) ORDER BY created_at, id",
                       (user_id, *LIVE))

    def pending_for_write(self, user_id: str) -> list[dict]:
        return self._q("SELECT * FROM facts WHERE user_id=? AND status IN (?,?,?) AND attempts<? ORDER BY created_at",
                       (user_id, STAGED, FAILED, INDETERMINATE, MAX_ATTEMPTS))

    def claim(self, user_id: str, fact_id: str) -> bool:
        """Atomically take a row for writing; refuses if consent is no longer granted or the row moved on."""
        with self._lock:
            if self.consent_state(user_id) != "granted":
                return False
            return self._x("UPDATE facts SET status=?, attempts=attempts+1 WHERE id=? AND user_id=? AND status IN (?,?,?)",
                           (WRITING, fact_id, user_id, STAGED, FAILED, INDETERMINATE)) == 1

    def settle(self, user_id: str, fact_id: str, status: str, error: str | None = None) -> bool:
        """Record a write outcome. Returns False if the row was forgotten while the write was in flight."""
        return self._x("UPDATE facts SET status=?, last_error=? WHERE id=? AND user_id=? AND status=?",
                       (status, error, fact_id, user_id, WRITING)) == 1

    def tombstone(self, user_id: str, fact_id: str) -> dict | None:
        with self._lock:
            row = self.get(user_id, fact_id)
            if row is None or row["status"] not in LIVE:
                return None
            self._x("UPDATE facts SET status=? WHERE id=? AND user_id=?", (TOMBSTONED, fact_id, user_id))
            return row

    def tombstone_all(self, user_id: str) -> int:
        marks = ",".join("?" * len(LIVE))
        return self._x(f"UPDATE facts SET status=? WHERE user_id=? AND status IN ({marks})", (TOMBSTONED, user_id, *LIVE))

    def to_erase(self, user_id: str) -> list[dict]:
        return self._q("SELECT * FROM facts WHERE user_id=? AND status=?", (user_id, TOMBSTONED))

    def mark_erased(self, user_id: str, fact_id: str) -> None:
        """Provider copy confirmed gone: drop the text, keep a content-free row (hash only) for the audit trail."""
        self._x("UPDATE facts SET status=?, text=NULL WHERE id=? AND user_id=? AND status=?",
                (ERASED, fact_id, user_id, TOMBSTONED))

    def forgotten_hashes(self, user_id: str) -> set[str]:
        return {r["text_hash"] for r in self._q("SELECT text_hash FROM facts WHERE user_id=? AND status IN (?,?)",
                                                (user_id, TOMBSTONED, ERASED))}

    def expired(self, user_id: str, at: datetime | None = None) -> list[dict]:
        return [r for r in self.list_live(user_id) if r["expires_at"] <= (at or now()).isoformat()]

    def users_with_work(self) -> list[str]:
        """Users with live rows (may need expiry or a write retry) or a pending provider erase."""
        rows = self._q("SELECT DISTINCT user_id FROM facts WHERE status IN (?,?,?,?,?,?)", (*LIVE, TOMBSTONED))
        return [r["user_id"] for r in rows]
