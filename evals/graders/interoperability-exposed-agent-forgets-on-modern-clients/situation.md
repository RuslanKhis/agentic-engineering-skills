# Situation: interoperability-exposed-agent-forgets-on-modern-clients

Standalone project: `triage/mcp_server.py` serves `to_mcp_server(root_agent)` over streamable HTTP;
mcp pinned 2.3.0; Cloud Run with two instances (minScale=maxScale=2) and no session affinity
(`deploy/service.yaml`) (A1: new client negotiates 2026-07-28, stateless per request -> new ADK
session per call; legacy continuity also breaks across instances without affinity); a scripted
model for tests; CI with Node 22 and no MCP checks (A3 in-process mcp.Client test under default and
legacy modes; A4 pinned Inspector CLI tools/list with --protocol-era, isolated storage, exit codes);
issue note describing the symptom. A2 graded from the answer. Context unchanged.
