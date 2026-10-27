"""Filings research agent."""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams, StreamableHTTPConnectionParams
from mcp import StdioServerParameters

from app.inventory import pinned_tool_filter

LEDGERLINE_MANIFEST = Path(__file__).resolve().parents[1] / "mcp" / "ledgerline.tools.json"

ledgerline = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.ledgerline.example/mcp",
        headers={"Authorization": f"Bearer {os.environ.get('LEDGERLINE_TOKEN', '')}"},
    ),
    # Allowlist plus runtime hash pin: a tool whose live definition differs from the manifest is withheld.
    tool_filter=pinned_tool_filter(
        json.loads(LEDGERLINE_MANIFEST.read_text()),
        ["search_filings", "get_filing"],
        log=logging.getLogger(__name__),
    ),
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
