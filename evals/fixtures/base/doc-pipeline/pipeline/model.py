"""OpenAI-compatible chat-completions adapter. The transport is injectable and every send is counted."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Callable

# transport(url, payload, headers, timeout) -> (status_code, body_dict)
Transport = Callable[[str, dict, dict, float], tuple[int, dict]]


class ProviderError(Exception):
    def __init__(self, message: str, status: int | None = None, retryable: bool = False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


def httpx_transport(url: str, payload: dict, headers: dict, timeout: float) -> tuple[int, dict]:
    import httpx  # imported here so tests never need it

    resp = httpx.post(url, json=payload, headers=headers, timeout=timeout)
    return resp.status_code, resp.json()


@dataclass
class ChatModel:
    base_url: str
    model: str
    api_key: str = ""
    transport: Transport = httpx_transport
    temperature: float = 1.0
    max_output_tokens: int = 8192
    timeout_s: float = 120.0
    sends: int = 0
    usage: list[dict] = field(default_factory=list)

    def complete_json(self, instruction: str, schema: dict, schema_name: str) -> tuple[dict, dict]:
        """One paid call. Returns (parsed JSON, usage). The gateway is asked for a JSON schema."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": instruction}],
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
            "response_format": {"type": "json_schema",
                                "json_schema": {"name": schema_name, "schema": schema, "strict": True}},
        }
        self.sends += 1
        status, body = self.transport(f"{self.base_url}/chat/completions", payload,
                                      {"Authorization": f"Bearer {self.api_key}"}, self.timeout_s)
        if status >= 400:
            raise ProviderError(f"provider returned {status}", status, retryable=status in (429, 500, 502, 503))
        usage = body.get("usage", {})
        self.usage.append(usage)
        text = body["choices"][0]["message"]["content"]
        try:
            return json.loads(text), usage
        except ValueError as exc:
            raise ProviderError("response is not JSON") from exc
