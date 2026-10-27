"""Memory write-back controls: consent, fact records, provider outbox, recall filter, correction, erasure.

No google.adk imports so the tests run without the SDK.

The application owns the fact record (this module's store). The memory service (Memory Bank in
deploy) is a derived recall index: a fact is shown to the model only if the engineer's own live,
consented, unexpired record matches what the provider returned, and what the model sees is the
record's text. Scope is always the authenticated user id; a site id is a tag on the fact, never a scope.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import re
import sqlite3
import threading
import uuid
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable, Iterable, Optional, Protocol

log = logging.getLogger(__name__)

POLICY_VERSION = "2026-10-v1"
TOPICS = ("answer_style", "kit", "site_note")
MAX_CHARS = 300
MAX_FACTS_PER_USER = 50
RECALL_MAX_FACTS = 5
RECALL_MAX_CHARS = 800
RECALL_MAX_QUERY = 500
DEFAULT_TTL_DAYS = 180
MAX_SYNC_ATTEMPTS = 5
LIVE_STATES = ("pending", "synced", "failed")

Submit = Callable[[str], Awaitable[None]]
Search = Callable[[str], Awaitable[list]]


class MemoryUnavailable(Exception):
    """The memory service could not be read. Distinct from 'nothing remembered'."""


class Eraser(Protocol):
    async def delete(self, user_id: str, text: str) -> None: ...


class UnsupportedEraser:
    """Default until provider deletion is wired: every delete stays pending, recall stays blocked."""

    async def delete(self, user_id: str, text: str) -> None:
        raise NotImplementedError("provider-side deletion is not wired")


_BLOCKED = [
    ("secret", re.compile(r"(?i)\b(password|passcode|pin|token|secret|api[ _-]?key|gate code|door code|key ?code|combination)\b")),
    ("long_number", re.compile(r"\d{5,}")),
    ("email", re.compile(r"\S+@\S+\.\S+")),
    ("instruction", re.compile(r"(?i)\b(ignore (all |any )?(previous|prior|above)|system prompt|disregard|override)\b")),
]


def screen(text: str) -> tuple[str, Optional[str]]:
    """Return (clean_text, None) or ("", reason). Memory is replayed into later prompts, so it is untrusted input."""
    clean = re.sub(r"\s+", " ", text or "").strip()
    if not clean:
        return "", "empty"
    if len(clean) > MAX_CHARS:
        return "", "too_long"
    if not clean.isprintable():
        return "", "unprintable"
    for reason, pattern in _BLOCKED:
        if pattern.search(clean):
            return "", reason
    return clean, None


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def render(fact: dict) -> str:
    """The exact text submitted to the provider and shown to the model."""
    return f"Site {fact['site_id']}: {fact['text']}" if fact["topic"] == "site_note" else fact["text"]


_SCHEMA = """
CREATE TABLE IF NOT EXISTS consent(
  user_id TEXT NOT NULL, topic TEXT NOT NULL, status TEXT NOT NULL,
  policy_version TEXT NOT NULL, changed_at TEXT NOT NULL, PRIMARY KEY(user_id, topic));
