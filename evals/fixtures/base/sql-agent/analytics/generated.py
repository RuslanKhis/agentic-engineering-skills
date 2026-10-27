"""The generated-query route: metadata, tool-free author, check, expand, execute."""
from __future__ import annotations

from analytics import executor
from analytics.checks import RejectedSQL, check_candidate
from analytics.domains import DOMAINS
from analytics.metadata import collect, expand_derived


def answer(question: str, domain_name: str, run_metadata_query, author_call, bq_client) -> dict:
    """author_call(context, question) -> SQL text or "CANNOT_ANSWER"."""
    context = collect(domain_name, run_metadata_query)
    candidate = author_call(context, question).strip().rstrip(";")
    if candidate == "CANNOT_ANSWER":
        return {"status": "clarify", "message": "That question is outside what I can answer."}
    allowed = set(DOMAINS[domain_name]["tables"]) | set(DOMAINS[domain_name]["derived"])
    try:
        check_candidate(candidate, allowed)
    except RejectedSQL as exc:
        return {"status": "rejected", "message": str(exc)}
    sql = expand_derived(candidate, DOMAINS[domain_name]["derived"])
    return {"status": "ok", "sql": sql, **executor.run(bq_client, sql, [])}
