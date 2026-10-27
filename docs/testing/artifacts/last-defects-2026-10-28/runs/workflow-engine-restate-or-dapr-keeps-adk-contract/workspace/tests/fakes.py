"""Fakes for the providers and the ADK tool context. No SDK, no network."""
from __future__ import annotations

from dataclasses import dataclass, field

from app import services
from app.clients.http import Response
from app.clients.mail import MailClient
from app.clients.payments import PaymentsClient
from app.helpdesk import HelpIndex
from app.store import Store


class FakeTransport:
    """Records every request and answers from a queue of responses (default 200 {})."""

    def __init__(self, responses: list[Response] | None = None) -> None:
        self.responses = list(responses or [])
        self.requests: list[dict] = []

    def request(self, method, url, *, json=None, headers=None, timeout=10.0):
        self.requests.append({"method": method, "url": url, "json": json, "headers": headers or {}})
        if self.responses:
            item = self.responses.pop(0)
            if isinstance(item, Exception):
                raise item
            return item
        return Response(200, {"id": f"prov_{len(self.requests)}"})


class FakeReviews:
    """Records start/wake calls; `fail` makes both raise, like an unreachable review engine."""

    def __init__(self) -> None:
        self.started: list[str] = []
        self.woken: list[str] = []
        self.fail = False

    def start(self, op_id: str) -> None:
        if self.fail:
            raise RuntimeError("engine down")
        self.started.append(op_id)

    def wake(self, op_id: str) -> None:
        if self.fail:
            raise RuntimeError("engine down")
        self.woken.append(op_id)


@dataclass
class FakeToolContext:
    """Duck-typed stand-in for the attributes our tool functions read. Not an ADK ToolContext."""
    user_id: str
    state: dict = field(default_factory=dict)


def configure_fakes(payments_responses=None, mail_responses=None) -> tuple[Store, FakeTransport, FakeTransport]:
    store = Store(":memory:")
    store.add_order("HO-10442", "cust-ana", "delivered", 8_900, "2026-10-02")
    store.add_order("HO-10518", "cust-ana", "processing", 15_400, "2026-10-20")
    store.add_order("HO-20001", "cust-ben", "delivered", 4_200, "2026-10-11")
    store.upsert_profile("cust-ana", "Ana")
    store.upsert_profile("cust-ben", "Ben")
    pay = FakeTransport(payments_responses)
    mail = FakeTransport(mail_responses)
    services.configure(services.Services(
        store=store,
        payments=PaymentsClient("https://payments.test/v1", pay, "test-key"),
        mail=MailClient("https://mail.test/api", mail),
        help_index=HelpIndex(),
        reviews=FakeReviews(),
        manager_emails=frozenset({"mia@harbour.test"}),
    ))
    return store, pay, mail
