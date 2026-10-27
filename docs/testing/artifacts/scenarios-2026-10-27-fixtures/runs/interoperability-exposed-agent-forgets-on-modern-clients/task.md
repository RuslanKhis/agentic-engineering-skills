We expose our ADK triage agent with to_mcp_server. Follow-up questions worked from our old host, but from the new MCP Python client every call forgets the previous one. Find out why, fix it, and add a CI check that would have caught it.

---
Situation (from the person asking): An ADK 2.12 project with mcp 2.3.0, to_mcp_server over streamable HTTP on Cloud Run with two instances, a scripted model for tests, Node 22 on CI, no cloud credentials in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.