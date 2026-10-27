"""Recording fakes for every backend. A test asserts on what they recorded, never on model text."""
from __future__ import annotations

from app import backends


class FakeMail:
    def __init__(self, messages: dict[str, dict] | None = None) -> None:
        self.messages = dict(messages or {})
        self.sent: list[dict] = []
        self.deleted: list[str] = []

    def search(self, query):
        return [{"id": k, "from": v["from"], "subject": v["subject"]} for k, v in self.messages.items()
                if query.lower() in (v["subject"] + v["body"]).lower()]

    def read(self, message_id):
        return self.messages[message_id]

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        return f"m{len(self.sent)}"

    def delete(self, message_id):
        self.deleted.append(message_id)


class FakeCalendar:
    def __init__(self, events: dict[str, list[dict]] | None = None) -> None:
        self.events = dict(events or {})
        self.created: list[dict] = []

    def list_events(self, day):
        return self.events.get(day, [])

    def create_event(self, title, start, attendees):
        self.created.append({"title": title, "start": start, "attendees": attendees})
        return f"e{len(self.created)}"


class FakeDrive:
    def __init__(self, files: dict[str, dict] | None = None) -> None:
        self.files = dict(files or {})
        self.shared: list[dict] = []

    def search(self, query):
        return [{"id": k, "name": v["name"]} for k, v in self.files.items() if query.lower() in v["name"].lower()]

    def read(self, file_id):
        return self.files[file_id]["text"]

    def share(self, file_id, email):
        self.shared.append({"file_id": file_id, "email": email})


class FakeBank:
    def __init__(self) -> None:
        self.payments: list[dict] = []

    def pay(self, payee_id, amount_cents, reference):
        self.payments.append({"payee_id": payee_id, "amount_cents": amount_cents, "reference": reference})
        return f"p{len(self.payments)}"


def install(mail=None, calendar=None, drive=None, bank=None) -> backends.Backends:
    wired = backends.Backends(mail or FakeMail(), calendar or FakeCalendar(), drive or FakeDrive(),
                              bank or FakeBank())
    backends.configure(wired)
    return wired


BASE_STATE = {
    "policy:mail_allowlist": ["accounts@larchpine.example", "ops@larchpine.example"],
    "policy:share_domains": ["larchpine.example"],
    "policy:known_payees": ["pay-0042", "pay-0107"],
    "policy:daily_payment_cap_cents": 500_000,
    "payments:today_cents": 0,
}
