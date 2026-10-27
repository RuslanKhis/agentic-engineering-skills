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
