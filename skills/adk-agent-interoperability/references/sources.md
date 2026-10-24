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
- modelcontextprotocol/conformance commit c37eec8 (2026-10-01; npm
  `@modelcontextprotocol/conformance@0.2.0-alpha.12`, published 2026-10-01;
  MCP-project licence in transition from MIT to Apache-2.0): `README.md`
  (server mode, `--requirements`, expected-failures semantics, per-check
  baseline entries), `requirements/2025-11-25.yaml`, `requirements/2026-07-28.yaml`,
  `src/scenarios/server/`. Read 2026-10-22 and executed the same day against a
  scripted-model `to_mcp_server` on google-adk 2.12.0 with `mcp` 2.3.0 on
  loopback; results in [validation](validation.md). The npm package was
  invoked; the repository was read, not run.
- Model Context Protocol specification, modelcontextprotocol/modelcontextprotocol
  commit 80041ab (2026-10-20): `docs/specification/2025-11-25/changelog.mdx`,
  `docs/specification/2026-07-28/changelog.mdx`, `2026-07-28/server/tools.mdx`,
  `2026-07-28/basic/authorization/client-registration.mdx`. Read 2026-10-22;
  facts in [mcp-exposure](mcp-exposure.md) and [mcp-consumption](mcp-consumption.md).
- modelcontextprotocol/ext-auth commit fb374c7 (2026-06-18; MIT):
  `specification/stable/enterprise-managed-authorization.mdx`,
  `specification/draft/oauth-client-credentials.mdx`. Read 2026-10-22; facts
  in [mcp-consumption](mcp-consumption.md).
