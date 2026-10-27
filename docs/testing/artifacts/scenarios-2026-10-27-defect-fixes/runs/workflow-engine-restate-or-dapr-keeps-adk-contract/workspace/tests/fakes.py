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


class DedupingTransport:
    """Payments provider double that honours Idempotency-Key: one effect per key.

    lose_response_first_n: the first N calls take effect, then raise ConnectionError, as when a pod
    dies after the provider accepted the write but before the caller saw the answer.
    """

    def __init__(self, lose_response_first_n: int = 0, fail_status: int | None = None) -> None:
        self.effects: dict[str, dict] = {}
        self.requests: list[dict] = []
        self.lose_left = lose_response_first_n
        self.fail_status = fail_status

    def request(self, method, url, *, json=None, headers=None, timeout=10.0):
        headers = headers or {}
        self.requests.append({"method": method, "url": url, "json": json, "headers": headers})
        if self.fail_status:
            return Response(self.fail_status, {})
        key = headers["Idempotency-Key"]
        self.effects.setdefault(key, json)
        if self.lose_left:
            self.lose_left -= 1
            raise ConnectionError("connection lost after the provider accepted")
        return Response(200, {"id": f"prov_{list(self.effects).index(key) + 1}"})


class FakeApprovals:
    """Approval gateway double: records submissions, answers with a fixed status."""

    def __init__(self, status: str = "pending") -> None:
        self.submitted = []
        self._status = status

    def submit(self, request):
        self.submitted.append(request)
        return self._status


@dataclass
class FakeToolContext:
    """Duck-typed stand-in for the attributes our tool functions read. Not an ADK ToolContext."""
    user_id: str
    state: dict = field(default_factory=dict)


def configure_fakes(payments_responses=None, mail_responses=None,
                    payments_transport=None) -> tuple[Store, FakeTransport, FakeTransport]:
    store = Store(":memory:")
    store.add_order("HO-10442", "cust-ana", "delivered", 8_900, "2026-10-02")
    store.add_order("HO-10518", "cust-ana", "processing", 15_400, "2026-10-20")
    store.add_order("HO-20001", "cust-ben", "delivered", 4_200, "2026-10-11")
    store.upsert_profile("cust-ana", "Ana")
    store.upsert_profile("cust-ben", "Ben")
    pay = payments_transport or FakeTransport(payments_responses)
    mail = FakeTransport(mail_responses)
    services.configure(services.Services(
        store=store,
        payments=PaymentsClient("https://payments.test/v1", pay, "test-key"),
        mail=MailClient("https://mail.test/api", mail),
        help_index=HelpIndex(),
    ))
    return store, pay, mail
