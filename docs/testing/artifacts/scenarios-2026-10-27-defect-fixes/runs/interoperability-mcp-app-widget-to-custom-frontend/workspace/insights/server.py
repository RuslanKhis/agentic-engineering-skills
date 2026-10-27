"""SSE endpoint the React app reads; relays ADK events as JSON lines."""
from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel

from insights import mcp_app
from insights.agent import root_agent

CHART_URI = "ui://charts/trend.html"  # from get_chart's _meta.ui.resourceUri (partner/tools-list-with-ui-capability.json)

app = FastAPI()
runner = InMemoryRunner(agent=root_agent, app_name="insights")


class Ask(BaseModel):
    user_id: str
    session_id: str
    text: str


def _widget_lines(event) -> list[str]:
    """One SSE line per chart the show_chart tool staged, in the shape the browser reads."""
    lines = []
    for resp in event.get_function_responses():
        marker = (resp.response or {}).get("_widget")
        if resp.name == "show_chart" and marker:
            # Pass the tool's _meta to the browser only for the resource URI; visibility
            # decisions stay on the server (see /api/mcp_app/call).
            payload = {"id": resp.id, "provider": "mcp", "resource_uri": CHART_URI, **marker}
            lines.append("data: " + json.dumps({"mcp_widget": payload}) + "\n\n")
    return lines


@app.post("/api/run_sse")
async def run_sse(body: Ask):
    async def stream():
        async for event in runner.run_async(user_id=body.user_id, session_id=body.session_id,
                                            new_message=types.Content(role="user", parts=[types.Part(text=body.text)])):
            yield "data: " + event.model_dump_json(exclude_none=True) + "\n\n"
            for line in _widget_lines(event):
                yield line
    return StreamingResponse(stream(), media_type="text/event-stream")


class AppCall(BaseModel):
    name: str
    arguments: dict = {}


# TODO(auth): these two endpoints need the same user/session authorization as /api/run_sse.
@app.get("/api/mcp_app/view")
async def mcp_app_view(uri: str):
    if uri != CHART_URI:  # serve only the page we showed a widget for
        raise HTTPException(404)
    return Response(await mcp_app.read_view(uri), media_type="text/html")


@app.post("/api/mcp_app/call")
async def mcp_app_call(body: AppCall):
    try:
        return await mcp_app.call_tool_for_app(body.name, body.arguments)
    except PermissionError as exc:
        raise HTTPException(403, str(exc))
