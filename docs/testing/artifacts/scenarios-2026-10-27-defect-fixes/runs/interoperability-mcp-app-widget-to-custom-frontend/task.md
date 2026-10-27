We connect our ADK agent to a partner MCP server whose chart tools ship MCP Apps UI. Nothing shows in our React app or in adk web. Make the charts render in our app and keep the model from calling the partner's UI-only refresh tool.

---
Situation (from the person asking): google-adk 2.12.0 with McpToolset (no tool_filter) against a server whose get_chart tool has _meta.ui.resourceUri and whose refresh_chart has _meta.ui.visibility ["app"]; the server registers UI tools only when the client advertises io.modelcontextprotocol/ui. The React app reads ADK events over SSE. No network; nothing installed.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.