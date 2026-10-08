# Sources

Each entry carries its evidence label and the date it was read or supplied.
Entries marked "supplied by research" came from the coordinator's research on
2026-10-08 and were not re-fetched here; confirm before quoting to an owner.

## ADK source and documentation (source-verified, documented behaviour)

- `google-adk` 2.8.0 source, tag v2.8.0 (2026-08-25), read 2026-10-08:
  `tools/mcp_tool/mcp_toolset.py`, `mcp_session_manager.py`, `mcp_tool.py`,
  `session_context.py`, `_agent_to_mcp.py`, `conversion_utils.py`,
  `tools/base_toolset.py`, `tools/toolbox_toolset.py`,
  `tools/application_integration_tool/application_integration_toolset.py`,
  `tools/openapi_tool/openapi_spec_parser/openapi_toolset.py`,
  `agents/remote_a2a_agent.py`, `a2a/_compat.py`, `a2a/experimental.py`,
  `a2a/utils/agent_to_a2a.py`, `a2a/utils/agent_card_builder.py`,
  `a2a/executor/a2a_agent_executor.py`, `a2a/converters/request_converter.py`,
  `a2a/agent/interceptors/new_integration_extension.py`, `cli/fast_api.py`,
  `cli/cli_tools_click.py`, `features/_feature_registry.py`,
  `flows/llm_flows/functions.py` (reserved tool names), `pyproject.toml`
  (`mcp>=1.24,<2`, `a2a-sdk[http-server]>=0.3.4,<2`),
  `integrations/agent_registry/agent_registry.py`.
- `adk-python` main at 2.11.0 (2026-10-01) and `CHANGELOG.md`, read
  2026-10-08: `tools/mcp_tool/mcp_session_manager.py` (`_is_google_api_host`),
  `a2a/agent/_remote_a2a_agent.py` (`_MAX_CARD_DESCRIPTION_CHARS = 1024`,
  `context_builder`), `a2a/agent/config.py`
  (`forward_session_id_as_context_id`), `pyproject.toml` (`mcp>=1.24,<3`).
  CHANGELOG entries cited by commit: 2.7.0 16cbb7d, efdecf4, a61d8ec,
  9cd5975, 4f58306, aec7aa3; 2.8.0 72f3ff5, d42c634, 9e9eaa6, 9a32eba,
  2aea859, 69a3ca5; 2.9.0 856acf2, 46edaa2, f9f4a39, 7ee3ae9, fe30ebb,
  04be48b, aef3a9c, 2685acd; 2.10.0 322e3bf, e10a1be, 5a018c9, 86ea33d,
  d64dcfa, e29ee23, dfc96d0; 2.11.0 e738c26, 8632980, f44d512, 9a33588,
  9115d61, caf2356, 5b079ee, f7967c3.
- ADK docs (adk-docs repository, read 2026-10-08): `docs/tools-custom/mcp-tools/index.md`
  (implementation options table, "always supply tool_filter", synchronous
  definition, `K_SERVICE` pattern), `advanced.md` (`header_provider`,
  `require_confirmation`, `progress_callback`, `close()`,
  `tool_name_prefix`, sampling and elicitation, UI widgets),
  `deployment.md` (synchronous definition, Streamable HTTP with
  `stateless=True`, sidecar pattern, security list), `agent-as-server.md`
  (`to_mcp_server`, hand-built servers with `adk_to_mcp_tool_type`),
  `agent-managed.md` (AgentTool delegation); `docs/a2a/intro.md` (when to use
  A2A versus local sub-agents), `quickstart-consuming.md`,
  `quickstart-exposing.md` (`to_a2a` parameters, advertised URL), `a2a-extension.md`
  (`use_legacy=False`, extension URI, Python v1.27.0); `docs/tools-custom/openapi-tools.md`
  (`operationId` naming). Published at https://adk.dev/ .

## Protocol specifications (documented behaviour, normative)

- Model Context Protocol specification changelog, revision 2026-07-28:
  https://modelcontextprotocol.io/specification/latest/changelog (read
  2026-10-08). Sessions and `Mcp-Session-Id` removed; `initialize` handshake
  removed in favour of `_meta` version fields and `server/discover`;
  `subscriptions/listen`; Tasks moved to extension
  `io.modelcontextprotocol/tasks`; Multi Round-Trip Requests with
  `resultType: "input_required"`; mandatory `resultType`; `ttlMs` and
  `cacheScope` on list results; deterministic `tools/list` order recommended;
  Roots, Sampling, Logging, HTTP+SSE and Dynamic Client Registration
  deprecated.
- MCP Security Best Practices, revision 2026-07-28:
  https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
  (token passthrough MUST NOT, audience validation, confused deputy and
  per-client consent, SSRF guards). Supplied by research; threat
  consequences owned by `adk-agent-security`.
