"""Backends the tools call. Production wires Gmail, Calendar, Drive and the bank API; tests wire fakes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class Mail(Protocol):
    def search(self, query: str) -> list[dict]: ...
    def read(self, message_id: str) -> dict: ...
    def send(self, to: str, subject: str, body: str) -> str: ...
    def delete(self, message_id: str) -> None: ...


class Calendar(Protocol):
    def list_events(self, day: str) -> list[dict]: ...
    def create_event(self, title: str, start: str, attendees: list[str]) -> str: ...


class Drive(Protocol):
    def search(self, query: str) -> list[dict]: ...
    def read(self, file_id: str) -> str: ...
    def share(self, file_id: str, email: str) -> None: ...


class Bank(Protocol):
    def pay(self, payee_id: str, amount_cents: int, reference: str) -> str: ...


@dataclass
class Backends:
    mail: Any
    calendar: Any
    drive: Any
    bank: Any


_backends: Backends | None = None


def configure(backends: Backends) -> None:
    global _backends
    _backends = backends


def get() -> Backends:
    if _backends is None:
        raise RuntimeError("backends are not configured")
    return _backends
