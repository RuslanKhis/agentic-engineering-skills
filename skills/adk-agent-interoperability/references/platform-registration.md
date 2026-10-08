# Host and register an A2A agent on Google Cloud

Read this for mode (f) after [a2a-contracts](a2a-contracts.md). Everything
here is vendor guidance from Google documentation supplied by research on
2026-10-08 unless marked read or source-verified; product names and paths
change, so confirm each row on the live page before quoting it to an owner.
Deployment mechanics (build, IAM bindings, service accounts, cleanup) belong
to `deploy-adk-on-google-cloud`; this page lists what the A2A boundary needs
from the platform.

## Where the agent runs and what serves the card

| Host | How A2A is served | Card discovery | Auth to reach it |
| --- | --- | --- | --- |
| Your container (Cloud Run, GKE) with `to_a2a` or `adk api_server --a2a` | Starlette routes from `_compat.attach_a2a_routes_to_app` (source-verified) | `/.well-known/agent-card.json` (or `/a2a/<folder>/.well-known/agent-card.json`) served publicly by the app | Whatever the edge enforces: Cloud Run IAM (`--no-allow-unauthenticated`), IAP, or in-app validation of the header the card declares |
| Agent Platform Runtime (formerly Agent Engine), A2A template, Preview | `vertexai.agent_engines.templates.a2a.A2aAgent(agent_card=..., agent_executor_builder=...)`; operations `on_message_send`, `on_get_task`, `on_cancel_task`, `handle_authenticated_agent_card`; endpoint `.../reasoningEngines/{id}/a2a` (community post 2025-09-10 and current docs under gemini-enterprise-agent-platform/scale/runtime/use-an-a2a-agent) | The public well-known card is **not** served; clients GET `{a2a_url}/v1/card` with a bearer ADC token. `agent_card_check.py --url <a2a_url> --card-path /v1/card --header "Authorization=Bearer $(gcloud auth print-access-token)" --allow-remote` after approval | Google IAM on the Reasoning Engine; `cloud-platform` scope for the caller |
| Gemini Enterprise (registered external A2A agent) | Gemini Enterprise calls your endpoint; traffic does not pass Agent Gateway, so its policies do not apply | Card JSON supplied at registration (`a2aAgentDefinition.jsonAgentCard`) | Cloud Run: Google-signed OIDC token for the Discovery Engine service agent in `X-Serverless-Authorization`; grant that service agent `roles/run.invoker`. End-user OAuth (when configured) arrives in `Authorization` |

Agent Runtime consequence: `RemoteA2aAgent(agent_card="https://.../a2a/.well-known/agent-card.json")`
cannot resolve a Runtime-hosted peer; pass the card as a file or object and
install an auth interceptor (or `auth_scheme`) that adds the bearer to both
the card request and message sends. Remember that a file card skips the
https and same-origin validation, so you own the target check.

## Gemini Enterprise registration (docs page last updated 2026-10-05, read 2026-10-08)

Required card fields: `protocolVersion`, `name`, `description`, `url`,
`version`, `defaultInputModes`, `defaultOutputModes`, `capabilities`,
`skills`. `agent_card_check.py` reports them under `gemini_enterprise` and
flags a missing top-level `url` on a 1.0-shaped card. Gemini Enterprise
"supports the A2A v0.3 streaming mechanism"; a 1.0.0 or later server must
offer the compatibility layer (`a2a.compat.v0_3` in the Python SDK; ADK's
`attach_a2a_routes_to_app(enable_v0_3_compat=True)` is the default on the
1.x path, source-verified). Registration uses the REST methods
`agents.create`, `agents.patch` and `agents.delete`. Model Armor and other
gateway policies must be applied inside the agent because this traffic
bypasses Agent Gateway (`protect-adk-sensitive-data` configures them). A
community thread (discuss.google.dev 325331, January 2026) reports a
same-project constraint that blocks registering an agent hosted in another
project; a cross-project A2A hop from a same-project agent is the workaround
people describe. Treat as community report.

## Agent Registry and Agent Gateway (vendor guidance, confirm commands)

- Agent Registry stores cards and MCP server specs:
  `gcloud agent-registry services create --agent-spec-type=a2a-agent-card
  --agent-spec-content=agent-card.json` (10 KB card cap reported). ADK's
  `AgentRegistry.get_remote_a2a_agent()` and `get_mcp_toolset()` exist in
  2.8.0 (`integrations/agent_registry/agent_registry.py`, source-verified
  method names) and need `google-adk[a2a,agent-identity]`; 2.11.0 resolves
  registry MCP bindings for a deployed agent at runtime (CHANGELOG 9115d61).
- Agent Gateway egress (2026 codelab): deploy with
  `identity_type=AGENT_IDENTITY` and an `agent_to_anywhere_config`, register
  MCP servers with `--mcp-server-spec-content` and
  `--interfaces=url=...,protocolBinding=JSONRPC`, grant `roles/iap.egressor`
  with a CEL condition on `iap.googleapis.com/mcp.toolName`, allow an empty
  tool name so `initialize` and `tools/list` pass, and start in `DRY_RUN`.
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
- Deregistration and cleanup steps are written down with the owner
  (`deploy-adk-on-google-cloud`).
