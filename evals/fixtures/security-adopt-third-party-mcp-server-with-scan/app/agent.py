"""Dispatch assistant with Freightline's MCP server."""
from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

FREIGHTLINE_PACKAGE = "@freightline/shipping-mcp@3.4.1"
FREIGHTLINE_TOOLS = ["get_rates", "create_shipment", "track_shipment"]

freightline = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", FREIGHTLINE_PACKAGE],
            env={"FREIGHTLINE_API_KEY": os.environ.get("FREIGHTLINE_API_KEY", "")},
        ),
        timeout=15,
    ),
    tool_filter=FREIGHTLINE_TOOLS,
)

root_agent = LlmAgent(
    name="dispatch_assistant",
    model="gemini-3.5-flash",
    instruction="Quote and book parcel shipments for warehouse staff. Book only when asked to.",
    tools=[freightline],
)
