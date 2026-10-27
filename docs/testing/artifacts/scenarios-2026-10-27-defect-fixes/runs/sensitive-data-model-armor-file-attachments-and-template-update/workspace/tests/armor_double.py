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


class InvocationResult(Enum):
    INVOCATION_RESULT_UNSPECIFIED = 0
    SUCCESS = 1
    PARTIAL = 2
    FAILURE = 3


class ByteDataItem(SimpleNamespace):
    class ByteItemType(Enum):
        BYTE_ITEM_TYPE_UNSPECIFIED = 0
        PLAINTEXT_UTF8 = 1
        PDF = 2
        WORD_DOCUMENT = 3
        IMAGE = 8


sdk = SimpleNamespace(FilterMatchState=FilterMatchState, DataItem=DataItem,
                      SanitizeUserPromptRequest=SanitizeUserPromptRequest,
                      InvocationResult=InvocationResult, ByteDataItem=ByteDataItem)

ALL_FILTERS = {"rai": 1, "pi_and_jailbreak": 1, "malicious_uris": 1, "sdp": 1}


class FakeArmorClient:
    def __init__(self, state=FilterMatchState.NO_MATCH_FOUND, error: Exception | None = None, empty=False,
                 invocation=InvocationResult.SUCCESS, filter_results=None):
        self.state, self.error, self.empty = state, error, empty
        self.invocation = invocation
        self.filter_results = dict(ALL_FILTERS) if filter_results is None else filter_results
        self.requests = []
        self.kwargs = []

    def sanitize_user_prompt(self, request, **kwargs):
        self.requests.append(request)
        self.kwargs.append(kwargs)
        if self.error:
            raise self.error
        if self.empty:
            return SimpleNamespace(sanitization_result=None)
        return SimpleNamespace(sanitization_result=SimpleNamespace(
            filter_match_state=self.state, invocation_result=self.invocation,
            filter_results=self.filter_results))
