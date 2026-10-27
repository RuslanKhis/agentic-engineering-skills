"""Serve the triage agent to MCP hosts over Streamable HTTP.

Conversation state travels as a server-minted `conversation_id` tool argument,
not as an MCP connection. On MCP 2026-07-28 (the default for mcp 2.x clients)
there is no connection, so `to_mcp_server`'s one-session-per-connection
behaviour gives every call a fresh session. The id is the ADK session id; the
session lives in a session service every instance can reach (SESSION_DB_URL),
and is looked up under the caller's principal, so a foreign id is "unknown".
"""
from __future__ import annotations

import os

from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import BaseSessionService, DatabaseSessionService, InMemorySessionService
from google.genai import types
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel

from triage.agent import root_agent

APP_NAME = "warranty_triage_mcp"
LOCAL_PRINCIPAL = "mcp_local"
UNKNOWN = "conversation_id is unknown or expired; omit it to start a new conversation"


class TriageResult(BaseModel):
    conversation_id: str
    answer: str


def _principal() -> str:
    token = get_access_token()  # None on stdio or unauthenticated HTTP
    return f"{token.client_id}|{token.subject}" if token else LOCAL_PRINCIPAL


def default_session_service() -> BaseSessionService:
    url = os.environ.get("SESSION_DB_URL")
    if url:
        return DatabaseSessionService(db_url=url)  # shared by every instance
    return InMemorySessionService()  # single process only: tests, local runs


def build_server(agent: BaseAgent, session_service: BaseSessionService | None = None) -> MCPServer:
    sessions = session_service or default_session_service()
    runner = Runner(app_name=APP_NAME, agent=agent, session_service=sessions)
    server = MCPServer(name=agent.name)

    @server.tool(
        name=agent.name,
        description=(
            f"{agent.description} Send the claim text or follow-up question as `request`. "
            "The result carries a `conversation_id`; pass it back as `conversation_id` on "
            "every follow-up about the same claim, otherwise the agent has no memory of earlier calls."
        ),
        structured_output=True,
    )
    async def triage(request: str, conversation_id: str | None = None) -> TriageResult:
        user_id = _principal()
        if conversation_id is None:
            session = await sessions.create_session(app_name=APP_NAME, user_id=user_id)
        else:
            session = await sessions.get_session(
                app_name=APP_NAME, user_id=user_id, session_id=conversation_id
            )
            if session is None:
                raise ToolError(UNKNOWN)
        answer = ""
        message = types.Content(role="user", parts=[types.Part(text=request)])
        async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
            if event.is_final_response() and event.content and event.content.parts:
                answer = "".join(p.text or "" for p in event.content.parts)
        return TriageResult(conversation_id=session.id, answer=answer)

    return server


server = build_server(root_agent)
app = server.streamable_http_app()

if __name__ == "__main__":
    # stateless_http: no Mcp-Session-Id, so any instance can serve any request.
    server.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        stateless_http=True,
    )
