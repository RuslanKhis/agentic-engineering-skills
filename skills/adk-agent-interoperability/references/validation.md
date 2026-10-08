# Validate an interoperability change

Use the target's interpreter, pins and test runner. Every boundary gets a
before and after artefact; the offline checks need no model call.

## 1. Inventory and card reports before and after

```bash
python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "<exact server command>" --out mcp-manifest.json > /tmp/mcp-before.json
python "$SKILL_DIR/scripts/agent_card_check.py" --url http://localhost:8001/a2a/<agent> --installed-a2a-sdk <version> > /tmp/card-before.json
# ... change ...
python "$SKILL_DIR/scripts/mcp_tool_inventory.py" --command "<exact server command>" --diff mcp-manifest.json > /tmp/mcp-after.json
python "$SKILL_DIR/scripts/agent_card_check.py" --url http://localhost:8001/a2a/<agent> --installed-a2a-sdk <version> > /tmp/card-after.json
```

Expect: `diff.rug_pull_signal` false unless the change was a reviewed
definition update; `tool_name_collision` empty; `reserved_adk_tool_name`
empty; every `description_imperative_phrase` read and either explained or
escalated to `adk-agent-security`; card `counts.errors` zero and
`gemini_enterprise.missing` empty when registering there. Commit the
manifest; a test compares the live list with it. Exit 1 (`partial`) means a
source was unreachable and must be explained.

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
