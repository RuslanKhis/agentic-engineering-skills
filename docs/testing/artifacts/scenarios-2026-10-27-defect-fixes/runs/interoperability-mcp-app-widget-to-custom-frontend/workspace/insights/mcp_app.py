"""Backend MCP session that declares the MCP Apps extension, and the app-call guard.

ADK 2.12.0's own McpToolset session does not advertise io.modelcontextprotocol/ui, so the
partner serves it text-only tools. This module holds a second session that does, used to
(1) call get_chart for the model, (2) read the ui:// page for the browser, (3) relay
view-initiated tool calls, refusing tools whose visibility lacks "app".
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

PARTNER_URL = os.getenv("PARTNER_MCP_URL", "https://mcp.partner-analytics.example/mcp")
UI_EXTENSION = {"io.modelcontextprotocol/ui": {"mimeTypes": ["text/html;profile=mcp-app"]}}
APP_MIME = "text/html;profile=mcp-app"


def ui_meta(tool_meta: dict | None) -> tuple[str | None, list[str]]:
    """(resourceUri, visibility) from a tool's _meta; visibility defaults to model+app."""
    ui = (tool_meta or {}).get("ui") or {}
    uri = ui.get("resourceUri") or (tool_meta or {}).get("ui/resourceUri")
    return uri, list(ui.get("visibility") or ["model", "app"])


def app_may_call(tool_meta: dict | None) -> bool:
    return "app" in ui_meta(tool_meta)[1]


@asynccontextmanager
async def ui_session():
    """Open and close in the same task (anyio cancel scopes).

    UNVERIFIED: `extensions=` on ClientSession is per the interoperability notes for
    mcp 2.3.0; google-adk is not installed here, so this was not run. Confirm against the
    installed mcp version.
    """
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    async with streamablehttp_client(PARTNER_URL) as (read, write, *_):
        async with ClientSession(read, write, extensions=UI_EXTENSION) as session:
            await session.initialize()
            yield session


async def read_view(resource_uri: str) -> str:
    if not resource_uri.startswith("ui://"):
        raise ValueError("not a ui:// resource")
    async with ui_session() as session:
        result = await session.read_resource(resource_uri)
    content = result.contents[0]
    if getattr(content, "mimeType", None) != APP_MIME:
        raise ValueError(f"unexpected MIME type {getattr(content, 'mimeType', None)!r}")
    return content.text


async def call_tool_for_app(name: str, arguments: dict) -> dict:
    """Relay a view-initiated call; refuse tools the server did not expose to the app."""
    async with ui_session() as session:
        tools = {t.name: t for t in (await session.list_tools()).tools}
        tool = tools.get(name)
        if tool is None or not app_may_call(getattr(tool, "meta", None)):
            raise PermissionError(f"tool {name!r} is not callable from the app")
        result = await session.call_tool(name, arguments)
    return result.model_dump(exclude_none=True, mode="json")


async def get_chart(region: str, months: int | None = None) -> dict:
    """Call get_chart on the UI-capable session; returns the raw result dump."""
    args = {"region": region, **({"months": months} if months else {})}
    async with ui_session() as session:
        result = await session.call_tool("get_chart", args)
    return result.model_dump(exclude_none=True, mode="json")
