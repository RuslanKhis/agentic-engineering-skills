"""Serve the triage agent to MCP hosts over Streamable HTTP."""
from __future__ import annotations

import os

from google.adk.tools.mcp_tool import to_mcp_server

from triage.agent import root_agent

server = to_mcp_server(root_agent)
app = server.streamable_http_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
