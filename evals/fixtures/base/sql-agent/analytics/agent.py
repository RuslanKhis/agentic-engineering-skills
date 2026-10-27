"""The ADK agent the app serves: one tool that answers a revenue question end to end."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.cloud import bigquery

from analytics import executor
from analytics.router import route
from analytics.templates import TEMPLATES, validate_params

MODEL = os.environ.get("MODEL_ID", "gemini-3.5-flash")
_client = bigquery.Client(project=os.environ.get("BQ_JOB_PROJECT", "fernhill-analytics"))


def run_template(name: str, values: dict) -> dict:
    """Run a reviewed template with typed values.

    Args:
        name: One of the reviewed template names.
        values: Parameter values, e.g. {"start_date": "2026-07-01", "end_date": "2026-09-30", "limit": 10}.
    """
    template = TEMPLATES.get(name)
    if template is None:
        return {"status": "error", "message": f"unknown template {name}"}
    errors = validate_params(template, values)
    if errors:
        return {"status": "error", "message": "; ".join(errors)}
    params = [bigquery.ScalarQueryParameter(k, template.params[k], v) for k, v in values.items()]
    return {"status": "ok", **executor.run(_client, template.sql, params)}


def plan_question(question: str) -> dict:
    """Say which path a question takes: a reviewed template, a generated query or a clarification."""
    r = route(question)
    return {"path": r.path, "template": r.template, "domain": r.domain, "reason": r.reason}


root_agent = LlmAgent(
    name="revenue_analyst",
    model=MODEL,
    description="Answers Fernhill account managers' revenue questions from BigQuery.",
    instruction=(
        "Answer revenue questions for account managers. Call plan_question first. For a template "
        "path, call run_template with the parameters from the question. For a clarify path, ask "
        "the question back. Report numbers exactly as returned and say when results are truncated."
    ),
    tools=[plan_question, run_template],
)
