"""Expose the research agent as an MCP server: one tool named after the agent.

    python -m research.mcp_server                                  # stdio
    MCP_TRANSPORT=streamable-http PORT=8000 python -m research.mcp_server

Binds 127.0.0.1 unless HOST is set. The server has no authentication of its own; put it
behind the platform's authenticated edge before binding anything else.
"""
import os

from google.adk.tools.mcp_tool import to_mcp_server

from research.agent import root_agent


def build_server(agent=root_agent):
    # Tool name and description come from the agent; the instruction is not published.
    # Each call is an independent question: on MCP 2026-07-28 there is no connection to
    # hang a conversation on, so no continuity is promised on any revision.
    return to_mcp_server(agent)


def main() -> None:
    server = build_server()
    if os.environ.get("MCP_TRANSPORT", "stdio") == "streamable-http":
        server.run(
            transport="streamable-http",
            host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "8000")),
        )
    else:
        server.run(transport="stdio")


if __name__ == "__main__":
    main()
