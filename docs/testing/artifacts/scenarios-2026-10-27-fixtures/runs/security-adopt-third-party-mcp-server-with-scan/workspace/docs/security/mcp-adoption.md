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
8. **Snyk Agent Scan.** Platform requires it for every third-party server. Keep
   `mcp-scan/<server>.json` with exactly the agent's command and arguments and no credentials
   (`tests/test_mcp_scan_config.py` asserts it equals the command in `app/agent.py`). The CI job
   `mcp-scan` runs the pinned `snyk-agent-scan` with `scan --ci --dangerously-run-mcp-servers` in
   an ephemeral container: exit 0 passes, 1 blocks, any other exit or a missing `SNYK_TOKEN` is
   NOT RUN and fails the job. Rules:
   - The scan adds to steps 2-6; it never replaces the allow-list, recorded definitions or the
     definition check. A clean scan says nothing about tomorrow's definitions.
   - Review the command and URLs (step 2) before the first run: the scanner executes them.
   - `scan` sends tool names and descriptions, MCP configuration and signatures to Snyk's API
     (secrets redacted, under Snyk's terms). Record in the PR that this is acceptable for this
     server. Never scan a config holding production credentials.
   - Do not key on output fields or scores (the scanner documents them as experimental); key on
     the exit code and the pinned scanner version. Ignoring a risk or failure code
     (`--ignore-risks`, `--ignore-failure-codes`) needs the security owner's approval in the PR.
9. **Sign-off.** Security owner approves the PR, including the scan result.
