"""Recording fakes for the claim backends."""
from __future__ import annotations

from claims.tools import claims_tools


class FakePayouts:
    def __init__(self):
        self.filed: list[dict] = []

    def file(self, claim_id, amount_cents, payee_account):
        self.filed.append({"claim_id": claim_id, "amount_cents": amount_cents, "payee_account": payee_account})
        return f"po{len(self.filed)}"


class FakeMail:
    def __init__(self):
        self.sent: list[dict] = []

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})


def install(documents: dict[str, str]) -> dict:
    wired = {"documents": dict(documents), "payouts": FakePayouts(), "mail": FakeMail()}
    claims_tools.BACKENDS.clear()
    claims_tools.BACKENDS.update(wired)
    return wired
