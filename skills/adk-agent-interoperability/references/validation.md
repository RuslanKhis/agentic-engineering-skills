# Validate an interoperability change

Use the target's interpreter, pins and test runner. Every boundary gets a
before and after artefact; the offline checks need no model call.

## 1. Inventory and card reports before and after

```bash
python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "<exact server command>" --out mcp-manifest.json > .adk-evidence/mcp-before.json
python "$SKILL_DIR/scripts/agent_card_check.py" --url http://localhost:8001/a2a/<agent> --installed-a2a-sdk <version> > .adk-evidence/card-before.json
# ... change ...
python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "<exact server command>" --diff mcp-manifest.json > .adk-evidence/mcp-after.json
python "$SKILL_DIR/scripts/agent_card_check.py" --url http://localhost:8001/a2a/<agent> --installed-a2a-sdk <version> > .adk-evidence/card-after.json
```

Expect: `diff.rug_pull_signal` false unless the change was a reviewed
definition update; `tool_name_collision` empty; `reserved_adk_tool_name`
empty; every `description_imperative_phrase` read and either explained or
escalated to `adk-agent-security`; card `counts.errors` zero and
`gemini_enterprise.missing` empty when registering there. Commit the
manifest; a test compares the live list with it. Exit 1 (`partial`) means a
source was unreachable and must be explained.

The diff compares tools by bare name whenever each manifest holds a single
target, so a manifest pinned against a staging URL or a loopback fake diffs
cleanly against production; `keyed_by` in the output says which key was used,
and a multi-target manifest keeps `target::name`. The committed manifest
lives beside the agent, not under `.adk-evidence/`, which holds run output.

## 2. Source and pin check

- `google-adk`, `mcp` and `a2a-sdk` pins unchanged, or the change is a
  decision in the report with the [compatibility](compatibility.md) rows it
  brings.
- `McpToolset` and `RemoteA2aAgent` constructed at module level in
  `agent.py`; `tool_filter` present on every toolset; `tool_name_prefix` when
  more than one; `header_provider` or `auth_scheme` for per-user servers; no
  user token in `connection_params.headers`.
- `RemoteA2aAgent(timeout=...)` set deliberately; `use_legacy=False` between
  ADK peers; card URL ends with the card path.
- Advertised `to_a2a` URL equals the served one; `task_store` and shared
  session service for multi-instance deployments; card has `securitySchemes`
  and `protocolVersion`.

## 3. Fake-server tests

Follow [evaluation-across-boundaries](evaluation-across-boundaries.md): one
test per row of the MCP and A2A tables that applies to the boundary you
changed. The minimum per boundary is: normal result, timeout, error, and
(A2A) `input-required` with a peer-authored answer ignored. Run with network
egress denied so a fake is the only reachable server.

## 4. Contract table

Attach the boundary contract rows from [topology](topology.md) (input,
output, identity, timeout, failure, pause handling, coverage, evidence). A
boundary without a failure result or a coverage statement is not done.

## 5. Live exchange (approved)

Only after steps 1 to 4, with the owner's approval for connecting to the real
server or peer: one `tools/list` and one read-only `tools/call` for MCP, one
`message/send` reaching a terminal state for A2A, recorded with date,
versions, identity used and the response's state. Label it live. For
platform registration, the platform's own test call is the live evidence.

## 6. Protocol conformance (local, pinned)

The MCP project's conformance suite (`@modelcontextprotocol/conformance`,
npm; `0.2.0-alpha.12` published 2026-10-01, repository
modelcontextprotocol/conformance commit c37eec8; MCP-project licence, in
transition from MIT to Apache-2.0; invoked, never vendored) runs scenarios
against a server URL and exits 0 when every scenario passed and 1 otherwise.
Three facts decide how to use it, all from its README and confirmed by running
it on 2026-10-22 against a `to_mcp_server` instance on google-adk 2.12.0 with
`mcp` 2.3.0, streamable HTTP on loopback, a scripted model and no network:

- **Run a requirement set, not the whole suite.** `--requirements 2025-11-25`
  or `--requirements 2026-07-28` runs exactly what that revision requires at
  that revision's wire format (the dated revisions through 2025-11-25 use the
  `initialize` handshake, 2026-07-28 is stateless with per-request `_meta`),
  replaces `--suite`, `--spec-version` and `--scenario`, and lists unscored
  extension and pending scenarios separately. `list --requirements <rev>`
  prints the set. A server that serves both revisions is run twice.
