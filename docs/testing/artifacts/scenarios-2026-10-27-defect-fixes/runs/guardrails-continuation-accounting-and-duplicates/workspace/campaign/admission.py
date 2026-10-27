"""Whether a stage request may go out."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from campaign.ledger import Ledger


@dataclass(frozen=True)
class Request:
    case_id: str
    stage: str

    @property
    def identity(self) -> str:
        return f"{self.case_id}:{self.stage}"


@dataclass
class Decision:
    allowed: bool
    reason: str
    reserve_cents: int = 0
    approval_id: str | None = None


def load_approvals(folder: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(folder).glob("*.json"))]


def reserve_estimate(ledger: Ledger, config: dict, stage: str) -> int:
    """Conservative cost to hold before sending: the configured reserve, or the dearest charge seen if higher."""
    configured = config["stages"][stage]["reserve_cents"]
    priciest = ledger.priciest_charge(stage)
    return max(configured, priciest) if priciest else configured


def find_approval(ledger: Ledger, config: dict, approvals: list[dict], request: Request, reserve: int) -> dict | None:
    """An approval whose scope names this campaign, stage and case and still has requests and spend left."""
    for approval in approvals:
        scope = approval["scope"]
        if (scope["campaign_id"] != config["campaign_id"] or scope["stage"] != request.stage
                or request.case_id not in scope["case_ids"]):
            continue
        if ledger.approval_uses(approval["approval_id"]) >= scope["max_requests"]:
            continue
        if ledger.approval_spend_cents(approval["approval_id"]) + reserve > scope["max_spend_cents"]:
            continue
        return approval
    return None


def admit(ledger: Ledger, config: dict, approvals: list[dict], request: Request) -> Decision:
    previous = ledger.attempts_for(request.identity)
    if any(a["status"] == "succeeded" for a in previous):
        return Decision(False, "already completed")
    if previous and ledger.has_receipt_for(request.identity):
        return Decision(False, "already paid for: a receipt exists for an earlier attempt; recover its output")
    reserve = reserve_estimate(ledger, config, request.stage)
    approval = None
    if previous or request.case_id not in config["cohort"]:
        approval = find_approval(ledger, config, approvals, request, reserve)
        if approval is None:
            what = "continuation" if previous else "case outside the cohort"
            return Decision(False, f"{what} needs an approval covering this case and stage with requests left")
    envelope = config["envelope"]
    if ledger.sends() >= envelope["max_sends"]:
        return Decision(False, "send limit reached")
    if ledger.remaining_allowance(envelope["spend_cents"]) < reserve:
        return Decision(False, "spending allowance exhausted")
    return Decision(True, "ok", reserve, approval["approval_id"] if approval else None)
