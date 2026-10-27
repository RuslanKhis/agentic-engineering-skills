"""Process-wide services the tools use. build_agent() configures them; tests configure fakes."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.mail import MailClient
from app.helpdesk import HelpIndex
from app.refund_adapter import RefundAdapter
from app.store import Store


@dataclass
class Services:
    store: Store
    refunds: RefundAdapter
    mail: MailClient
    help_index: HelpIndex
    max_refund_cents: int = 20_000


_services: Services | None = None


def configure(services: Services) -> None:
    global _services
    _services = services


def get() -> Services:
    if _services is None:
        raise RuntimeError("services are not configured; call app.services.configure() first")
    return _services
