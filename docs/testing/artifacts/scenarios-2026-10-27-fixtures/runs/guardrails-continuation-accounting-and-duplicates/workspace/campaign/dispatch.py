"""Admission, reservation, send and settlement for one stage request."""
from __future__ import annotations

from campaign.admission import Decision, Request, admit
from campaign.ledger import Ledger
from campaign.transport import NoResponse, ProviderTransport


def dispatch(ledger: Ledger, config: dict, approvals: list[dict], transport: ProviderTransport,
             request: Request, payload: dict) -> Decision:
    decision = admit(ledger, config, approvals, request)
    if not decision.allowed:
        return decision
    attempt_id = ledger.start_attempt(request.identity, request.stage)
    reservation_id = ledger.reserve(attempt_id, decision.reserve_cents)
    try:
        result = transport.send(attempt_id, request.stage, payload)
    except NoResponse as exc:
        # The provider may still charge for it: keep the hold until a receipt or a human settles it.
        ledger.finish_attempt(attempt_id, "no_response", str(exc))
        return Decision(False, "no response")
    except Exception as exc:
        ledger.finish_attempt(attempt_id, "failed", str(exc))
        ledger.release(reservation_id)
        return Decision(False, "failed")
    receipt = dict(result["receipt"], reservation_id=reservation_id)
    ledger.settle(receipt)
    ledger.finish_attempt(attempt_id, "succeeded")
    return decision


def apply_late_receipts(ledger: Ledger, receipts: list[dict]) -> None:
    for receipt in receipts:
        ledger.settle(receipt)  # idempotent on receipt_id; redelivery is ignored


def load_receipts(path) -> list[dict]:
    from pathlib import Path
    import json
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
