# Follow-up questions forget the earlier answer (reported 2026-10-24)

From the service-desk host (old MCP client, `mcp` 1.x): "Triage claim C-881",
then "Why urgency 3?" gets an answer about claim C-881.

From the new host built on the MCP Python client 2.3: the second call answers
"I don't have a previous claim in this conversation". Same server, same day.
Sometimes the old host also forgets after a redeploy.
