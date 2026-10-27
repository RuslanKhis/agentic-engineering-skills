Expose our ADK research agent as an MCP server for the platform team's hosts, and give us a CI check that proves the server speaks the protocol correctly and tells us when the suite or the SDK moves.

---
Situation (from the person asking): An ADK 2.12 project pinning mcp 2.x, one LlmAgent with two tools, a scripted model available for tests, Node 22 on the CI runner, no cloud credentials.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.