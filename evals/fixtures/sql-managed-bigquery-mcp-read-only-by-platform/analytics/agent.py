"""The ADK agent the app serves. BigQuery is reached through our MCP Toolbox service."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

from analytics.router import route

MODEL = os.environ.get("MODEL_ID", "gemini-3.5-flash")
TOOLBOX_URL = os.environ.get("TOOLBOX_URL", "https://analytics-toolbox-6p2kq3vt4a-nw.a.run.app/mcp")
# ID token for the Toolbox Cloud Run service, minted at start-up by deploy/start.sh.
TOOLBOX_TOKEN = os.environ.get("TOOLBOX_TOKEN", "")


def plan_question(question: str) -> dict:
    """Say which path a question takes: a reviewed template, a generated query or a clarification."""
    r = route(question)
    return {"path": r.path, "template": r.template, "domain": r.domain, "reason": r.reason}


bigquery_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=TOOLBOX_URL,
        headers={"Authorization": f"Bearer {TOOLBOX_TOKEN}"},
    ),
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
)
