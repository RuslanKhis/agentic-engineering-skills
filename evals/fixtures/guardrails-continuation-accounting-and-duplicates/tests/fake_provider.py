"""Counting fake of the provider transport. Never touches the network."""
from __future__ import annotations

from campaign.transport import NoResponse


class CountingTransport:
    """Each send is counted; outcomes come from a script: "ok", "no_response" or an exception."""

    def __init__(self, script=None, charge_cents: int = 50) -> None:
        self.script = list(script or [])
        self.charge_cents = charge_cents
        self.sends: list[dict] = []

    def send(self, request_id, stage, payload):
        self.sends.append({"request_id": request_id, "stage": stage, "payload": payload})
        outcome = self.script.pop(0) if self.script else "ok"
        if outcome == "no_response":
            raise NoResponse("read timeout")
        if isinstance(outcome, Exception):
            raise outcome
        return {"output": {"text": "ok"},
                "receipt": {"receipt_id": f"rc-{len(self.sends):04d}", "amount_cents": self.charge_cents}}
