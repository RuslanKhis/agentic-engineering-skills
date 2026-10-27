"""Deterministic double of the payments provider's refund API (docs/providers/payments-api.md).

It keeps the provider's own ledger of accepted refunds and honours replay keys exactly as
the contract says. A script of per-request behaviours lets a test choose what the client
sees for each POST:

- "ok": accept and answer 201 (or 200 replayed for a known key)
- "timeout_after_accept": accept and commit, then raise TransportTimeout to the caller
- "timeout_before_accept": raise TransportTimeout without committing anything
- an int status (e.g. 503, 402): answer that error without committing
"""
from __future__ import annotations

from app.clients.http import Response, TransportTimeout


class PaymentsProviderDouble:
    def __init__(self, script: list | None = None) -> None:
        self.script = list(script or [])
        self.refunds: list[dict] = []          # what the provider actually committed
        self.by_key: dict[str, dict] = {}
        self.requests: list[dict] = []         # every request the client sent

    def request(self, method, url, *, json=None, headers=None, timeout=10.0):
        headers = headers or {}
        self.requests.append({"method": method, "url": url, "json": json, "headers": dict(headers)})
        if method == "GET" and "/refunds?replay_key=" in url:
            key = url.split("replay_key=", 1)[1]
            found = self.by_key.get(key)
            return Response(200, dict(found)) if found else Response(404, {"error": "not_found"})
        if method != "POST" or not url.endswith("/refunds"):
            return Response(404, {"error": "not_found"})
        behaviour = self.script.pop(0) if self.script else "ok"
        if behaviour == "timeout_before_accept":
            raise TransportTimeout("read timed out")
        if isinstance(behaviour, int):
            return Response(behaviour, {"error": "provider_error"})
        key = headers.get("Replay-Key")
        if key in self.by_key:
            original = self.by_key[key]
            if {k: original[k] for k in ("order_id", "amount_cents", "reason")} != json:
                return Response(409, {"error": "replay_key_mismatch"})
            return Response(200, {**original, "replayed": True})
        refund = {"id": f"re_{len(self.refunds) + 1:04d}", "status": "accepted", **json}
        self.refunds.append(refund)
        if key:
            self.by_key[key] = refund
        if behaviour == "timeout_after_accept":
            raise TransportTimeout("read timed out")
        return Response(201, dict(refund))

    def refunded_cents(self, order_id: str) -> int:
        return sum(r["amount_cents"] for r in self.refunds if r["order_id"] == order_id)
