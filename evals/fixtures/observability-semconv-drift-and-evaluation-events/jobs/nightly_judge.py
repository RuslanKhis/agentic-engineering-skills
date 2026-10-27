"""Nightly: score yesterday's sampled conversations with a judge model and store the scores."""
from __future__ import annotations

import datetime as dt

JUDGE_MODEL = "gemini-3.5-pro-001"
TABLE = "support_analytics.judge_scores"


def score_rows(samples: list[dict], judge) -> list[dict]:
    rows = []
    for sample in samples:
        verdict = judge(sample["question"], sample["answer"])
        rows.append({"trace_id": sample["trace_id"], "span_id": sample["span_id"],
                     "metric": "helpfulness", "score": verdict["score"], "label": verdict["label"],
                     "judge_model": JUDGE_MODEL, "scored_at": dt.datetime.now(dt.timezone.utc).isoformat()})
    return rows


def write_rows(rows: list[dict]) -> None:
    from google.cloud import bigquery

    errors = bigquery.Client().insert_rows_json(TABLE, rows)
    if errors:
        raise RuntimeError(errors)
