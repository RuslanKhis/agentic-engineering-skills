"""The sales insights agent with the partner's MCP tools."""
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

from insights import mcp_app

# Allowlist by name. refresh_chart is app-only (_meta.ui.visibility ["app"]): ADK 2.12.0
# does not apply visibility, so it is excluded here. get_chart is deliberately absent:
# ADK's session is text-only (partner serves get_chart_text to it), and charts go through
# show_chart below, which uses a session that declares the UI extension.
partner = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=mcp_app.PARTNER_URL),
    tool_filter=["get_sales_figures", "get_chart_text"],
)


async def show_chart(region: str, months: int | None = None) -> dict:
    """Show a sales trend chart for a region to the user.

    Args:
        region: Region name.
        months: Number of months to cover (optional).
    """
    result = await mcp_app.get_chart(region, months)
    if result.get("isError"):
        return {"error": "chart unavailable", "detail": result.get("content")}
    # The server (server.py) turns this marker into a widget event for the browser.
    return {
        "status": "chart shown to the user",
        "summary": result.get("content"),
        "_widget": {"tool": "get_chart", "tool_args": {"region": region, **({"months": months} if months else {})}},
    }


root_agent = LlmAgent(
    name="sales_insights",
    model="gemini-3.5-flash",
    instruction=(
        "Answer sales questions. When a trend is asked for, call show_chart; it displays the chart "
        "to the user, so describe the trend briefly instead of repeating the data. If show_chart "
        "fails, use get_chart_text."
    ),
    tools=[partner, show_chart],
)
