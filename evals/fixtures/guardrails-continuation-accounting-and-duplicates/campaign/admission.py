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


def load_approvals(folder: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(Path(folder).glob("*.json"))]


def reserve_estimate(ledger: Ledger, config: dict, stage: str) -> int:
    """Conservative cost to hold before sending; tightened once we have seen real charges."""
    configured = config["stages"][stage]["reserve_cents"]
    cheapest = ledger.cheapest_charge(stage)
    return min(configured, cheapest) if cheapest else configured


def admit(ledger: Ledger, config: dict, approvals: list[dict], request: Request) -> Decision:
    if request.case_id not in config["cohort"]:
        if not any(a["scope"]["campaign_id"] == config["campaign_id"] for a in approvals):
            return Decision(False, "case outside the cohort and no approval")
    previous = ledger.attempts_for(request.identity)
    if any(a["status"] == "succeeded" for a in previous):
        return Decision(False, "already completed")
    if previous and not any(a["scope"]["campaign_id"] == config["campaign_id"] for a in approvals):
        return Decision(False, "continuation needs an approval")
    envelope = config["envelope"]
    if ledger.sends() >= envelope["max_sends"]:
        return Decision(False, "send limit reached")
    reserve = reserve_estimate(ledger, config, request.stage)
    if ledger.remaining_allowance(envelope["spend_cents"]) < reserve:
        return Decision(False, "spending allowance exhausted")
    return Decision(True, "ok", reserve)
