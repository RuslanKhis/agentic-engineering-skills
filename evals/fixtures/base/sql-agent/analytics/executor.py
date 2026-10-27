"""Runs SQL on BigQuery: dry run first, then a capped, labelled job."""
from __future__ import annotations

MAX_BYTES_BILLED = 2 * 1024**3  # 2 GiB per query
LABELS = {"app": "fernhill-analytics-agent", "env": "prod"}


class QueryTooLarge(Exception):
    pass


def run(client, sql: str, params: list, max_rows: int = 500) -> dict:
    from google.cloud import bigquery

    dry = client.query(sql, job_config=bigquery.QueryJobConfig(dry_run=True, use_query_cache=False,
                                                               query_parameters=params))
    if dry.total_bytes_processed > MAX_BYTES_BILLED:
        raise QueryTooLarge(f"{dry.total_bytes_processed} bytes")
    job = client.query(sql, job_config=bigquery.QueryJobConfig(
        query_parameters=params, maximum_bytes_billed=MAX_BYTES_BILLED, labels=LABELS))
    rows = [dict(r) for r in job.result(max_results=max_rows + 1)]
    return {"rows": rows[:max_rows], "truncated": len(rows) > max_rows,
            "bytes_billed": job.total_bytes_billed}
