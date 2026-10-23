# Host and register an A2A agent on Google Cloud

Read this for mode (f) after [a2a-contracts](a2a-contracts.md). Everything
here is vendor guidance from Google documentation supplied by research on
2026-10-08 unless marked read or source-verified; product names and paths
change, so confirm each row on the live page before quoting it to an owner.
Deployment mechanics (build, IAM bindings, service accounts, cleanup) belong
to `deploy-adk-on-google-cloud`; this page lists what the A2A boundary needs
from the platform. When the registration itself, or an Agent Registry entry,
is to be performed with Google's CLI (`agents-cli publish gemini`, `gcloud
agent-registry`), consult the installed `google-agents-cli-publish` skill;
if it is not installed, adk-engineer explains how to get it.

## Where the agent runs and what serves the card

| Host | How A2A is served | Card discovery | Auth to reach it |
| --- | --- | --- | --- |
| Your container (Cloud Run, GKE) with `to_a2a` or `adk api_server --a2a` | Starlette routes from `_compat.attach_a2a_routes_to_app` (source-verified) | `/.well-known/agent-card.json` (or `/a2a/<folder>/.well-known/agent-card.json`) served publicly by the app; an Agents CLI Python scaffold mounts the card and JSON-RPC under `/a2a/{app_name}` and advertises `APP_URL` as the card's `url` (Agents CLI 1.11.0, `google-agents-cli-publish` skill, read 22 October 2026) | Whatever the edge enforces: Cloud Run IAM (`--no-allow-unauthenticated`), IAP, or in-app validation of the header the card declares |
| Agent Platform Runtime (formerly Agent Engine), A2A template, Preview | `A2aAgent(agent_card=..., agent_executor_builder=...)` template; operations `on_message_send`, `on_get_task`, `on_cancel_task`, `handle_authenticated_agent_card`; endpoint `.../reasoningEngines/{id}/a2a`. The current page (read 2026-10-21) drives it with `import agentplatform`, `agentplatform.Client(project=, location=, http_options={"api_version": "v1beta1"})` and `client.runtimes.get(name=...)`; the earlier `vertexai.agent_engines` and `client.agent_engines` names (community post 2025-09-10) are the deprecated spelling, so match the installed `google-cloud-aiplatform` before copying either | The public well-known card is **not** served; clients GET `{a2a_url}/v1/card` with a bearer ADC token. `agent_card_check.py --url <a2a_url> --card-path /v1/card --header "Authorization=Bearer $(gcloud auth print-access-token)" --allow-remote` after approval | Google IAM on the Reasoning Engine; `cloud-platform` scope for the caller |
| Gemini Enterprise (registered external A2A agent) | Gemini Enterprise calls your endpoint; traffic does not pass Agent Gateway, so its policies do not apply | Card JSON supplied at registration (`a2aAgentDefinition.jsonAgentCard`) | Cloud Run: Google-signed OIDC token for the Discovery Engine service agent (`service-PROJECT_NUMBER@gcp-sa-discoveryengine.iam.gserviceaccount.com`) in `X-Serverless-Authorization`; grant that service agent `roles/run.invoker` ([register and manage an A2A agent](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-a2a-agent), page updated 2026-10-14, read 2026-10-22). Google's `google-agents-cli-publish` skill at 1.11.0 names `roles/run.servicesInvoker` for the same grant; grant the documented role and verify effective access rather than both. End-user OAuth (when configured) arrives in `Authorization` |

Agent Runtime consequence: `RemoteA2aAgent(agent_card="https://.../a2a/.well-known/agent-card.json")`
cannot resolve a Runtime-hosted peer; pass the card as a file or object and
install an auth interceptor (or `auth_scheme`) that adds the bearer to both
the card request and message sends. Remember that a file card skips the
https and same-origin validation, so you own the target check.

A container deployed to Agent Runtime by Agents CLI is a different case from
the A2A template: the runtime exposes the container's own routes under an
`/api` passthrough,
`https://{location}-aiplatform.googleapis.com/reasoningEngines/v1/{resource}/api/{container_path}`,
so the scaffold's card is at
`.../api/a2a/{app_name}/.well-known/agent-card.json`, the deploy sets
`APP_URL` to that passthrough so the card advertises a reachable `url`, and
the caller sends a Google access token (`agents-cli run --url ... --mode a2a`
does this) (Agents CLI 1.11.0, `google-agents-cli-publish` skill, read 22 October 2026). `agent_card_check.py --allow-remote` with an
`Authorization=Bearer` header reads it the same way.

## Gemini Enterprise registration (docs page updated 2026-10-14, re-read 2026-10-22; Google's console and CLI now say "Gemini")