CREATE TABLE IF NOT EXISTS facts(
  fact_id TEXT PRIMARY KEY, user_id TEXT NOT NULL, topic TEXT NOT NULL, site_id TEXT NOT NULL DEFAULT '',
  text TEXT NOT NULL, state TEXT NOT NULL, sent INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0,
  candidate_id TEXT NOT NULL UNIQUE, supersedes TEXT, created_at TEXT NOT NULL, expires_at TEXT NOT NULL,
  updated_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS facts_user ON facts(user_id, state);
CREATE TABLE IF NOT EXISTS audit(
  id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, user_id TEXT NOT NULL, action TEXT NOT NULL,
  fact_id TEXT, outcome TEXT NOT NULL);
"""


class MemoryControls:
    def __init__(self, db_path: str = ":memory:", *, clock: Optional[Callable[[], datetime]] = None,
                 ttl_days: int = DEFAULT_TTL_DAYS, eraser: Optional[Eraser] = None,
                 known_sites: Optional[Iterable[str]] = None, policy_version: str = POLICY_VERSION):
        self._db = sqlite3.connect(db_path, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.executescript(_SCHEMA)
        self._lock = threading.Lock()
        self._user_locks: dict[str, asyncio.Lock] = {}
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._ttl = timedelta(days=ttl_days)
        self._eraser = eraser or UnsupportedEraser()
        self._known_sites = {s.upper() for s in known_sites} if known_sites is not None else None
        self._policy_version = policy_version
        self.metrics: Counter = Counter()

    # -- storage helpers -------------------------------------------------------------------------
    def _now(self) -> str:
        return self._clock().astimezone(timezone.utc).isoformat(timespec="seconds")

    def _run(self, sql: str, params: tuple = ()) -> int:
        with self._lock:
            cur = self._db.execute(sql, params)
            self._db.commit()
            return cur.rowcount

    def _all(self, sql: str, params: tuple = ()) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._db.execute(sql, params).fetchall()]

    def _one(self, sql: str, params: tuple = ()) -> Optional[dict]:
        rows = self._all(sql, params)
        return rows[0] if rows else None

    def _fact(self, fact_id: str) -> Optional[dict]:
        return self._one("SELECT * FROM facts WHERE fact_id=?", (fact_id,))

    def _live(self, user_id: str) -> list[dict]:
        marks = ",".join("?" * len(LIVE_STATES))
        return self._all(f"SELECT * FROM facts WHERE user_id=? AND state IN ({marks}) ORDER BY created_at DESC, rowid DESC",
                         (user_id, *LIVE_STATES))

    def _audit(self, user_id: str, action: str, fact_id: Optional[str], outcome: str) -> None:
        """Content-free: ids, action and outcome only, never fact text."""
        self._run("INSERT INTO audit(at, user_id, action, fact_id, outcome) VALUES (?,?,?,?,?)",
                  (self._now(), user_id, action, fact_id, outcome))

    def _user_lock(self, user_id: str) -> asyncio.Lock:
        return self._user_locks.setdefault(user_id, asyncio.Lock())

    def audit_log(self, user_id: str) -> list[dict]:
        return self._all("SELECT at, action, fact_id, outcome FROM audit WHERE user_id=? ORDER BY id", (user_id,))

    # -- consent ----------------------------------------------------------------------------------
    def grant_consent(self, user_id: str, topics: Iterable[str] = TOPICS) -> None:
        """Call from an authenticated settings surface only; never from a model-callable tool."""
        topics = tuple(topics)
        if not user_id or not topics or any(t not in TOPICS for t in topics):
            raise ValueError("user_id and known topics are required")
        for topic in topics:
            self._set_consent(user_id, topic, "granted")
        self._audit(user_id, "consent_granted", None, ",".join(topics))

    def withdraw_consent(self, user_id: str, topics: Optional[Iterable[str]] = None) -> None:
        """Stops saving and recall at once; unsent candidates are discarded. Saved facts stay until deleted."""
        topics = tuple(topics) if topics is not None else TOPICS
        for topic in topics:
            self._set_consent(user_id, topic, "withdrawn")
            self._run("UPDATE facts SET state='deleted', text='', updated_at=? "
                      "WHERE user_id=? AND topic=? AND state IN ('pending','failed') AND sent=0",
                      (self._now(), user_id, topic))
        self._audit(user_id, "consent_withdrawn", None, ",".join(topics))

    def _set_consent(self, user_id: str, topic: str, status: str) -> None:
        self._run("INSERT INTO consent(user_id, topic, status, policy_version, changed_at) VALUES (?,?,?,?,?) "
                  "ON CONFLICT(user_id, topic) DO UPDATE SET status=excluded.status, "
                  "policy_version=excluded.policy_version, changed_at=excluded.changed_at",
                  (user_id, topic, status, self._policy_version, self._now()))

    def has_consent(self, user_id: str, topic: str) -> bool:
        row = self._one("SELECT status, policy_version FROM consent WHERE user_id=? AND topic=?", (user_id, topic))
        return bool(row) and row["status"] == "granted" and row["policy_version"] == self._policy_version

    def consent_status(self, user_id: str) -> dict:
        return {t: self.has_consent(user_id, t) for t in TOPICS}

    # -- save (stage into the outbox) -------------------------------------------------------------
    def _create(self, user_id: str, topic: str, site_id: str, text: str, candidate_id: str,
                supersedes: Optional[str] = None) -> tuple[str, bool]:
        fact_id = uuid.uuid4().hex
        now = self._clock().astimezone(timezone.utc)
        n = self._run("INSERT OR IGNORE INTO facts(fact_id, user_id, topic, site_id, text, state, candidate_id, supersedes,"
                      " created_at, expires_at, updated_at) VALUES (?,?,?,?,?,'pending',?,?,?,?,?)",
                      (fact_id, user_id, topic, site_id, text, candidate_id, supersedes,
                       now.isoformat(timespec="seconds"), (now + self._ttl).isoformat(timespec="seconds"),
                       now.isoformat(timespec="seconds")))
        if n:
            return fact_id, True
        return self._one("SELECT fact_id FROM facts WHERE candidate_id=?", (candidate_id,))["fact_id"], False

    @staticmethod
    def _candidate(*parts: str) -> str:
        return hashlib.sha256("|".join(parts).encode()).hexdigest()[:32]

    def _check(self, topic: str, text: str, site_id: str) -> tuple[str, str, Optional[str]]:
        clean, reason = screen(text)
        if reason:
            return "", "", reason
        site_id = (site_id or "").strip().upper()
        if topic == "site_note":
            if not site_id or (self._known_sites is not None and site_id not in self._known_sites):
                return "", "", "unknown_site"
        else:
            site_id = ""
        return clean, site_id, None

    def remember(self, user_id: str, topic: str, text: str, *, site_id: str = "",
                 invocation_id: str, function_call_id: str) -> dict:
        """Stage one candidate for the authenticated user. Consent is read here, not taken from the model."""
        if not (user_id and invocation_id and function_call_id):
            return {"status": "error", "reason": "missing_context"}
        if topic not in TOPICS:
            return {"status": "rejected", "reason": "unknown_topic"}
        if not self.has_consent(user_id, topic):
            self._audit(user_id, "remember", None, "no_consent")
            return {"status": "consent_required",
                    "message": "The engineer has not turned on memory for this topic. Do not save it. "
                               "Tell them they can enable it in Fieldline memory settings."}
        candidate = self._candidate(user_id, invocation_id, function_call_id, topic)
        existing = self._one("SELECT fact_id, state FROM facts WHERE candidate_id=?", (candidate,))
        if existing:
            return {"status": "recorded", "fact_id": existing["fact_id"], "duplicate": True}
        clean, site_id, reason = self._check(topic, text, site_id)
        if reason:
            self._audit(user_id, "remember", None, f"rejected:{reason}")
            return {"status": "rejected", "reason": reason}
        live = self._live(user_id)
        for f in live:
            if f["topic"] == topic and f["site_id"] == site_id and _norm(f["text"]) == _norm(clean):
                return {"status": "recorded", "fact_id": f["fact_id"], "duplicate": True}
        if len(live) >= MAX_FACTS_PER_USER:
            return {"status": "rejected", "reason": "limit_reached"}
        fact_id, _ = self._create(user_id, topic, site_id, clean, candidate)
        self._audit(user_id, "remember", fact_id, "staged")
        return {"status": "recorded", "fact_id": fact_id,
                "message": "Saved to the engineer's Fieldline memory; they can review, correct or delete it any time."}

    # -- view -------------------------------------------------------------------------------------
    def list_facts(self, user_id: str) -> list[dict]:
        labels = {"synced": "saved", "pending": "saving", "failed": "not saved yet, will retry"}
        return [{"fact_id": f["fact_id"], "topic": f["topic"], "site_id": f["site_id"], "text": f["text"],
                 "status": labels[f["state"]], "expires_at": f["expires_at"]} for f in self._live(user_id)]

    # -- provider sync (outbox drain) -------------------------------------------------------------
    async def reconcile(self, user_id: str, submit: Submit) -> dict:
        """Push pending/failed facts, then retry pending provider deletions. Never raises into a user turn."""
        report = {"synced": 0, "failed": 0, "skipped": 0, "delete_pending": 0}
        async with self._user_lock(user_id):
            ids = [r["fact_id"] for r in self._all(
                "SELECT fact_id FROM facts WHERE user_id=? AND state IN ('pending','failed') AND attempts<? "
                "ORDER BY created_at, rowid", (user_id, MAX_SYNC_ATTEMPTS))]
            for fid in ids:
                f = self._fact(fid)
                if f is None or f["state"] not in ("pending", "failed"):
                    continue  # deleted or superseded since the scan
                if not self.has_consent(user_id, f["topic"]) or f["expires_at"] <= self._now():
                    if not f["sent"]:
                        self._tombstone(fid)
                    report["skipped"] += 1
                    continue
                self._run("UPDATE facts SET sent=1, updated_at=? WHERE fact_id=?", (self._now(), fid))
                try:
                    await submit(render(f))
                except Exception as exc:  # the write may or may not have landed: sent stays 1
                    self._run("UPDATE facts SET state='failed', attempts=attempts+1, updated_at=? "
                              "WHERE fact_id=? AND state IN ('pending','failed')", (self._now(), fid))
                    self.metrics["write_failed"] += 1
                    log.warning("memory write failed for fact %s: %s", fid, type(exc).__name__)
                    self._audit(user_id, "sync", fid, "failed")
                    report["failed"] += 1
                else:
                    self._run("UPDATE facts SET state='synced', updated_at=? WHERE fact_id=? "
                              "AND state IN ('pending','failed')", (self._now(), fid))
                    self.metrics["write_ok"] += 1
                    self._audit(user_id, "sync", fid, "ok")
                    report["synced"] += 1
            for r in self._all("SELECT fact_id FROM facts WHERE user_id=? AND state='delete_pending'", (user_id,)):
                if not await self._finalize_delete(r["fact_id"]):
                    report["delete_pending"] += 1
        return report

    # -- recall -----------------------------------------------------------------------------------
    async def recall(self, user_id: str, query: str, search: Search) -> list[str]:
        """Return fact texts to show the model. Raises MemoryUnavailable when the provider fails (never [])."""
        allowed = {t for t in TOPICS if self.has_consent(user_id, t)}
        if not allowed or not user_id:
            return []  # no consent: the provider is not even read
        try:
            entries = await search((query or "")[:RECALL_MAX_QUERY])
        except Exception as exc:
            self.metrics["recall_failed"] += 1
            log.warning("memory recall failed: %s", type(exc).__name__)
            raise MemoryUnavailable() from None
        haystack = [_norm(str(e)) for e in entries]
        now = self._now()
        out: list[str] = []
        used = 0
        for f in self._live(user_id):
            if f["topic"] not in allowed or f["expires_at"] <= now:
                continue
            text = render(f)
            if not any(_norm(text) in h for h in haystack):
                continue  # not in the provider's answer, or the provider returned something else
            if len(out) >= RECALL_MAX_FACTS or used + len(text) > RECALL_MAX_CHARS:
                break
            out.append(text)
            used += len(text)
        return out

    # -- correct and delete -----------------------------------------------------------------------
    def _tombstone(self, fact_id: str) -> None:
        self._run("UPDATE facts SET state='deleted', text='', updated_at=? WHERE fact_id=?", (self._now(), fact_id))

    def _mark_delete(self, fact_id: str) -> None:
        """Takes the fact out of recall immediately, before any provider call."""
        self._run("UPDATE facts SET state='delete_pending', updated_at=? WHERE fact_id=? AND state!='deleted'",
                  (self._now(), fact_id))

    async def _finalize_delete(self, fact_id: str) -> bool:
        """Caller holds the user lock. Text is cleared only after the provider confirms."""
        f = self._fact(fact_id)
        if f is None or f["state"] == "deleted":
            return True
        if not f["sent"]:
            self._tombstone(fact_id)
            return True
        try:
            await self._eraser.delete(f["user_id"], render(f))
        except Exception as exc:
            self._run("UPDATE facts SET attempts=attempts+1 WHERE fact_id=?", (fact_id,))
            self.metrics["delete_failed"] += 1
            log.warning("memory delete pending for fact %s: %s", fact_id, type(exc).__name__)
            return False
        self._tombstone(fact_id)
        return True

    def _owned_live(self, user_id: str, fact_id: str) -> Optional[dict]:
        f = self._fact(fact_id)
        if f is None or f["user_id"] != user_id or f["state"] not in LIVE_STATES:
            return None  # same answer for foreign and missing ids
        return f

    async def delete_fact(self, user_id: str, fact_id: str) -> dict:
        if self._owned_live(user_id, fact_id) is None:
            return {"status": "not_found"}
        self._mark_delete(fact_id)
        async with self._user_lock(user_id):
            done = await self._finalize_delete(fact_id)
        self._audit(user_id, "delete", fact_id, "ok" if done else "pending")
        return {"status": "deleted" if done else "delete_pending"}

    async def correct_fact(self, user_id: str, fact_id: str, new_text: str, *,
                           invocation_id: str, function_call_id: str) -> dict:
        old = self._owned_live(user_id, fact_id)
        if old is None:
            return {"status": "not_found"}
        if not (invocation_id and function_call_id):
            return {"status": "error", "reason": "missing_context"}
        if not self.has_consent(user_id, old["topic"]):
            return {"status": "consent_required"}
        candidate = self._candidate(user_id, invocation_id, function_call_id, "correct", fact_id)
        clean, site_id, reason = self._check(old["topic"], new_text, old["site_id"])
        if reason:
            return {"status": "rejected", "reason": reason}
        new_id, created = self._create(user_id, old["topic"], site_id, clean, candidate, supersedes=fact_id)
        if not created:
            return {"status": "corrected", "fact_id": new_id, "duplicate": True}
        self._mark_delete(fact_id)
        async with self._user_lock(user_id):
            done = await self._finalize_delete(fact_id)
        self._audit(user_id, "correct", new_id, "ok" if done else "old_pending")
        return {"status": "corrected", "fact_id": new_id, "old_removed": done}

    async def erase_user(self, user_id: str, *, session_service=None, app_name: Optional[str] = None) -> dict:
        """Withdraw consent first (blocks saving and recall), then delete every fact and the user's sessions.
        Excludes the visit log (a business record) and provider backups; see docs/memory-design.md."""
        self.withdraw_consent(user_id)
        ids = [r["fact_id"] for r in self._all("SELECT fact_id FROM facts WHERE user_id=? AND state!='deleted'", (user_id,))]
        for fid in ids:
            self._mark_delete(fid)
        pending = 0
        async with self._user_lock(user_id):
            for fid in ids:
                if not await self._finalize_delete(fid):
                    pending += 1
        deleted = failed = 0
        if session_service is not None:
            try:
                listed = await session_service.list_sessions(app_name=app_name, user_id=user_id)
                for s in listed.sessions:
                    try:
                        await session_service.delete_session(app_name=app_name, user_id=user_id, session_id=s.id)
                        deleted += 1
                    except Exception:
                        failed += 1
            except Exception:
                failed += 1
        self._audit(user_id, "erase", None, "complete" if not (pending or failed) else "incomplete")
        return {"facts_erased": len(ids) - pending, "facts_pending_provider": pending,
                "sessions_deleted": deleted, "sessions_failed": failed, "complete": not (pending or failed)}

    async def purge_expired(self) -> int:
        """Run from a scheduler. Expired facts are deleted like any other (provider included)."""
        rows = self._all("SELECT fact_id, user_id FROM facts WHERE state IN ('pending','synced','failed') AND expires_at<=?",
                         (self._now(),))
        for r in rows:
            self._mark_delete(r["fact_id"])
        for user_id in {r["user_id"] for r in rows}:
            async with self._user_lock(user_id):
                for r in rows:
                    if r["user_id"] == user_id:
                        await self._finalize_delete(r["fact_id"])
        return len(rows)
