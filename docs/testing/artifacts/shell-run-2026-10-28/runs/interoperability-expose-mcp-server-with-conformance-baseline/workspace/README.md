# Research agent

One ADK agent that answers questions about published papers using two tools.
The platform team wants to call it from their MCP hosts.

Tests: `python -m unittest discover -s tests -t .` runs the tool tests offline.
`tests/test_agent_scripted.py` drives the agent with a scripted model and needs
google-adk installed; it is skipped here, where neither google-adk nor mcp is
installed. No cloud credentials.

## MCP server

`python -m research.mcp_server` serves the agent as one MCP tool, `paper_research(request: str)`,
over streamable HTTP on `127.0.0.1:$PORT` (`--stdio` for stdio; `MCP_HOST` overrides the bind, and
there is no authentication, so front it before exposing it). Calls are single-turn: on spec
2026-07-28 there is no connection to hold a conversation, so hosts send full context per call.

CI (`.github/workflows/ci.yml`):
- `tests/test_mcp_server.py` lists and calls the tool in process under both protocol revisions.
- `scripts/conformance.sh` runs `@modelcontextprotocol/conformance` (pinned in `conformance/PINS.json`)
  for 2026-07-28 and 2025-11-25 against `conformance/baseline-<rev>.yml`. A new failure fails the
  job, and so does a baselined failure that starts passing (stale entry), so a suite change shows up either way.
- `tests/test_pins.py` fails when google-adk or mcp differ from `conformance/PINS.json`.
- A weekly `drift` job runs the latest mcp and latest conformance suite (advisory).

To move a pin: run `BASELINES=0 scripts/conformance.sh`, review the output, edit the baselines
(a reason comment per entry) and `PINS.json` in the same change.
