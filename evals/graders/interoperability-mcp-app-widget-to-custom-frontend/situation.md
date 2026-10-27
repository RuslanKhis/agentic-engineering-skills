# Situation: interoperability-mcp-app-widget-to-custom-frontend

Standalone project: McpToolset with no tool_filter (`insights/agent.py`); partner docs and two
recorded tools/list results showing get_chart with _meta.ui.resourceUri and refresh_chart with
visibility ["app"] only when the client advertises the UI extension, while our agent receives
text-only tools (A2); the React stream reader keeps only text parts (A1, A4); no backend
resources/read route. A3 (tool_filter dropping tools without "model" visibility; backend refuses
view-initiated calls to tools without "app"). Tests cannot run (no SDK). Context unchanged.
