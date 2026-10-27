# security-adopt-third-party-mcp-server-with-scan: what the fixture holds

Standalone project `dispatch-assistant` (google-adk==2.12.0, mcp 1.18.0).

- Existing controls (A1 says keep them as the control): `tool_filter` allow-list and pinned
  package `@freightline/shipping-mcp@3.4.1` in `app/agent.py`; recorded definitions with hashes in
  `mcp/freightline-shipping.tools.json`; `app/mcp_pin.py` + `scripts/check_mcp_definitions.py`
  CI diff; `docs/security/mcp-adoption.md` checklist (steps 1-8, no scan step).
- CI (`.github/workflows/ci.yml`) runs jobs in containers; SNYK_TOKEN exists as a CI secret
  (README). The stdio server receives `FREIGHTLINE_API_KEY` from the environment — a scan with
  `--dangerously-run-mcp-servers` must not run against a config holding production credentials
  (A2).
- Expected additions: Snyk Agent Scan via `uvx` pinned to an exact version, `--ci`, exit code read
  (fields not parsed), in an ephemeral container after the server-command review (A1, A2); what
  the scan uploads to Snyk and `inspect` as the local no-upload mode, owner decision on data
  handling (A3); record that it was documented, not run, and that the output schema is
  experimental (A4).
- Tests: `tests/test_mcp_pin.py` (stdlib) passes. No network, nothing installed.