- a2aproject/a2a-tck v0.2.5 (commit 5daf014, 2026-10-20; Apache-2.0):
  `README.md`, `run_tck.py`, `tck/requirements/{auth,agent_card,versioning}.py`,
  `scenarios/core_operations.feature`, `tck/transport/jsonrpc_client.py`,
  `AGENTS.md` (companion skills). Read 2026-10-22; not run (not published
  to PyPI; executing a downloaded repository is outside this review's
  rules). google/agents-cli main `src/google/agents/cli/run/_a2a_pinning.py`
  (origin pinning note), read 2026-10-22. a2aproject/a2a-samples HEAD
  6603ba3 (2026-08-04; Apache-2.0): `samples/python/agents/sign_and_verify_agent_card`,
  `multitenancy` and `headless_agent_auth`, with the A2A specification §7.6.4
  and §8.4 at main 98279d6 and tag v1.0.1, a2a-sdk 1.2.3 `a2a/utils/signing.py`,
  `client/card_resolver.py` and `client/transports/tenant_decorator.py`, and
  google-adk 2.12.0 `a2a/agent/_remote_a2a_agent.py` and
  `a2a/utils/agent_to_a2a.py`. Read 2026-10-24; the signing behaviour was
  probed offline against the installed a2a-sdk; no sample was run. Imported
  into [a2a-contracts](a2a-contracts.md#signed-agent-cards) and the signature
  rules of `agent_card_check.py`.
- modelcontextprotocol/inspector commit 0cac110 (release 2.12.0; MIT moving
  to Apache-2.0, docs CC BY 4.0): `clients/cli/README.md`,
  `docs/secret-storage.md`, `docs/environment-variables.md`;
  modelcontextprotocol/python-sdk commit 2af9e30 (MIT): `docs/run/legacy-clients.md`,
  `docs/protocol-versions.md`, `docs/client/transports.md`,
  `schema/2026-07-28.json`; PrefectHQ/fastmcp commit 37301f9 (Apache-2.0):
  `docs/servers/testing.mdx`, `docs/getting-started/upgrading/from-fastmcp-3.mdx`,
  `docs/servers/auth/oauth-proxy.mdx`, `docs/servers/storage-backends.mdx`.
  Read 2026-10-24. Spikes, offline: the Inspector CLI 2.12.0 against a local
  `MCPServer` on both eras (exit codes 0, 1 and 5; a manifest hash
  cross-check), `to_mcp_server` continuity under both client modes with a
  scripted model (re-run by the maintainer), and the inventory against a
  modern-only server before and after its `server/discover` fix.
- MCP python-sdk v2, `docs/whats-new.md` (v2.3.0 stable line): `FastMCP`
  renamed `MCPServer`, old import path removed, both revisions served from
  one app, `mcp>=1.28,<2` advice for unmigrated libraries. Read 2026-10-22.
- A2A specification `CHANGELOG.md` (1.0.0, 2026-03-12; 1.0.1, 2026-05-26):
  `application/a2a+json` preferred in the HTTP binding, implicit and
  password OAuth flows removed, device code and PKCE added. Read 2026-10-22.
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

## Google recipes (vendor samples)

- google/adk-recipes commit be63596 (2026-10-20; Apache-2.0):
  `core/python/long-horizon-harness/AGENTS.md` ("Pinned versions": `a2a-sdk>=1.0,<2`
  with `google-adk>=2.8.0,<3`; one `/a2a` endpoint serving the 1.0 wire and
  Gemini Enterprise's v0.3 interface). Read 2026-10-22; cited in
  [platform-registration](platform-registration.md).

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
- `googleapis/mcp-toolbox` README (repository renamed from
  `googleapis/genai-toolbox`; latest tag v1.14.0; Python SDKs including
  `toolbox-adk` in `googleapis/mcp-toolbox-sdk-python`), read 2026-10-22.
- Read 2026-10-21: Agent Gateway egress codelab
  https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp
  (`roles/iap.egressor`, `api.getAttribute('iap.googleapis.com/mcp.toolName', '')`,
  empty name for the handshake, `DRY_RUN` then enforced); routing Agent
  Runtime through Agent Gateway
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-gateway-runtime-deploy
  (`client.runtimes.create`, `agent_gateway_config`, `identity_type=AGENT_IDENTITY`,
  `GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES`,
  `networkservices.agentGateways.get`); Agent Gateway overview
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview
  (Agent Runtime and Gemini Enterprise only); use-an-a2a-agent page
  (`agentplatform.Client`, `client.runtimes`); API Gateway MCP
  https://docs.cloud.google.com/api-gateway/docs/mcp-configure.
- Re-read 2026-10-22: Gemini Enterprise "Register and manage an A2A agent"
  (page updated 2026-10-14; `roles/run.invoker`, `X-Serverless-Authorization`,
  the nine required card fields unchanged); Agent Identity page (baseline
  `roles/aiplatform.expressUser`, `serviceusage.serviceUsageConsumer`,
  `browser`, plus `logging.logWriter`, `monitoring.metricWriter`,
  `cloudapiregistry.viewer`; `spec.effectiveIdentity`); routing Agent Runtime
  through Agent Gateway (`PATCH` with
  `updateMask=spec.deploymentSpec.agentGatewayConfig`, identity type not
  changed by patch, binding change archives revisions).
- Google Agents CLI 1.11.0 (Apache-2.0, released 2026-10-20), read 2026-10-22
  from a local copy: `skills/google-agents-cli-publish/SKILL.md` (`publish
  gemini` flags and defaults, idempotent upsert, `roles/run.servicesInvoker`
  where the docs say `roles/run.invoker`, Live agents unsupported, Agent
  Registry commands and auto-registration), `skills/google-agents-cli-deploy`
  (`--agent-gateway-egress`/`-ingress`, `/api` passthrough, `APP_URL`),
  `skills/google-agents-cli-adk-code/references/adk-python.md` (MCP audience
  and extras gotchas), `src/google/agents/cli/publish/cmd_publish.py` and
  `scaffold/agents/adk/app/app_utils/a2a.py`. Vendor guidance; commands not
  executed here.
- google/skills (Apache-2.0), `skills/cloud/` collection, read 2026-10-21:
  `google-cloud-solution-multi-agent-security`,
  `apigee-agent-gateway-governance`, `api-gateway-mcp-server`,
  `api-gateway-backend-security-and-rate-limiting`. Facts taken only from
  there (principal format, `mcp.tool.isReadOnly`, four-policy limit,
  `roles/networkservices.viewer`, HTTP 200 on an invalid API key) are
  labelled vendor guidance.

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