Required card fields: `protocolVersion`, `name`, `description`, `url`,
`version`, `defaultInputModes`, `defaultOutputModes`, `capabilities`,
`skills`. `agent_card_check.py` reports them under `gemini_enterprise` and
flags a missing top-level `url` on a 1.0-shaped card. Gemini Enterprise
"supports the A2A v0.3 streaming mechanism"; a 1.0.0 or later server must
offer the compatibility layer (`a2a.compat.v0_3` in the Python SDK; ADK's
`attach_a2a_routes_to_app(enable_v0_3_compat=True)` is the default on the
1.x path, source-verified). Google's long-horizon-harness recipe runs exactly
that configuration: `a2a-sdk[http-server,sqlite]>=1.0,<2` with
`google-adk>=2.8.0,<3`, one `/a2a` endpoint serving the web UI on the native
1.0 wire and Gemini Enterprise on the v0.3 interface, with one converter
reshaping streams for both clients (google/adk-recipes be63596,
`core/python/long-horizon-harness/AGENTS.md`, "Pinned versions" and the A2A
row, read 2026-10-22; vendor sample). Registration uses the REST methods
`agents.create`, `agents.patch` and `agents.delete` (Agents CLI calls
`v1alpha/.../engines/{engine}/assistants/default_assistant/agents` with
`a2aAgentDefinition.jsonAgentCard`, or `adkAgentDefinition` for a native
Agent Runtime registration, and `authorizationConfig` for an OAuth
authorization; it looks up an existing registration for the same card URL
and patches it, so a re-run updates in place). With `agents-cli publish
gemini`, A2A is the only registration mode on Cloud Run and GKE, and on
Agent Runtime the default is ADK native registration (`:streamQuery` on the
reasoning-engine resource), with A2A available through `--registration-type
a2a` and a warning; `--authorization-id` attaches an OAuth authorization,
`--deployment-target` sets the default mode and the card-fetch
authentication, and a Live or voice (bidi) agent cannot be registered
because the Gemini app has no `/run_live` transport. The `publish
gemini-enterprise` spelling and `--gemini-enterprise-app-id` remain hidden
aliases (Agents CLI 1.11.0, `google-agents-cli-publish` skill, read 22 October 2026). "Session not found" after an ADK registration on
`google-cloud-aiplatform <= 1.128.0` is a known SDK bug per the same skill;
upgrade, redeploy and re-register (vendor guidance). Model Armor and other
gateway policies must be applied inside the agent because this traffic
bypasses Agent Gateway (`protect-adk-sensitive-data` configures them). A
community thread (discuss.google.dev 325331, January 2026) reports a
same-project constraint that blocks registering an agent hosted in another
project; a cross-project A2A hop from a same-project agent is the workaround
people describe. Treat as community report.

## Agent Registry and Agent Gateway (vendor guidance, confirm commands)

- Agent Registry stores cards and MCP server specs:
  `gcloud agent-registry services create --agent-spec-type=a2a-agent-card
  --agent-spec-content=agent-card.json` (10 KB card cap reported). Agents
  deployed to Agent Runtime are auto-registered, so no create call follows
  `agents-cli deploy`; the metadata and endpoint are edited on the Service
  resource (`gcloud agent-registry services update NAME --interfaces
  "url=ENDPOINT_URL,protocolBinding=http-json"`), an external MCP server is
  registered from its `tools/list` response (`gcloud agent-registry services
  create SERVER --location=L --mcp-server-spec-type=tool-spec
  --mcp-server-spec-content=toolspec.json
  --interfaces="url=SERVER_URL,protocolBinding=jsonrpc"`, no `us`/`eu`
  multi-region), writes need `roles/agentregistry.editor`, and Terraform has
  `google_agent_registry_service` with an `mcp_server_spec` block (Agents CLI 1.11.0, `google-agents-cli-publish` skill, read 22 October 2026). ADK's
  `AgentRegistry.get_remote_a2a_agent()` and `get_mcp_toolset()` exist in
  2.8.0 (`integrations/agent_registry/agent_registry.py`, source-verified
  method names) and need `google-adk[a2a,agent-identity]`; 2.11.0 resolves
  registry MCP bindings for a deployed agent at runtime (CHANGELOG 9115d61).
