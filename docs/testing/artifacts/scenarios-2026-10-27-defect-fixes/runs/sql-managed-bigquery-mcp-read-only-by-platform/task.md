Point our ADK analytics agent at Google's managed BigQuery MCP server instead of running MCP Toolbox ourselves. Security says it must be impossible for the agent to write, whatever the model does. Tell us what to configure and what to test.

---
Situation (from the person asking): An ADK 2.12 agent on Cloud Run with its own service account, McpToolset over streamable HTTP, answers that sometimes aggregate large tables, no network or credentials in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.