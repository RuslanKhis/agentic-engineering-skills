# Triage agent

Classifies inbound warranty claims (product, fault category, urgency) for the
service desk. One ADK root agent.

Tests: `python -m unittest discover -s tests -t .`. google-adk and a2a-sdk are
not installed in this environment; no cloud credentials.

The agent is also exposed to MCP hosts from `triage/mcp_server.py` (Cloud Run
service `warranty-triage-mcp`).
