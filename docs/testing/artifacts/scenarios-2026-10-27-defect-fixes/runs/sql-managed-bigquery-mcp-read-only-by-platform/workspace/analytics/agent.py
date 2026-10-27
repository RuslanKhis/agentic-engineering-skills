"""The ADK agent the app serves. BigQuery is reached through Google's managed BigQuery MCP server."""
from __future__ import annotations

import os

import google.auth
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.auth.transport.requests import Request

from analytics.mcp_policy import ALLOWED_TOOLS, guard
from analytics.router import route

MODEL = os.environ.get("MODEL_ID", "gemini-3.5-flash")
BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"
BQ_JOB_PROJECT = os.environ.get("BQ_JOB_PROJECT", "fernhill-analytics")

_credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/bigquery"])


def plan_question(question: str) -> dict:
    """Say which path a question takes: a reviewed template, a generated query or a clarification."""
    r = route(question)
    return {"path": r.path, "template": r.template, "domain": r.domain, "reason": r.reason}


def bigquery_headers(_readonly_context) -> dict[str, str]:
    """The runtime service account's own access token, refreshed when it expires; no user token."""
    if not _credentials.valid:
        _credentials.refresh(Request())
    return {"Authorization": f"Bearer {_credentials.token}"}


def pin_job_project(tool, args, tool_context):
    return guard(tool.name, args, BQ_JOB_PROJECT)


bigquery_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=BIGQUERY_MCP_URL, timeout=10.0, sse_read_timeout=240.0),
    tool_filter=ALLOWED_TOOLS,
    header_provider=bigquery_headers,
)

root_agent = LlmAgent(
    name="revenue_analyst",
    model=MODEL,
    description="Answers Fernhill account managers' revenue questions from BigQuery.",
    instruction=(
        "Answer revenue questions for account managers. Call plan_question first. Use the BigQuery "
        "tools to run the query; only ever read data, never create, change or delete anything. "
        "Report numbers exactly as returned."
    ),
    tools=[plan_question, bigquery_tools],
    before_tool_callback=pin_job_project,
)
