# Adopting a third-party MCP server

Every MCP server we did not write goes through these steps before an agent may use it. The
security owner (Priya) signs off the last step.

1. **Need and owner.** Name the tools we need and the engineer who owns the integration.
2. **Read the server command.** Review the package or image, what it starts, what it reads from
   the environment and which network destinations it calls. Record the review in the PR.
3. **Pin.** Pin the exact package version (`@scope/name@x.y.z`) or image digest; never `latest`.
4. **Allow-list.** Set `tool_filter` to the tools from step 1; nothing else is exposed to the model.
5. **Record definitions.** Commit the listed tool definitions with their hashes under `mcp/`
   (`app/mcp_pin.py` computes them).
6. **Definition check in CI.** `scripts/check_mcp_definitions.py` fails the build on any added,
   removed or changed tool.
7. **Credentials.** The server gets only its own scoped key from Secret Manager, never the
   agent's service-account credentials.
8. **Sign-off.** Security owner approves the PR.