- Agent Gateway egress (codelab
  https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp and the
  runtime routing page, both read 2026-10-21): create the runtime with
  `client.runtimes.create(...)`, `identity_type="AGENT_IDENTITY"` and
  `agent_gateway_config={"agent_to_anywhere_config": {"agent_gateway":
  "projects/P/locations/R/agentGateways/G"}}`. The binding can also be set
  on an existing agent (`PATCH` with
  `updateMask=spec.deploymentSpec.agentGatewayConfig`), but patching does
  not change `identity_type`, so an agent created without Agent Identity
  must be recreated, and any binding change archives every earlier
  revision (runtime routing page, re-read 2026-10-22). Agents CLI 1.11.0
  performs the same update with `agents-cli deploy --agent-gateway-egress`
  and `--agent-gateway-ingress` (`google-agents-cli-deploy` skill, read 22
  October 2026); `deploy-adk-on-google-cloud` carries the certificate and
  approval consequences. Register MCP servers with
  `--mcp-server-spec-content` and `--interfaces=url=...,protocolBinding=JSONRPC`,
  grant `roles/iap.egressor` with the condition
  `api.getAttribute('iap.googleapis.com/mcp.toolName', '') in ['<tool>', '']`
  (the empty name lets `initialize` and `tools/list` pass), and start in
  `DRY_RUN`. The agent's principal has the form
  `principal://agents.global.org-<N>.system.id.goog/resources/aiplatform/projects/<P>/locations/<R>/reasoningEngines/<ID>`
  and the attribute `iap.googleapis.com/mcp.tool.isReadOnly` is also offered
  in conditions (Google's `google-cloud-solution-multi-agent-security` skill,
  read 21 October 2026; vendor guidance, confirm against current docs). The
  Vertex AI service agent `service-<N>@gcp-sa-aiplatform.iam.gserviceaccount.com`
  needs `networkservices.agentGateways.get` on the gateway project or
  creation fails at once; `roles/networkservices.viewer` carries it and the
  `agentGatewayUser` role does not (runtime routing page and Google's
  `apigee-agent-gateway-governance` skill, read 2026-10-21). Limits: the
  gateway governs agents on Agent Runtime (ingress and egress) and Gemini
  Enterprise (egress) only (overview page, read 2026-10-21); at most four
  custom AuthzPolicies attach to one gateway and the order of two
  `CONTENT_AUTHZ` policies is undefined (Google skill, vendor guidance).
  When the gateway, its egress policies or Agent Registry entries must be
  provisioned, consult the installed Google skill
  `google-cloud-solution-multi-agent-security` (from google/skills); when
  the gateway's LLM egress must be metered or screened through Apigee,
  `apigee-agent-gateway-governance`; if either is not installed,
  adk-engineer explains how to get it. The deployment itself, including the
  Agent Identity settings, belongs to `deploy-adk-on-google-cloud`.
  Agent Identity (`integrations/agent-identity.md`, Python ≥ 1.30):
  `CredentialManager.register_auth_provider(GcpAuthProvider())` and a
  `GcpAuthProviderScheme(name="projects/.../authProviders/...", continue_uri=...)`
  as `McpToolset.auth_scheme`. Identity provisioning is
  `adk-tool-auth-and-secrets`' and `deploy-adk-on-google-cloud`'s work; the
  interoperability consequence is that the gateway, not your code, decides
  which tool names may cross.

## Toolset-specific platform notes

- MCP Toolbox for Databases: `ToolboxToolset(server_url, toolset_name,
  tool_names, auth_token_getters, bound_params)` on 2.8.0; the Toolbox ADK
  docs describe `credentials=CredentialStrategy.workload_identity(target_audience=TOOLBOX_URL)`,
  `user_identity`, `api_key`, `manual_token` and `from_adk_auth_config`, plus
  `secure_params` (toolbox-adk ≥ 1.4.0). Bound parameters never reach the
  model. Verify the installed `toolbox-adk` version before using these names.
  Re-read 2026-10-22 in the Toolbox Python ADK SDK page (mcp-toolbox v1.14.0,
  `docs/en/documentation/connect-to/toolbox-sdks/python-sdk/adk/index.md`):
  the strategies are `workload_identity(target_audience=)`, `user_identity`
  (the ADK-native three-legged flow; the `openid` scope is required for a
  valid ID token), `api_key(header_name=)`, `manual_token`,
  `manual_credentials`, `toolbox_identity` (no auth, local only) and
  `from_adk_auth_config` / `from_adk_credentials`; the default protocol is
  MCP 2026-07-28 with `Protocol.MCP_v2025xxxx` values to pin an older
  revision. On adk-python main `ToolboxToolset` takes
  `credentials: CredentialConfig | None` (source-verified, `tools/toolbox_toolset.py`,
  ed76f94).

- Application Integration on Agent Runtime: the research notes that the
  execution role must be `roles/integrations.integrationEditor` rather than
  `integrationInvoker` to avoid 403s, that `ExecuteConnection` needs the
  integration name, and that the connector must be in the same region. Confirm
  against the current Application Integration documentation.

## Registration checklist

- Card passes `agent_card_check.py` with no `error` checks; `review` items
  read by the owner; `gemini_enterprise.missing` empty when registering
  there.
- Advertised URL is the public https URL (no trailing slash; the ADK builder
  strips one) and resolves from outside the VPC if the registry needs it.
- `securitySchemes` matches what the edge enforces; the Discovery Engine
  service agent (Gemini Enterprise) or the calling principal (Runtime, your
  own callers) has the invoker role. Granting it is an approval.
- Protocol version on the card matches what the server really speaks; 0.3
  compatibility is on when Gemini Enterprise is the caller.
- A live `message/send` from the platform (or `curl` with the same token)
  reaches a `completed` task and is recorded as live evidence with the date.
- Registration mode matches the host: A2A on Cloud Run and GKE, ADK native
  preferred on Agent Runtime; a Live agent is not offered for registration.
- Deregistration and cleanup steps are written down with the owner
  (`deploy-adk-on-google-cloud`).
