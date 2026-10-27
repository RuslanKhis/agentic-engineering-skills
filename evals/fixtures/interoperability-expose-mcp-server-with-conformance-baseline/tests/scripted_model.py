"""A scripted model for Runner tests: returns queued LlmResponses in order. Needs google-adk."""
from __future__ import annotations

from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse


class ScriptedModel(BaseLlm):
    model: str = "scripted"
    responses: list = []

    async def generate_content_async(self, llm_request, stream: bool = False) -> AsyncGenerator[LlmResponse, None]:
        yield self.responses.pop(0)
