"""Serve the research agent as an MCP server: one tool, `paper_research`, taking `request: str`.

    python -m research.mcp_server                 # streamable HTTP on 127.0.0.1:$PORT (default 8000)
    python -m research.mcp_server --stdio

Binds loopback unless MCP_HOST says otherwise. There is no authentication here: put the edge
(IAP, gateway, mTLS) in front before binding anything but loopback.
Every call is one self-contained turn. On spec 2026-07-28 there is no connection, so
`to_mcp_server` cannot keep a conversation across calls; hosts must put the full context in `request`.
"""
from __future__ import annotations

import os
import sys

from google.adk.tools.mcp_tool import to_mcp_server

from research.agent import root_agent

TOOL_NAME = "paper_research"


def build_server():
    return to_mcp_server(root_agent, name=TOOL_NAME)


def main(argv: list[str]) -> None:
    server = build_server()
    if "--stdio" in argv:
        server.run(transport="stdio")
    else:
        server.run(transport="streamable-http", host=os.environ.get("MCP_HOST", "127.0.0.1"),
                   port=int(os.environ.get("PORT", "8000")))


if __name__ == "__main__":
    main(sys.argv[1:])
