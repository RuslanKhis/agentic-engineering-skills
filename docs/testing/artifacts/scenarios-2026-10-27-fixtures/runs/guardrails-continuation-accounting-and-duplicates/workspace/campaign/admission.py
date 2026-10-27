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
    # Never tighten below the configured hold: a cheap past charge does not bound the next one.
    return config["stages"][stage]["reserve_cents"]


def _covering_approval(ledger: Ledger, approvals: list[dict], config: dict, request: Request,
                       reserve: int) -> dict | None:
    """An approval whose scope names this campaign, stage and case and still has requests and spend left."""
    for a in approvals:
        s = a["scope"]
        if (s["campaign_id"] != config["campaign_id"] or s["stage"] != request.stage
                or request.case_id not in s["case_ids"]):
            continue
        ids = {f"{c}:{request.stage}" for c in s["case_ids"]}
        since = a["approved_at"]
        used = ledger.count_attempts(request.stage, ids, since)
        spent = ledger.committed_cents(request.stage, since, ids)
        if used < s["max_requests"] and spent + reserve <= s["max_spend_cents"]:
            return a
    return None


def admit(ledger: Ledger, config: dict, approvals: list[dict], request: Request) -> Decision:
    previous = ledger.attempts_for(request.identity)
    if any(a["status"] == "succeeded" for a in previous) or ledger.has_receipt(request.identity):
        return Decision(False, "already completed or charged")
    if request.stage not in config["stages"]:
        return Decision(False, "unknown stage")
    reserve = reserve_estimate(ledger, config, request.stage)
    if request.case_id not in config["cohort"] or previous:
        if _covering_approval(ledger, approvals, config, request, reserve) is None:
            return Decision(False, "needs an approval covering this case and stage")
    envelope = config["envelope"]
    if ledger.sends() >= envelope["max_sends"]:
        return Decision(False, "send limit reached")
    stage_cfg = config["stages"][request.stage]
    if ledger.sends(request.stage) >= stage_cfg["max_sends"]:
        return Decision(False, "stage send limit reached")
    if ledger.committed_cents(request.stage) + reserve > stage_cfg["spend_cents"]:
        return Decision(False, "stage spending allocation exhausted")
    if ledger.remaining_allowance(envelope["spend_cents"]) < reserve:
        return Decision(False, "spending allowance exhausted")
    return Decision(True, "ok", reserve)
