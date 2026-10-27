# Research agent

One ADK agent that answers questions about published papers using two tools.
The platform team wants to call it from their MCP hosts.

Tests: `python -m unittest discover -s tests -t .` runs the tool tests offline.
`tests/test_agent_scripted.py` drives the agent with a scripted model and needs
google-adk installed; it is skipped here, where neither google-adk nor mcp is
installed. No cloud credentials.
