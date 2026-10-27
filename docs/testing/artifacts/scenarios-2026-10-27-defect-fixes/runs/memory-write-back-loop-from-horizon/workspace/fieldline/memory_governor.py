"""Rules for saving, recalling, correcting and erasing engineer memories. No google.adk imports.

Everything here is keyed by the authenticated user_id that the Runner supplies; nothing takes a user id,
consent flag or scope from model arguments. The backend (Memory Bank or in-memory) is reached only through
the `MemoryBackend` protocol so the rules can be tested without the SDK.
"""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Protocol

from fieldline import memory_ledger as L
from fieldline.memory_ledger import MemoryLedger, text_hash

log = logging.getLogger("fieldline.memory")

TOPICS = ("answer_style", "kit", "site_note")  # the whole allowlist; nothing else is ever saved
MAX_FACT_CHARS = 200
MAX_RECALL = 10
SITE_ID = re.compile(r"^[A-Z]{2}-\d{4}$")
# Access codes, credentials and contact details do not belong in a preference memory. Site access
# arrangements live in the site record (get_site), which is the owning source.
_SENSITIVE = re.compile(r"\b(pass(word|code)?|pin|code|token|secret|key|login)\b|\d{4,}|@|https?://", re.I)


class MemoryUnavailable(RuntimeError):
    """The memory service failed. Distinct from an empty result so callers can say so."""


class MemoryBackend(Protocol):
    async def write(self, *, user_id: str, fact_id: str, text: str, session_id: str | None) -> None: ...
    async def search(self, *, user_id: str, query: str) -> list[str]: ...
    async def erase(self, *, user_id: str, text: str) -> None: ...


def validate(topic: str, text: str, site_id: str | None) -> str | None:
    """Return a reason the candidate is refused, or None when it may be staged."""
    if topic not in TOPICS:
        return f"topic must be one of {', '.join(TOPICS)}"
    if not isinstance(text, str) or not text.strip():
        return "empty"
    if len(text) > MAX_FACT_CHARS or "\n" in text or "\r" in text:
        return f"must be one line of at most {MAX_FACT_CHARS} characters"
    if _SENSITIVE.search(text):
        return "looks like a code, credential, number sequence or contact detail; not saved"
    if topic == "site_note":
        if not site_id or not SITE_ID.match(site_id.strip().upper()):
            return "a site note needs a site id such as NW-0417"
    elif site_id:
        return "only site notes carry a site id"
    return None


def fact_id_for(user_id: str, invocation_id: str, call_id: str, topic: str) -> str:
    """Same tool call retried gives the same id, so staging is idempotent."""
    return hashlib.sha256(f"{user_id}|{invocation_id}|{call_id}|{topic}".encode()).hexdigest()[:32]


