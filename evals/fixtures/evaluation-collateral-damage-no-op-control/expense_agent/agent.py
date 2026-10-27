"""Builds the expense agent with its database tools and two MCP toolsets."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

from expense_agent import db, tools

INSTRUCTION = """You file expense claims for employees. Read the receipt the employee names from
the receipts folder, check the category limit, and file the claim. If the amount is over the
limit, open an approval issue in the finance repository for the employee's approver."""

receipts = McpToolset(connection_params=StdioConnectionParams(server_params=StdioServerParameters(
    command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/srv/receipts"])),
    tool_filter=["read_file", "list_directory"])

github = McpToolset(connection_params=StdioConnectionParams(server_params=StdioServerParameters(
    command="docker", args=["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                            "ghcr.io/github/github-mcp-server:v0.9"],
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": os.environ.get("FINANCE_GITHUB_TOKEN", "")})),
    tool_filter=["create_issue"])

tools.use_connection(db.connect(os.environ.get("EXPENSES_DB", "expenses.db")))

root_agent = LlmAgent(
    name="expense_agent",
    model=os.environ.get("MODEL_ID", "gemini-3.5-flash"),
    instruction=INSTRUCTION,
    tools=[tools.get_policy_limit, tools.file_expense, tools.get_my_profile, tools.update_profile,
           tools.list_my_expenses, receipts, github],
)
