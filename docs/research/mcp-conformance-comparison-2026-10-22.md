# The MCP conformance suite compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [modelcontextprotocol/conformance](https://github.com/modelcontextprotocol/conformance)
at commit `c37eec8` (2026-10-01), latest tag v0.1.16, cloned on 22 October
2026 into its own directory and read, with the published npm package
`@modelcontextprotocol/conformance@0.2.0-alpha.12` (published 2026-10-01)
invoked from the registry for the spike. Licence: the MCP project's,
described in its repositories as in transition from MIT to Apache-2.0; the
suite is invoked as a tool, never vendored. Files read: `README.md` (server
mode, suites, requirement sets, expected failures, per-check baselining),
`requirements/2025-11-25.yaml` and `requirements/2026-07-28.yaml`, the
`src/scenarios/server/` listing and `action.yml`.

**Conclusion.** The memo's central claim holds and was proven rather than
read: the suite gives the interoperability specialist a pinned command with
usable exit codes, and its baseline file fails on a stale entry as well as a
new failure, so a committed baseline is a drift detector. The memo's
secondary claims were refined by the run: on an ADK 2.12.0 server the
fixture-dependent scenarios fail because they look for the reference
server's tools, resources and prompts (not only the `tools`, `stateless` and
`prompts` scenarios the memo named), the server passed every scenario that
needs no fixture, and `--requirements 2026-07-28` did not "fail wholesale"
on the 2.12.0 line, which ships `mcp` 2.x.

## Method and spike

A scratch virtual environment outside the repository with
`google-adk[mcp]==2.12.0` (resolving `mcp` 2.3.0) served one `LlmAgent` with
a scripted `BaseLlm` through `to_mcp_server` over streamable HTTP on
loopback; no network, project or credential was used. The suite ran in its
default active mode, under `--requirements 2025-11-25`, under
`--requirements 2026-07-28`, as single scenarios to record exit codes, and
with two baseline files to observe the expected-failure rules. The toolkit's
own `mcp_tool_inventory.py` was run against the same server. Everything
observed is written into the interoperability skill's validation reference
with the versions; nothing from the suite was copied. The spike results and
the fresh-agent trial are in the
[testing record](../testing/mcp-conformance-alignment-2026-10-22.md).

## Drift corrected

- "ADK 2.8.0 pins `mcp<2`, so `--requirements 2026-07-28` may fail
  wholesale": not on 2.12.0, where `server-stateless` passed 25 of 27 checks
  and the two failures are diagnostic-tool checks. The 2.8.0 line was not
  spiked; the validation reference says what was observed and on which
  versions.
- The set of fixture-dependent scenarios is wider than the memo's three; the
  validation reference lists them.

## Imported, by specialist

- **adk-agent-interoperability.** A "Protocol conformance" section in the
  validation reference (requirement sets and wire formats, the
  fixture-dependent scenarios and the ones that are the real test with the
  observed results, the baseline semantics with all three exit paths
  observed, the Node and registry prerequisites, the inventory helper's
  negotiation against the same server, the Inspector CLI as a manual
  cross-check); the pinned command among the checks before publishing.
- **adk-release-engineering.** The suite as a tier 1 gate for an exposed MCP
  server, with the exit-code and stale-baseline behaviour.
- **adk-system-designer.** The acceptance check for an exposed MCP server as
  a pinned command with a reviewed baseline, written only because the spike
  proved it.

## Routed, not copied

The suite is invoked by its pinned npm name; no routing line, since it is a
tool rather than a skill.

## Vendored assets

None.

## Left out, with reasons

- The client mode, the authorization-server scenarios, `tier-check`,
  `new-sep` and the traceability manifest: for SDK and host implementers.
- The GitHub Action: described by its inputs only; the pinned `npx` command
  is the portable form.
- The Inspector's keychain behaviour: read in the memo, not verified.
- A spike on the 2.8.0 line: the environment would need `mcp` 1.x and a
  second server; left as the version-conditional note.

## Limits

One server shape (`to_mcp_server`, one tool, scripted model), one ADK
version, one suite version at alpha. The suite keeps growing and its
requirement sets are frozen per revision, so the scenario lists above date
from this run; the baseline rules are the stable part.
