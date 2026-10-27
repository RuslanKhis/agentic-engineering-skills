# MCP conformance suite alignment — 22 October 2026

*What changed, what was checked, what the spike proved, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/mcp-conformance-comparison-2026-10-22.md).
In the repository:

- **Facts** from modelcontextprotocol/conformance (commit `c37eec8`, npm
  `0.2.0-alpha.12`), each confirmed by running the suite: a "Protocol
  conformance" section in the interoperability skill's validation reference
  (requirement sets and wire formats, the fixture-dependent scenarios, the
  scenarios the ADK server passed, the totals, the baseline semantics and
  the three exit paths, prerequisites, the inventory helper against the same
  server, the Inspector as a manual cross-check); the pinned command in the
  MCP exposure reference's checks before publishing; a fifth tier 1 gate in
  the release skill's CI reference; the acceptance phrase in the designer's
  handoff route row.
- **No routing line**: the suite is a tool invoked by name.
- **One scenario case** (`interoperability-expose-mcp-server-with-conformance-baseline`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the [testing log](index.md) entry for this date. No helper script, test or
`last-tested` date changed.

## Spike

Outside the repository, in a scratch virtual environment with
`google-adk[mcp]==2.12.0` (resolving `mcp` 2.3.0), one `LlmAgent` with one
tool and a scripted `BaseLlm` was served with
`to_mcp_server(agent, name="spike_agent").run(transport="streamable-http",
host="127.0.0.1", port=8765)`; no network, project or credential. The suite
was invoked with `npx -y @modelcontextprotocol/conformance@0.2.0-alpha.12`
on Node 22.23.2.

| Run | Result | Exit |
| --- | --- | --- |
| `server --url http://127.0.0.1:8765/mcp` (default active suite) | 44 passed, 21 failed | 1 |
| `--requirements 2025-11-25` | 45 passed, 23 failed, 3 unscored | 1 |
| `--requirements 2026-07-28` | 113 passed, 56 failed, 13 unscored (Tasks extension, 3 pending) | 1 |
| `--scenario tools-list` | passed | 0 |
| `--scenario tools-call-image` | failed (fixture tool) | 1 |
| `--scenario tools-call-image --expected-failures` baseline listing it | "Baseline check passed: all failures are expected" | 0 |
| `--scenario tools-list --expected-failures` baseline listing it | "Baseline is stale: update your expected-failures file" | 1 |
| `mcp_tool_inventory.py --url http://127.0.0.1:8765/mcp` | one tool, `initialize` at protocol 2025-06-18 | 0 |

Every failure was a scenario that calls a fixture tool, resource or prompt
of the reference server, or a diagnostic tool (`test_missing_capability`)
that the ADK server answers with an `isError` result (verified with the
`mcp` client). Every scenario that needs no fixture passed. The logs are in
the scratch directory, not the repository.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no ADK
installed, Node available, on a synthetic project, without the expected
answers.

### Interoperability: expose a research agent as an MCP server with a CI conformance check

The project: an ADK 2.12 research agent with two tools, `mcp` 2.3.0
pinned, a scripted `BaseLlm` in its tests, a CI workflow with Node 22 and
the npm registry and no Google credentials. The request: expose it to the
platform team's MCP hosts and add a CI check that proves the protocol and
tells the team when the suite or the SDK moves.

What the agent did: wrote a `to_mcp_server` entry point with stdio and
streamable HTTP transports and a scripted-model switch for CI; a
specification-free contract module and committed JSON for the published
tool; a CI job that starts the server and runs the pinned suite under both
requirement sets with one expected-failures baseline each, every entry
commented with the fixture it depends on, the fixture-free scenarios kept
enforced; tests that the contract, the pins and the baselines agree and
that no fixture-free scenario is ever baselined; a stdio JSON-RPC test and a
Runner test reported as not run without the SDK. Verified every baseline
entry against the suite's `list --requirements` output and the pin against
the registry, read-only; started no server.

Ease rating: **4 of 5**. Routing was unambiguous and the validation
section matched the task; the point lost went to information spread over
five references and two unsettled decisions.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| "The repository's 2.8.0 pin" read as the project's pin, while the validation section ran on 2.12.0 | The compatibility reference now says 2.8.0 is this toolkit's reference baseline, not the project's pin, and that later-version facts say so beside the fact |
| No skill said how to bind host and port on the 2.x server; the agent guessed at a `settings` attribute | The exposure reference now gives `MCPServer.run(transport, **kwargs)` and the full `run_streamable_http_async` signature read in the installed SDK, and the one-line bind |
| Per-check baseline entries were recommended but the check ids were unreachable offline | The validation reference names both `server-stateless` check ids and says where ids appear |
| Observed 2.x server behaviour (`initialize` negotiation, `isError` on unknown tools) was only implied | Stated in the exposure reference as observed on 2.12.0 with `mcp` 2.3.0, with stdio framing marked as not exercised |
| The inventory helper lives in the skill and cannot run in the project's CI | The exposure reference says to copy it with its header or run it from a pinned checkout, and to record which |
| The engineer's `__init__.py` rule did not name a pattern that keeps `adk web` discovery working | The rule now names the module-level `__getattr__` pattern with a confirm-once note |
| The security skill had no producer-side section, so the routing looked like a dead end | The validation reference says the producer-side security review is the tier review of the tools behind the server and that the exposure reference and checklist carry the rest |
| "the memo's note" in the validation reference dangled | Reworded |
| Whether to gate on both revisions was unsettled | The validation reference says a server that serves both is gated on both, one baseline each |

## What this does not establish

The spike proved one server shape on one SDK pair; the trial's server was
never started and its CI job never ran. Stdio framing was not exercised.
