I've written the MCP server and the CI checks, but none of it has been run. google-adk and mcp aren't installed here and I couldn't install anything or reach the network. The conformance baselines are also not seeded, so the conformance job doesn't gate yet.

**What's there**
- **Server** (`research/mcp_server.py`): serves the agent as one tool, `paper_research`, taking a single `request` string. The default is stdio. Setting `MCP_TRANSPORT=streamable-http` gives HTTP on `127.0.0.1:$PORT/mcp`. The tool description is the agent's description, so the agent's instruction isn't published.
- **Tests** (`tests/test_mcp_server.py`): in-process tests that drive the server with a scripted model under both protocol versions (2026-07-28 and the older handshake). They check the tool list, a normal call, an agent exception coming back as `isError`, and an unknown tool being refused. A separate test fails if the installed `mcp` differs from `ci/constraints.txt`. The tests skip when ADK or mcp is missing, like the existing scripted-agent test.
- **CI** (`ci.yml`): `mcp` is pinned to 2.3.0 in `ci/constraints.txt`. A new `conformance` job runs the official conformance suite, pinned to `0.2.0-alpha.12`, for 2025-11-25 and 2026-07-28. It runs through `ci/conformance.sh` against `tests/conformance_server.py`, which uses a fixed-text model, so no credentials are needed.
- **Drift** (`mcp-drift.yml`): a weekly and manual run with the newest `mcp` below 3 and the newest conformance suite. It goes red if the tests or conformance fail, or if either pin is behind. The baselines also catch drift: a listed failure that now passes fails the run as stale.

**Not done**
- **Baselines are seeded only partly.** The two `server-stateless` entries come from the skill's notes on a 2.12.0 / mcp 2.3.0 run, not from a run here. Both files carry an `# UNSEEDED` marker. While it's present, the conformance job only records results and uploads them as an artifact with a warning. After the first CI run, add the expected failures, each with a reason, and delete the marker. Until then conformance isn't a gate.
- **Unverified API details.** `mcp.Client(server, mode="legacy")`, the `isError`/`is_error` field name, and `root_agent.clone(update=...)` follow the skill's notes and my reading of the SDK, not an installed copy. ADK also marks `to_mcp_server` experimental, and I don't know whether it needs a feature flag. Expect the first CI run to turn up small fixes.
- **No committed tool manifest.** I couldn't generate one without running the server, so there's no tool-definition diff check beyond the name, description and argument assertions in the tests.

**Assumptions** (nobody was available to answer)
- Hosts ask independent questions and don't need conversation continuity. On the 2026-07-28 revision there is no connection to hold a session on, so the README says no continuity is promised. If you need multi-turn, that needs a hand-built server, which I haven't written.
- Hosts are trusted callers: the server has no auth and every caller is the fixed ADK user `mcp_user`. The tools are read-only over a static index. It binds to loopback by default, so authentication at the platform edge is needed before it's exposed more widely.
- The `# UNSEEDED` marker is my own convention. It lets the conformance job go green before the baselines exist, at the price of not gating.

**Questions for the platform team**
- Do their hosts need multi-turn conversations with the agent?
- Which auth mechanism will front the server?