Platform wants every third-party MCP server scanned with Snyk Agent Scan before we adopt it. Add the scan to our adoption checklist and CI without weakening what we already do.

---
Situation (from the person asking): An ADK 2.12 agent adopting a vendor's stdio MCP server, CI with containers, a Snyk token in CI secrets, no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.