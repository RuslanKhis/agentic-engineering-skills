"""Campaign ledger: the approved allowance, what each run reserved and what it was charged."""
from __future__ import annotations

import json
from pathlib import Path


class AllowanceExceeded(Exception):
    pass


class CampaignLedger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    @property
    def allowance_usd(self) -> float:
        return self.data["allowance_usd"]

    def spent_usd(self) -> float:
        return round(sum(e.get("charged_usd") or 0 for e in self.data["entries"]), 4)

    def reserved_usd(self) -> float:
        return round(sum(e["reserved_usd"] for e in self.data["entries"] if e["state"] == "reserved"), 4)

    def remaining_usd(self) -> float:
        return round(self.allowance_usd - self.spent_usd() - self.reserved_usd(), 4)

    def reserve(self, run_id: str, stage: str, amount_usd: float) -> dict:
        if amount_usd > self.remaining_usd():
            raise AllowanceExceeded(f"{run_id}/{stage} needs {amount_usd}, {self.remaining_usd()} left")
        entry = {"run_id": run_id, "stage": stage, "reserved_usd": amount_usd, "charged_usd": None,
                 "state": "reserved"}
        self.data["entries"].append(entry)
        self.save()
        return entry

    def settle(self, run_id: str, stage: str, charged_usd: float) -> None:
        for entry in self.data["entries"]:
            if entry["run_id"] == run_id and entry["stage"] == stage and entry["state"] == "reserved":
                entry["charged_usd"] = charged_usd
                entry["state"] = "settled"
                self.save()
                return
        raise KeyError(f"no open reservation for {run_id}/{stage}")

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=1) + "\n", encoding="utf-8")