- **Most scenarios call fixture tools and fail on a business server by
  design.** The `tools-call-*` (image, audio, embedded resource, mixed
  content, logging, progress, sampling, elicitation), `elicitation-*`,
  `resources-read-*`, `resources-templates-read`, `resources-subscribe`,
  `prompts-get-*`, `completion-complete`, `logging-set-level`,
  `json-schema-2020-12`, `http-custom-header-server-validation` and
  `input-required-result-*` scenarios look for the reference "everything"
  server's tools, resources and prompts (`json_schema_2020_12_tool`, tools
  with `x-mcp-header` annotations, a `test_missing_capability` diagnostic
  tool); the ADK server answers an unknown tool name with an `isError` result,
  which those checks read as a failure, not a rejection. They go into the
  baseline with the reason. The checks that need no fixture are the real
  test, and the ADK 2.12.0 server passed every one of them: `server-initialize`,
  `server-session-lifecycle`, `ping`, `tools-list`, `tools-call-simple-text`,
  `tools-call-error`, `server-sse-multiple-streams`, `resources-list`,
  `prompts-list`, `dns-rebinding-protection`, `caching` (7 of 7),
  `http-header-validation` (14 of 14), `sep-2164-resource-not-found`, and 25
  of the 27 checks in `server-stateless` (the two failures are the
  diagnostic-tool checks `sep-2575-server-rejects-undeclared-capability` and
  `sep-2575-missing-capability-http-400`, so the per-check baseline entries
  are `server-stateless:sep-2575-server-rejects-undeclared-capability` and
  `server-stateless:sep-2575-missing-capability-http-400`; check ids appear
  only in run output and in the suite's `src/scenarios/server/` sources, not
  in `list`). Totals on that server: 44 passed and 21
  failed in the default active suite; 45 and 23 under 2025-11-25 with 3
  unscored; 113 and 56 under 2026-07-28 with 13 unscored (the Tasks extension
  and three pending scenarios).
- **The baseline is a YAML file and it fails both ways.** `server:` lists
  scenario names or single checks as `<scenario>:<check-id>`; a failing entry
  in the baseline exits 0, a failing scenario not in it exits 1, and a
  baselined scenario that now passes exits 1 as a stale entry ("Baseline is
  stale: update your expected-failures file"), which is what makes the file
  a drift detector; a baselined check that a scenario never reaches is
  tolerated. All three exit paths were observed. Keep one baseline per
  revision, each entry with a comment naming the fixture it depends on, and
  prefer per-check entries so the other checks in a scenario stay enforced.

For an exposed A2A agent the counterpart is the A2A TCK, scoped to the card
and versioning requirements against a local `to_a2a` instance; the command,
the requirement ids, what the TCK cannot test on a real agent and why it was
not run here are in [a2a-contracts](a2a-contracts.md#checklist-per-boundary).
Record its `reports/compatibility.json` and the deferred ids as local
evidence once it has run on the pinned a2a-sdk.

The conformance suite needs Node 22 and the npm registry; it does not need a
model, a project or credentials when the agent behind the server runs a
scripted model. A server that serves both revisions is gated on both, one
baseline each; the first run is what turns scenario-level entries into
per-check ones. The producer-side security review is the tier review of the
tools behind the server in `adk-agent-security` (outputs as data, no
model-chosen recipient, read-only where possible); this skill's exposure
reference and checklist carry the rest of the producer's obligations. The same server answered this skill's `mcp_tool_inventory.py` over
the `initialize` handshake at protocol 2025-06-18 (one tool, exit 0), so the
inventory manifest and the conformance baseline can sit side by side in the
repository. The Inspector CLI (`@modelcontextprotocol/inspector`, 2.12.0 on
npm on 2026-10-22; `--method tools/list`) is an independent manual
cross-check of the same manifest; where it stores OAuth tokens was not
verified here.

## Completion report

State files changed, the exact commands and their output, and separate:

| Evidence | What it supports |
| --- | --- |
| Source verified | Behaviour read in the named ADK file at the pinned version |
| Local | Inventory and card reports, manifest diffs, unit tests |
| Mocked | Scripted-model Runner tests against fake servers and peers |
| Live | Approved exchanges on a named date and version |
| Not run | Anything above that was not executed on the target |

Each finding carries its `file:line`, the boundary, the contract gap, the
observable check, the evidence label and the owning skill
(`adk-agent-security`, `adk-tool-auth-and-secrets`, `safe-api-tool-calls`,
`adk-workflow-design`, `deploy-adk-on-google-cloud`,
`adk-agent-evaluation`). List the residual risks each boundary still
accepts, in the owner's words.