- MCP Tools: https://modelcontextprotocol.io/specification/latest/server/tools
  (servers MUST validate inputs and rate limit; clients SHOULD confirm
  sensitive operations, time out, log, validate results against
  `outputSchema`; prefix names when aggregating; annotations are hints).
  Supplied by research.
- A2A Protocol specification 1.0.0: https://a2a-protocol.org/latest/specification/
  (JSON-RPC, gRPC and HTTP+JSON bindings; `A2A-Version` header with empty
  meaning 0.3; task states including `REJECTED`, `INPUT_REQUIRED`,
  `AUTH_REQUIRED`; `SendStreamingMessage`, `SubscribeToTask`, push
  notification config methods; `GetExtendedAgentCard`). Read 2026-10-08
  (first 100k characters).
- A2A agent discovery: https://a2a-protocol.org/latest/topics/agent-discovery/
  (`/.well-known/agent-card.json`; registries; direct configuration;
  authenticated extended card). Read 2026-10-08. The research summary's
  `/.well-known/a2a-agent-card` rendering was not found on the live page and
  is not encoded.
- A2A and MCP: https://a2a-protocol.org/latest/topics/a2a-and-mcp/ (vertical
  versus horizontal). Supplied by research.
- A2A enterprise readiness: https://a2a-protocol.org/latest/topics/enterprise-ready/
  (TLS 1.2+, card-declared auth in headers, 401/403 semantics, per-skill
  authorization, OpenTelemetry and W3C trace headers, webhook security).
  Supplied by research.

## Google Cloud platform (vendor guidance)

- Gemini Enterprise, "Register and manage an A2A agent", last updated
  2026-10-05: https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent
  (required card fields; A2A v0.3 streaming; compatibility packages for
  1.0.0+; `X-Serverless-Authorization` OIDC token for Cloud Run; end-user
  OAuth in `Authorization`; Agent Gateway bypass; `agents.create`,
  `agents.patch`, `agents.delete`). Read 2026-10-08.
- Agent Platform Runtime A2A agents:
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime/create-an-a2a-agent
  and https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-a2a-agent
  (A2aAgent template, authenticated `/v1/card`, Preview). Community
  announcement "Building bridges: deploy agents with A2A on Vertex AI Agent
  Engine", 2025-09-10,
  https://discuss.google.dev/t/building-bridges-deploy-agents-with-a2a-on-vertex-ai-agent-engine/264044 .
  Supplied by research.
- Google Cloud blog, "Where to use sub-agents versus agents-as-tools",
  2025-11-08: https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools .
  Supplied by research.
- Agent Registry, Agent Gateway egress codelab, Agent Identity
  (`integrations/agent-identity.md`), MCP Toolbox for Databases ADK page
  (mcp-toolbox.dev), Application Integration role notes. Supplied by
  research; commands and role names to confirm on the live pages.

## Independent evidence and practitioner analyses

- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST), arXiv
  2503.13657, 2025 (14 failure modes in three categories; κ = 0.88).
  Independent evidence, supplied by research.
- Anthropic engineering, "How we built our multi-agent research system",
  2025-06-13: https://www.anthropic.com/engineering/multi-agent-research-system
  (parallelisable work beyond one context; about 15 times chat tokens;
  isolated windows; condensed returns). Vendor-measured, supplied by research.
- Cognition, "Don't build multi-agents", 2025-06-12:
  https://cognition.com/blog/dont-build-multi-agents (share full traces;
  actions carry implicit decisions; default to a single thread).
  Practitioner analysis, supplied by research.

## Community reports (verify status before quoting)

- google/adk-python issues #6461 (approvals over A2A, open at 2.8.0), #7060
  (stale pooled MCP session after scale-to-zero), #7217 (static ADC header
  expiry), #6735 (YAML McpToolset under adk web), #6585 (A2A stream ending
  early), #6721 (relayed human-input pause), #6831 (completed delegation
  breaking later peers), #3301 (context_builder), #3098 (request metadata
  forwarding), #4448 (`to_a2a` path prefix), PR #3236 (cache review).
  Supplied by research; CHANGELOG entries for the fixes verified locally.
- discuss.google.dev 303219 (Dec 2025, Agent Engine root with remote A2A
  sub-agents returns HTTP 400, unresolved) and 325331 (Jan 2026, Gemini
  Enterprise same-project constraint). Supplied by research.
- Practitioner notes on card URLs needing to end in
  `/.well-known/agent-card.json` (Pega forum, 2026-07) and on trailing
  slashes in registered card URLs (Medium, 2026-04-01). Supplied by research;
  the ADK behaviour behind them (`A2ACardResolver` path use, `rstrip("/")`
  in `build_agent_card`) was verified in source.
