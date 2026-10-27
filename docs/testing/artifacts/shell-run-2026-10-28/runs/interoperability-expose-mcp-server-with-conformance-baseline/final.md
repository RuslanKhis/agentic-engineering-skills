The MCP server, the CI check and the version-drift detection are all written, but none of the new code has run. google-adk and mcp aren't installed here and I wasn't allowed to install them or use the network. What I did run offline: `bash -n` on the script, a syntax parse of the server file, and the existing unit tests. Those gave 7 tests with 5 skipped, because the SDK-dependent ones skip without google-adk and mcp.

**What I added**
- **Server:** `research/mcp_server.py` serves the agent through ADK's `to_mcp_server` as one tool, `paper_research(request: str)`. Run it with `python -m research.mcp_server` for streamable HTTP on `127.0.0.1:$PORT`, or add `--stdio`.
- **Protocol tests:** `tests/test_mcp_server.py` runs the tool list and a call through the scripted model, in process. It runs under both protocol revisions, 2026-07-28 and the older handshake revision. It also checks that an unknown tool is rejected and that the agent's instructions don't leak into the tool description.
- **Conformance run:** `scripts/conformance.sh` starts the server and runs `@modelcontextprotocol/conformance@0.2.0-alpha.12` once per revision. Each run is checked against `conformance/baseline-<rev>.yml`.
- **Drift detection:**
  - The baselines fail the job both when a new failure appears and when a baselined failure starts passing. That means a suite change surfaces either way.
  - `tests/test_pins.py` fails when the installed google-adk or mcp differ from `conformance/PINS.json` (2.12.0 and 2.3.0). I recorded those as the baseline versions because the skill's reference notes say it observed them on exactly that pairing.
  - A weekly `drift` job in `.github/workflows/ci.yml` runs the latest mcp and the latest conformance suite. It is advisory and doesn't gate PRs.
- **README:** a short section on the server and how to move a pin.

**Assumptions, since nobody could answer**
- Which spec revisions the platform team's hosts use is unknown, so I gate both.
- The server binds to loopback by default, and `MCP_HOST` overrides that. It has no authentication, so someone needs to put an authenticated edge in front of it before it is exposed. Who owns that is an open question.
- Each call is a single turn. On 2026-07-28, `to_mcp_server` can't keep a conversation across calls, so hosts must send full context in each request. Multi-turn would need a hand-built server with conversation handles, which I left out.

**Left undone**
- The baselines are not generated on this repo. The 2026-07-28 file holds only the two failures the skill documents, and the 2025-11-25 file is empty. The first CI run will probably fail and list the fixture-dependent scenarios that need entries, each with a reason. Run `BASELINES=0 scripts/conformance.sh` once to get the real list.
- I did not verify that `to_mcp_server` and the mcp 2.x client calls in my tests work as written on ADK 2.12.0.
- The unpinned `mcp>=2.0,<3` in `pyproject.toml` is unchanged. Tightening it is your call, and `test_pins.py` catches movement either way.
- I did no live exchange and no A2A work.