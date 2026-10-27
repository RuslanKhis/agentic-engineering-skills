"""The generated-query route: metadata, tool-free author, check, expand, execute."""
from __future__ import annotations

from analytics import executor
from analytics.checks import RejectedSQL, check_candidate
from analytics.domains import DOMAINS
from analytics.metadata import collect, expand_derived


def answer(question: str, domain_name: str, run_metadata_query, author_call, bq_client,
           on_success=None) -> dict:
    """author_call(context, question) -> SQL text or "CANNOT_ANSWER".

    on_success(domain_name, candidate_sql), if given, queues the query for review. It must not
    make the example visible to the author; only reviewed examples do.
    """
    context = collect(domain_name, run_metadata_query)
    candidate = author_call(context, question).strip().rstrip(";")
    if candidate == "CANNOT_ANSWER":
        return {"status": "clarify", "message": "That question is outside what I can answer."}
    domain = DOMAINS[domain_name]
    try:
        check_candidate(candidate, set(domain["tables"]) | set(domain["derived"]))
        sql = expand_derived(candidate, domain["derived"])
        # A derived name the expansion missed would reach BigQuery as an unknown table.
        check_candidate(sql, set(domain["tables"]))
    except RejectedSQL as exc:
        return {"status": "rejected", "message": str(exc)}
    result = {"status": "ok", "sql": sql, **executor.run(bq_client, sql, [])}
    if on_success is not None:
        on_success(domain_name, candidate)
    return result
