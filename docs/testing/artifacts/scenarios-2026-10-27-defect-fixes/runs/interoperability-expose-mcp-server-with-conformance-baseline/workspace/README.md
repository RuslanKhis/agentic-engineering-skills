# Research agent

One ADK agent that answers questions about published papers using two tools.
The platform team wants to call it from their MCP hosts.

Tests: `python -m unittest discover -s tests -t .` runs the tool tests offline.
`tests/test_agent_scripted.py` drives the agent with a scripted model and needs
google-adk installed; it is skipped here, where neither google-adk nor mcp is
installed. No cloud credentials.

## MCP server

`python -m research.mcp_server` serves the agent over stdio;
`MCP_TRANSPORT=streamable-http PORT=8000 python -m research.mcp_server` serves
`http://127.0.0.1:8000/mcp` (override with `HOST`).

Contract for hosts:

| | |
| --- | --- |
| Tool | one tool, `paper_research`, arg `request: str`; description is the agent's description (instruction not published) |
| Revisions | whatever `mcp` 2.x serves: 2025-11-25 handshake and 2026-07-28 stateless, same `/mcp` path |
| Conversation | none. Every call is an independent question (there is no connection to hold a session on 2026-07-28). Hosts must put needed context in `request` |
| Identity | caller is the fixed ADK user `mcp_user`; there is no per-caller authorisation. Tools are read-only over a static index |
| Auth | none in the server. Loopback by default; authenticate at the platform edge before binding elsewhere |
| Failure | agent exception -> `isError: true` result |

## CI

- `ci.yml` `test`: unit tests incl. `tests/test_mcp_server.py` (in-process `mcp.Client`, both eras, scripted model) with `mcp` pinned by `ci/constraints.txt`.
- `ci.yml` `conformance`: `ci/conformance.sh <revision>` runs `@modelcontextprotocol/conformance` (version in `ci/conformance.version`) for 2025-11-25 and 2026-07-28 against `tests/conformance_server.py` (fixed-text model, loopback). Failures must be in `ci/conformance-baseline-<revision>.yml`; an unlisted failure fails, and so does a listed entry that now passes (stale).
- `mcp-drift.yml` (weekly + manual): newest `mcp` <3 and newest conformance suite; fails if tests/conformance fail or if either pin is behind. Fix by bumping `ci/constraints.txt` / `ci/conformance.version` and re-reviewing the baselines.

**Baselines are not seeded yet.** Nothing could be installed or run when this was written, so
the baseline files carry an `# UNSEEDED` marker and the conformance job only records
(`ci/out/<revision>` artifact, `::warning::`) until someone seeds them from the first CI run
and deletes the marker.
