"""Process-wide services the tools use. The flow builder configures them; tests configure fakes."""
from __future__ import annotations

from dataclasses import dataclass

from app.clients.helpdesk import HelpdeskClient
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.store import Store


@dataclass
class Services:
    store: Store
    payments: PaymentsClient
    mail: MailClient
    help_index: HelpIndex
    helpdesk: HelpdeskClient | None = None
    max_refund_cents: int = 20_000


_services: Services | None = None


def configure(services: Services) -> None:
    global _services
    _services = services


def get() -> Services:
    if _services is None:
        raise RuntimeError("services are not configured; call app.services.configure() first")
    return _services
