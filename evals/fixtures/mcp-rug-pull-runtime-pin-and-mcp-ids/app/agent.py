"""Filings research agent."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
from mcp import StdioServerParameters

ledgerline = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.ledgerline.example/mcp",
        headers={"Authorization": f"Bearer {os.environ.get('LEDGERLINE_TOKEN', '')}"},
    ),
    tool_filter=["search_filings", "get_filing"],
    tool_list_cache_ttl_seconds=None,
)

pdf_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(command="pdf-extract-mcp", args=["--stdio"]),
    ),
)

root_agent = LlmAgent(
    name="filings_research",
    model="gemini-3.5-flash",
    instruction=("Answer analysts' questions about company filings. Find filings with search_filings, "
                 "read them with get_filing, and extract tables from attached PDFs with the PDF tools."),
    tools=[ledgerline, pdf_tools],
)
