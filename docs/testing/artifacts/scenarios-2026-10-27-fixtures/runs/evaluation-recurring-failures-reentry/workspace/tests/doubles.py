"""Scripted provider transport: answers from a queue and counts sends. Never reaches the network."""
from __future__ import annotations

import json


class ScriptedTransport:
    def __init__(self, replies: list) -> None:
        self.replies = list(replies)
        self.sent: list[dict] = []

    def __call__(self, url, payload, headers, timeout):
        self.sent.append({"url": url, "payload": payload})
        if not self.replies:
            raise AssertionError("unexpected provider send")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if isinstance(reply, tuple):
            return reply
        return 200, {"choices": [{"message": {"content": json.dumps(reply)}}],
                     "usage": {"prompt_tokens": 1000, "completion_tokens": 200, "cost_usd": 0.01}}

    @property
    def sends(self) -> int:
        return len(self.sent)


def enum_values_with_line_break(node, path="$") -> list[str]:
    """Paths of enum string values containing a line break (the one rule the 2026-10-22 probe observed)."""
    hits = []
    if isinstance(node, dict):
        hits += [f"{path}.enum" for v in node.get("enum", []) if isinstance(v, str) and "\n" in v]
        for key, value in node.items():
            hits += enum_values_with_line_break(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            hits += enum_values_with_line_break(value, f"{path}[{i}]")
    return hits


class RejectingTransport(ScriptedTransport):
    """ScriptedTransport that answers 400 to a request whose schema has a line-break enum value.

    Models only the rejection recorded in probes/writer-schema-probe-2026-10-22.json. It is not a
    model of the gateway: other schema rules stay unknown until a real send observes them.
    """

    def __call__(self, url, payload, headers, timeout):
        schema = payload["response_format"]["json_schema"]["schema"]
        if enum_values_with_line_break(schema):
            self.sent.append({"url": url, "payload": payload})
            return 400, {"error": {"code": "invalid_request_error", "message": "enum value contains a line break"}}
        return super().__call__(url, payload, headers, timeout)
