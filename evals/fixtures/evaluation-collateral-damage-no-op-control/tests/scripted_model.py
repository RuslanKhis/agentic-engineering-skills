"""A model double for Runner tests: replays a case's script and records requests."""
from __future__ import annotations

import copy

from google.adk.models import BaseLlm, LlmResponse
from google.genai import types


class ScriptedModel(BaseLlm):
    model: str = "scripted"
    script: list = []
    requests: list = []

    async def generate_content_async(self, llm_request, stream: bool = False):
        self.requests.append(copy.deepcopy(llm_request))
        if not self.script:
            raise AssertionError("scripted model: no response left for this request")
        yield self.script.pop(0)


def script_from(steps: list[dict]) -> list:
    responses = []
    for step in steps:
        if "call" in step:
            part = types.Part(function_call=types.FunctionCall(name=step["call"], args=step["args"]))
        else:
            part = types.Part(text=step["text"])
        responses.append(LlmResponse(content=types.Content(role="model", parts=[part])))
    return responses


def user(text: str) -> types.Content:
    return types.Content(role="user", parts=[types.Part(text=text)])
