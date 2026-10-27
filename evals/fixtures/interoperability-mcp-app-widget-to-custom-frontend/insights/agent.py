"""The sales insights agent with the partner's MCP tools."""
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

partner = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url="https://mcp.partner-analytics.example/mcp"),
)

root_agent = LlmAgent(
    name="sales_insights",
    model="gemini-3.5-flash",
    instruction="Answer sales questions. Show a chart with get_chart when a trend is asked for.",
    tools=[partner],
)
