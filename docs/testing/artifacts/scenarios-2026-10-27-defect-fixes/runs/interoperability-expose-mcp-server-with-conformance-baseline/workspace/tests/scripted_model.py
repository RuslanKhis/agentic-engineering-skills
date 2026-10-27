"""Scripted models for Runner tests. Needs google-adk."""
from __future__ import annotations

from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.genai import types


class ScriptedModel(BaseLlm):
    """Returns queued LlmResponses in order."""
    model: str = "scripted"
    responses: list = []

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        yield self.responses.pop(0)


class FixedTextModel(BaseLlm):
    """Always answers with the same text; never runs out, so it can back a long-lived server."""
    model: str = "fixed-text"
    text: str = "See p-102."

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=self.text)]))


class FailingModel(BaseLlm):
    """Raises on every call, for the agent-exception path."""
    model: str = "failing"

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        raise RuntimeError("scripted model failure")
        yield  # pragma: no cover  (makes this an async generator)
