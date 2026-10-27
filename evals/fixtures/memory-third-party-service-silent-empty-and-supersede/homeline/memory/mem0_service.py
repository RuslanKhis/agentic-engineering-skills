"""ADK memory service backed by Mem0 Platform.

Copied from the Mem0 ADK integration guide (docs/integrations/google-ai-adk)
in June 2026.
"""
from __future__ import annotations

import os

from google.adk.memory.base_memory_service import BaseMemoryService, SearchMemoryResponse
from google.adk.memory.memory_entry import MemoryEntry
from google.genai import types


class Mem0MemoryService(BaseMemoryService):
    def __init__(self, api_key: str | None = None, client=None):
        self._api_key = api_key if api_key is not None else os.environ.get("MEM0_API_KEY", "")
        self._client = client

    def _get_client(self):
        if self._client is None:
            from mem0 import MemoryClient

            self._client = MemoryClient(api_key=self._api_key)
        return self._client

    async def add_session_to_memory(self, session):
        try:
            messages = []
            for event in session.events:
                if not event.content or not event.content.parts:
                    continue
                text = " ".join(part.text for part in event.content.parts if part.text)
                if not text:
                    continue
                role = "user" if event.author == "user" else "assistant"
                messages.append({"role": role, "content": text})
            if messages:
                self._get_client().add(
                    messages,
                    user_id=session.user_id,
                    metadata={"app_id": session.app_name, "session_id": session.id},
                )
        except Exception as e:
            print(f"Error adding session to memory: {e}")

    async def search_memory(self, *, app_name: str, user_id: str, query: str) -> SearchMemoryResponse:
        try:
            results = self._get_client().search(
                query,
                filters={"AND": [{"user_id": user_id}, {"app_id": app_name}]},
                top_k=5,
            )
            memories = []
            for item in results.get("results", []):
                memories.append(MemoryEntry(
                    content=types.Content(role="user", parts=[types.Part(text=item["memory"])]),
                    author="memory",
                    timestamp=item.get("updated_at") or item.get("created_at"),
                ))
            return SearchMemoryResponse(memories=memories)
        except Exception as e:
            print(f"Error searching memory: {e}")
            return SearchMemoryResponse(memories=[])
