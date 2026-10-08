# Interoperability review checklist

Copy into the target's docs and fill one row per boundary. A boundary is any
`McpToolset`, `OpenAPIToolset`, `ToolboxToolset`,
`ApplicationIntegrationToolset`, `RemoteA2aAgent`, `to_a2a`, `to_mcp_server`
or `agent.json`. Each row needs an owner, an observable check and an evidence
tier (source verified, local, mocked, live, not run).

## Boundary register

| Boundary (`file:line`) | Kind | Operator | Transport and auth | Filter and prefix | Timeout | Failure result | Pause handling | Manifest or card checked | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | |

## Per-boundary questions

MCP consumer:

- [ ] Defined synchronously in `agent.py`; transport chosen by environment.
- [ ] `tool_filter` lists names; read-only in production unless tiered and gated.
- [ ] `tool_name_prefix` set when another toolset exists.
- [ ] Manifest committed; `--diff` runs in a test or at startup; `rug_pull_signal` fails the check.
- [ ] Credentials via `header_provider` or `auth_scheme`; no user token in static headers; no passthrough.
- [ ] `tool_list_cache_ttl_seconds` decided and justified.
- [ ] `close()` owner identified outside `adk web`.
- [ ] Fake-server tests: normal, `isError`, down, restarted, slow, confirmation.

MCP producer (`to_mcp_server` or hand-built):

- [ ] Description states capability only; no instructions.
- [ ] Caller treated as a client, not the user; no approval satisfiable by the MCP caller.
- [ ] Own `Runner` with shared session service where conversations must persist.
- [ ] Inventory run against the served endpoint; findings read.

A2A consumer (`RemoteA2aAgent`):

- [ ] Card URL ends with the card path; `agent_card_check.py` shows no errors.
- [ ] `timeout` from the peer's SLA; parent behaviour on error event written.
- [ ] `use_legacy=False` between ADK peers.
- [ ] Auth header matches the card's `securitySchemes`; no upstream token forwarded.
- [ ] `a2a:task_id` and `a2a:context_id` consumed where the UI or logs need them.
- [ ] Peer messages, metadata and `a2a_metadata` treated as data; approval-over-A2A test present.
- [ ] Fake-peer tests: completed, streaming, input-required, auth-required, rejected, failed, 401/403/5xx, stream cut.

A2A producer (`to_a2a`, `adk api_server --a2a`, platform template):

- [ ] Advertised URL equals served URL; https for non-loopback.
- [ ] Card has `protocolVersion`, `securitySchemes`, deliberate `capabilities`; instructions and secrets absent; tool docstrings reviewed.
- [ ] Persistent `task_store` and shared session service for multi-instance.
- [ ] `Workflow` emits an `Event` with a message so the task completes.
- [ ] Registration fields complete for the target platform; invoker role granted with approval.

Topology:

- [ ] Each remote boundary justified by ownership, identity, language or contract (not by habit).
- [ ] Contract table filled (input, output, identity, timeout, failure, pause, coverage, evidence).
- [ ] MAST categories reviewed: specification, inter-agent misalignment, verification.

## Owning skills for deferred findings

| Concern | Skill |
| --- | --- |
| Tool poisoning, pinning by hash, token passthrough, SSRF, trifecta | adk-agent-security |
| OAuth flow, credential storage, Agent Identity provisioning | adk-tool-auth-and-secrets |
| Retries, cooperative deadlines, idempotent writes | safe-api-tool-calls |
| In-process orchestration, state handoffs | adk-workflow-design |
| Budgets, approval mechanics | adk-operational-guardrails |
| Cloud Run, Agent Runtime, GKE deployment and IAM | deploy-adk-on-google-cloud |
| Eval sets, judges, measurement | adk-agent-evaluation |
| Tool docstrings and schemas | adk-tool-interface-design |
