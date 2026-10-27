# Dispatch assistant

Helps Harbour Outfitters' warehouse team quote and book parcel shipments. Google ADK 2.12, on
Cloud Run. We are adopting Freightline's MCP server (`@freightline/shipping-mcp`, stdio) for
rates, bookings and tracking; it runs as a subprocess of the agent container.

- `app/agent.py`: the agent with the Freightline `McpToolset` (pinned package version, tool
  allow-list).
- `app/mcp_pin.py`: canonical hashing of tool definitions and the diff against the recorded
  manifest `mcp/freightline-shipping.tools.json`.
- `scripts/check_mcp_definitions.py`: CI step that starts the pinned server, lists its tools and
  fails on any difference from the recorded manifest.
- `docs/security/mcp-adoption.md`: our checklist for adopting any third-party MCP server.

- `mcp-scan/freightline-shipping.json`: the agent's server command (no credentials) that the CI
  `mcp-scan` job passes to Snyk Agent Scan; `tests/test_mcp_scan_config.py` keeps it equal to
  `app/agent.py`.

CI (`.github/workflows/ci.yml`) runs jobs in containers; `SNYK_TOKEN` is available as a CI secret
and is used only by the `mcp-scan` job.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk and the MCP SDK are not installed in this environment and there is no network.
