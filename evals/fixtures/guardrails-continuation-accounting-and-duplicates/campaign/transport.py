"""Provider transport interface. Production wraps the provider SDK; tests use a counting fake."""
from __future__ import annotations

from typing import Protocol


class NoResponse(Exception):
    """The request left but no answer came back; the provider may still charge for it."""


class ProviderTransport(Protocol):
    def send(self, request_id: str, stage: str, payload: dict) -> dict:
        """Returns {"output": ..., "receipt": {"receipt_id", "amount_cents"}} or raises."""
