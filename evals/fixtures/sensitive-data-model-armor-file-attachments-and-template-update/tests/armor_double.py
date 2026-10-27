"""An SDK-shaped double for google.cloud.modelarmor_v1, enough for screening.py. Not the SDK."""
from __future__ import annotations

from enum import Enum
from types import SimpleNamespace


class FilterMatchState(Enum):
    FILTER_MATCH_STATE_UNSPECIFIED = 0
    NO_MATCH_FOUND = 1
    MATCH_FOUND = 2


class DataItem(SimpleNamespace):
    pass


class SanitizeUserPromptRequest(SimpleNamespace):
    pass


sdk = SimpleNamespace(FilterMatchState=FilterMatchState, DataItem=DataItem,
                      SanitizeUserPromptRequest=SanitizeUserPromptRequest)


class FakeArmorClient:
    def __init__(self, state=FilterMatchState.NO_MATCH_FOUND, error: Exception | None = None, empty=False):
        self.state, self.error, self.empty = state, error, empty
        self.requests = []

    def sanitize_user_prompt(self, request):
        self.requests.append(request)
        if self.error:
            raise self.error
        if self.empty:
            return SimpleNamespace(sanitization_result=None)
        return SimpleNamespace(sanitization_result=SimpleNamespace(filter_match_state=self.state))
