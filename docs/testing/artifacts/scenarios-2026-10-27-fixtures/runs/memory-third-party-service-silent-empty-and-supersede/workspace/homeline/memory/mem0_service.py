"""ADK memory service backed by Mem0 Platform.

Started from the Mem0 ADK integration guide (June 2026) and changed where the
guide's adapter lost or leaked data:

* Provider failures raise ``Mem0MemoryError`` instead of being printed and turned
  into "no memories", so an outage is not mistaken for an empty memory.
* ``app_id`` is written as an entity field on ``add`` and read inside ``filters``
  on ``search``; the guide wrote it as metadata but filtered on it, which matches
  nothing.
* Recall asks for the current fact only (``latest_only=True``), so a superseded
  address is not returned beside the new one.
* ``erase_user`` deletes a user's memories, verifies by listing, and leaves a
  tombstone that blocks further writes and reads for that user.
"""
from __future__ import annotations

import json
import logging
import os
import threading

# Mem0's erasure telemetry event carries the user id being erased. Must be set
# before ``mem0`` is imported.
os.environ.setdefault("MEM0_TELEMETRY", "False")

from google.adk.memory.base_memory_service import BaseMemoryService, SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry
from google.genai import types

logger = logging.getLogger(__name__)

SEARCH_TOP_K = 5


class Mem0MemoryError(RuntimeError):
    """The Mem0 provider failed or returned something unusable (not 'empty')."""


class Tombstones:
    """Users who asked to be forgotten. Durable when ``path`` is given."""

    def __init__(self, path: str | None = None):
        self._path = path
        self._lock = threading.Lock()
        self._users: set[str] = set()
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self._users = set(json.load(f))

    def add(self, user_id: str) -> None:
        with self._lock:
            self._users.add(user_id)
            if self._path:
                tmp = f"{self._path}.tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(sorted(self._users), f)
                os.replace(tmp, self._path)

    def __contains__(self, user_id: str) -> bool:
        with self._lock:
            return user_id in self._users


class Mem0MemoryService(BaseMemoryService):
    def __init__(self, api_key: str | None = None, client=None, tombstones: Tombstones | None = None):
        self._api_key = api_key if api_key is not None else os.environ.get("MEM0_API_KEY", "")
        self._client = client
        self.tombstones = tombstones if tombstones is not None else Tombstones(
            os.environ.get("HOMELINE_TOMBSTONE_PATH")
        )
        # Counters so an alert can fire on provider failures.
        self.write_failures = 0
        self.search_failures = 0

    def _get_client(self):
        if self._client is None:
            from mem0 import MemoryClient

            self._client = MemoryClient(api_key=self._api_key)
        return self._client

    async def add_session_to_memory(self, session):
        if session.user_id in self.tombstones:
            logger.info("memory write skipped: user has been erased")
            return
        messages = []
        for event in session.events:
            if not event.content or not event.content.parts:
                continue
            text = " ".join(part.text for part in event.content.parts if part.text)
            if not text:
                continue
            role = "user" if event.author == "user" else "assistant"
            messages.append({"role": role, "content": text})
        if not messages:
            return
        try:
            self._get_client().add(
                messages,
                user_id=session.user_id,
                app_id=session.app_name,
                metadata={"session_id": session.id},
            )
        except Exception as e:
            self.write_failures += 1
            logger.error("mem0 write failed (%s)", type(e).__name__, exc_info=True)
            raise Mem0MemoryError("mem0 write failed") from e

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        if user_id in self.tombstones:
            return SearchMemoryResponse(memories=[])
        try:
            results = self._get_client().search(
                query,
                filters={"AND": [{"user_id": user_id}, {"app_id": app_name}]},
                top_k=SEARCH_TOP_K,
                latest_only=True,
            )
        except Exception as e:
            self.search_failures += 1
            logger.error("mem0 search failed (%s)", type(e).__name__, exc_info=True)
            raise Mem0MemoryError("mem0 search failed") from e
        if not isinstance(results, dict) or not isinstance(results.get("results"), list):
            self.search_failures += 1
            logger.error("mem0 search returned an unexpected shape: %s", type(results).__name__)
            raise Mem0MemoryError("mem0 search returned an unexpected response")
        memories = []
        for item in results["results"]:
            text = item.get("memory")
            if not text:
                continue
            memories.append(MemoryEntry(
                content=types.Content(role="user", parts=[types.Part(text=text)]),
                author="memory",
                timestamp=item.get("updated_at") or item.get("created_at"),
            ))
        return SearchMemoryResponse(memories=memories)

    def erase_user(self, user_id: str) -> None:
        """Forget a user: tombstone first, delete their memories, verify by listing.

        Raises ``Mem0MemoryError`` if deletion fails or anything is still listed;
        the tombstone stays so nothing new is written or recalled meanwhile.
        """
        self.tombstones.add(user_id)
        client = self._get_client()
        try:
            client.delete_all(user_id=user_id)
            remaining = client.get_all(filters={"user_id": user_id})
        except Exception as e:
            logger.error("mem0 erasure failed (%s)", type(e).__name__, exc_info=True)
            raise Mem0MemoryError("mem0 erasure failed") from e
        left = remaining.get("results") if isinstance(remaining, dict) else None
        if left is None or len(left) > 0:
            raise Mem0MemoryError("mem0 erasure not confirmed: memories still listed or response unreadable")