class MemoryGovernor:
    def __init__(self, ledger: MemoryLedger, backend: MemoryBackend):
        self.ledger = ledger
        self.backend = backend
        self.recall_failures = 0  # exposed so a health check or metric can read it

    # --- consent (called by the application, never by the model) -------------------------
    def grant_consent(self, user_id: str, source: str = "app-settings") -> bool:
        if self.ledger.consent_state(user_id) == "erasing":
            return False  # an earlier erasure has not finished; do not let new writes in behind it
        self.ledger.set_consent(user_id, "granted", source)
        return True

    async def withdraw_consent(self, user_id: str, source: str = "app-settings") -> dict:
        """Stop saving and recalling at once, then erase everything held for this engineer."""
        self.ledger.set_consent(user_id, "erasing", source)
        self.ledger.tombstone_all(user_id)
        result = await self._erase_pending(user_id)
        if result["pending_provider_erase"] == 0:
            self.ledger.set_consent(user_id, "withdrawn", source)
        return result

    # --- save ----------------------------------------------------------------------------
    def stage(self, user_id: str, invocation_id: str, call_id: str, topic: str, text: str,
              site_id: str | None = None, replaces: str | None = None) -> dict:
        if self.ledger.consent_state(user_id) != "granted":
            return {"status": "not_enabled",
                    "message": "Memory is off for this engineer, so nothing was saved. It is turned on in app settings."}
        site = site_id.strip().upper() if site_id else None
        why = validate(topic, text, site)
        if why:
            return {"status": "refused", "message": f"Not saved: {why}."}
        stored = f"At site {site}: {text.strip()}" if site else text.strip()
        fid = fact_id_for(user_id, invocation_id, call_id, topic)
        if not self.ledger.stage(fid, user_id, topic, site, stored, replaces):
            return {"status": "not_enabled", "message": "Memory is off for this engineer, so nothing was saved."}
        return {"status": "staged", "memory_id": fid,
                "message": "Will be saved at the end of this turn. 'List my memories' shows whether it was."}

    async def commit(self, user_id: str, session_id: str | None = None) -> None:
        """Write staged and retryable rows. Called after each turn; never raises into the user's turn."""
        try:
            for row in self.ledger.pending_for_write(user_id):
                await self._write_one(user_id, row, session_id)
            await self._erase_pending(user_id)
        except Exception:  # noqa: BLE001 - a memory problem must not break the reply
            log.exception("memory commit failed for a user; rows stay in the ledger for retry")

    async def _write_one(self, user_id: str, row: dict, session_id: str | None) -> None:
        if not self.ledger.claim(user_id, row["id"]):  # consent withdrawn, erasing, or already taken
            return
        try:
            if not (row["status"] == L.INDETERMINATE and await self._already_there(user_id, row["text"])):
                await self.backend.write(user_id=user_id, fact_id=row["id"], text=row["text"], session_id=session_id)
        except TimeoutError as exc:  # outcome unknown: reconcile by search before any resubmission
            self.ledger.settle(user_id, row["id"], L.INDETERMINATE, type(exc).__name__)
            return
        except Exception as exc:  # noqa: BLE001
            self.ledger.settle(user_id, row["id"], L.FAILED, type(exc).__name__)  # class only: no fact text in logs
            log.warning("memory write failed (%s); will retry on a later turn", type(exc).__name__)
            return
        if not self.ledger.settle(user_id, row["id"], L.ACCEPTED):
            # Forgotten while the write was in flight: the provider copy now exists and must go.
            await self._erase_pending(user_id)
            return
        if row["replaces"]:  # a correction is only effective once the new fact is accepted
            await self.forget(user_id, row["replaces"])

    async def _already_there(self, user_id: str, text: str) -> bool:
        try:
            return any(text_hash(t) == text_hash(text) for t in await self.backend.search(user_id=user_id, query=text))
        except Exception:  # noqa: BLE001
            return False

    # --- recall --------------------------------------------------------------------------
    async def recall(self, user_id: str, query: str) -> list[str]:
        """Facts for this engineer only. Raises MemoryUnavailable on a provider failure, never returns []."""
        if self.ledger.consent_state(user_id) != "granted":
            return []  # not opted in, withdrawn, mid-erasure or stale policy: no recall
        try:
            found = await self.backend.search(user_id=user_id, query=query[:500])
        except Exception as exc:  # noqa: BLE001
            self.recall_failures += 1
            log.warning("memory recall failed (%s)", type(exc).__name__)
            raise MemoryUnavailable(type(exc).__name__) from exc
        gone = self.ledger.forgotten_hashes(user_id)
        return [t[:MAX_FACT_CHARS] for t in found if text_hash(t) not in gone][:MAX_RECALL]

    # --- see, correct, forget ------------------------------------------------------------
    def list_memories(self, user_id: str) -> list[dict]:
        return [{"memory_id": r["id"], "topic": r["topic"], "site_id": r["site_id"], "text": r["text"],
                 "status": r["status"], "saved_on": r["created_at"][:10], "expires_on": r["expires_at"][:10]}
                for r in self.ledger.list_live(user_id)]

    def correct(self, user_id: str, invocation_id: str, call_id: str, memory_id: str, new_text: str) -> dict:
        old = self.ledger.get(user_id, memory_id)  # keyed by user: another engineer's id is simply not found
        if old is None or old["status"] not in L.LIVE:
            return {"status": "not_found", "message": "No such memory."}
        site = old["site_id"]
        body = new_text.strip()
        res = self.stage(user_id, invocation_id, call_id, old["topic"], body, site, replaces=memory_id)
        if res["status"] == "staged":
            res["message"] = "The corrected version replaces the old one once it is saved."
        return res

    async def forget(self, user_id: str, memory_id: str) -> dict:
        row = self.ledger.tombstone(user_id, memory_id)
        if row is None:
            return {"status": "not_found", "message": "No such memory."}
        result = await self._erase_pending(user_id)
        return {"status": "forgotten" if not result["pending_provider_erase"] else "forgotten_pending_provider",
                **result}

    async def _erase_pending(self, user_id: str) -> dict:
        deleted, pending = 0, 0
        for row in self.ledger.to_erase(user_id):
            try:
                await self.backend.erase(user_id=user_id, text=row["text"])
            except Exception as exc:  # noqa: BLE001
                pending += 1
                log.warning("provider erase failed (%s); recall already suppresses it, will retry", type(exc).__name__)
                continue
            self.ledger.mark_erased(user_id, row["id"])
            deleted += 1
        return {"erased": deleted, "pending_provider_erase": pending}

    async def sweep(self, user_id: str) -> None:
        """Periodic job: expire old facts, retry writes, retry provider erases."""
        for row in self.ledger.expired(user_id):
            self.ledger.tombstone(user_id, row["id"])
        await self.commit(user_id)

    async def sweep_all(self) -> None:
        for user_id in self.ledger.users_with_work():
            await self.sweep(user_id)
