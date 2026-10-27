"""Run one case through source -> writer -> review -> export, saving a checkpoint per stage."""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path

from pipeline import prompts, stages
from pipeline.checkpoints import CheckpointStore
from pipeline.config import Settings
from pipeline.ledger import CampaignLedger
from pipeline.model import ChatModel
from pipeline.sources import case_spans, load_case, load_policies, manifest, representation
from pipeline.warnings import draft_warnings

# Conservative reservation per call, before the provider reports usage.
RESERVE_USD = {"writer": 0.40, "review": 0.25}


def run_case(case_dir: Path, settings: Settings, writer: ChatModel, reviewer: ChatModel,
             store: CheckpointStore, ledger: CampaignLedger, run_id: str | None = None) -> dict:
    case = load_case(case_dir)
    spans = case_spans(case, load_policies())
    run_id = run_id or f"{case['case_id']}-{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}"
    store.write_manifest(run_id, {"run_id": run_id, "case_id": case["case_id"], "source": manifest(spans),
                                  "writer": {"model": writer.model, "prompt": prompts.WRITER_VERSION},
                                  "review": {"model": reviewer.model, "prompt": prompts.REVIEW_VERSION}})
    store.save(run_id, "source", {"span_ids": [s.span_id for s in spans]}, {"manifest": manifest(spans)})

    ledger.reserve(run_id, "writer", RESERVE_USD["writer"])
    draft, usage = stages.run_writer(writer, case, spans, settings.max_source_chars)
    ledger.settle(run_id, "writer", usage.get("cost_usd", RESERVE_USD["writer"]))
    # Keep what the model saw and what it returned with the checkpoint, for the audit trail.
    frame = representation(spans, settings.max_source_chars)
    store.save(run_id, "writer", draft, {"usage": usage, "attempt": "a1", "frame": frame,
                                         "raw_response": writer.last_response,
                                         "warnings": draft_warnings(draft, spans)})

    ledger.reserve(run_id, "review", RESERVE_USD["review"])
    review, usage = stages.run_review(reviewer, draft, spans, settings.max_source_chars)
    ledger.settle(run_id, "review", usage.get("cost_usd", RESERVE_USD["review"]))
    store.save(run_id, "review", review, {"usage": usage})

    result = stages.export(case, draft, review)
    store.save(run_id, "export", result, {})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    args = parser.parse_args()
    settings = Settings.from_env()
    key = os.environ["PROVIDER_API_KEY"]
    writer = ChatModel(settings.provider_base_url, settings.writer_model, key)
    reviewer = ChatModel(settings.provider_base_url, settings.review_model, key)
    print(run_case(args.case, settings, writer, reviewer,
                   CheckpointStore(settings.checkpoint_dir, settings.checkpoint_limit_bytes),
                   CampaignLedger(settings.ledger_path)))


if __name__ == "__main__":
    main()
