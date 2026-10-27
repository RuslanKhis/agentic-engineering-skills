"""Offline stand-ins for Model Armor and SDP with the response shapes app.screening reads."""
from __future__ import annotations

import re
from types import SimpleNamespace

from tests.runner import canaries

_PATTERNS = [re.escape(v) for v in canaries.ALL]


class FakeArmor:
    def __init__(self, blocked_phrases=("ignore previous instructions",)):
        self.blocked = blocked_phrases
        self.calls = []

    def sanitize_user_prompt(self, request):
        self.calls.append(request)
        text = request["user_prompt_data"]["text"].lower()
        name = "MATCH_FOUND" if any(p in text for p in self.blocked) else "NO_MATCH_FOUND"
        return SimpleNamespace(sanitization_result=SimpleNamespace(filter_match_state=SimpleNamespace(name=name)))


class FakeDlp:
    """Replaces exactly the known canaries; it knows nothing about other personal data."""

    def __init__(self):
        self.calls = []

    def deidentify_content(self, request):
        self.calls.append(request)
        value = request["item"]["value"]
        for pattern in _PATTERNS:
            value = re.sub(pattern, "[REDACTED]", value)
        return SimpleNamespace(item=SimpleNamespace(value=value))
