"""What the agent may ask Google's managed BigQuery MCP server to do.

This is the early refusal. The control that makes writes impossible is on the platform: the agent's
IAM roles and the deny policy in deploy/iam.md. Nothing here imports google.adk.
"""
from __future__ import annotations

# Names as the server's tools/list reports them (before any prefix). Never add execute_sql or cancel_job.
ALLOWED_TOOLS = [
    "list_dataset_ids",
    "list_table_ids",
    "get_dataset_info",
    "get_table_info",
    "execute_sql_readonly",
    "get_query_results",
]

# The server runs and bills the job in the project the call names; the model must not choose it.
PROJECT_ARGS = ("project_id", "projectId")


def guard(tool_name: str, args: dict, job_project: str) -> dict | None:
    """Pin the job project in `args` in place; return an error result for a tool outside the allowlist."""
    if tool_name not in ALLOWED_TOOLS:
        return {"error": f"Tool {tool_name!r} is not available to this agent."}
    present = [k for k in PROJECT_ARGS if k in args]
    for key in present or PROJECT_ARGS[:1]:
        args[key] = job_project
    return None
