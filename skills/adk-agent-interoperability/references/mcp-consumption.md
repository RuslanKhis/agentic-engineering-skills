# Consume an MCP server from ADK

Read this for mode (b). Statements are source-verified against google-adk
2.8.0 (`tools/mcp_tool/mcp_toolset.py`, `mcp_session_manager.py`,
`mcp_tool.py`, `session_context.py`) unless labelled otherwise; 2.8.0 is
this toolkit's reference baseline, not your project's pin, and a 2.8.0
statement holds on later versions unless [compatibility](compatibility.md)
or a version-labelled sentence here says otherwise. On 2.12.0 the
constructor keeps every parameter listed below and the revision the client
speaks is chosen by a feature flag, not a parameter: `ADK_ENABLE_MCP_MODERN_PROTOCOL=1`
(experimental, off by default, no effect on SDK 1.x) makes the session try
the 2026-07-28 `server/discover` path first and fall back to `initialize`
for older servers, with a one-time warning when the installed SDK has no
era probe (`features/_feature_registry.py`, `tools/mcp_tool/session_context.py`,
read 2026-10-23). A `header_provider` that raises is not caught in the
header merge (`_get_headers`, 2.12.0), so the exception surfaces through the
toolset's session call as the tool's error; failing closed there is the
right default, and the test for it is a provider that raises. The threat
model for server-supplied text, pinning by hash, token passthrough and SSRF
belongs to `adk-agent-security`; this page is the client contract.

## The constructor you are configuring

```python
McpToolset(
    *, connection_params,                 # StdioConnectionParams | SseConnectionParams | StreamableHTTPConnectionParams
    tool_filter=None,                     # list[str] | ToolPredicate(tool, readonly_context)
    tool_name_prefix=None,
    tool_list_cache_ttl_seconds=None,     # None = tools/list on every get_tools()
    errlog=sys.stderr,
    auth_scheme=None, auth_credential=None, credential_key=None,
    require_confirmation=False,           # bool | Callable over the tool arguments (+ tool_context)
    header_provider=None,                 # (ReadonlyContext) -> dict[str, str] | Awaitable[dict[str, str]]
    progress_callback=None,               # ProgressFnT | ProgressCallbackFactory
    use_mcp_resources=False,              # adds LoadMcpResourceTool
    sampling_callback=None, sampling_capabilities=None,
    elicitation_callback=None,
)
```

A bare `StdioServerParameters` is accepted but logs "not recommended" and is
wrapped with `timeout=5`. `MCPToolset` and `MCPTool` are deprecated aliases
that warn. The keyword-only signature means positional calls fail; keep the
keywords in configs too (`McpToolsetConfig` requires exactly one of the four
`*_params` fields).

## Connection params and timeouts

| Class | Fields and defaults | Notes |
| --- | --- | --- |
| `StdioConnectionParams(server_params, timeout=5.0)` | `timeout` bounds connecting and `initialize()` together (`SessionContext` docstring) | Spawns a child process with the agent's environment and identity. Agent YAML configs reject stdio servers unless `ADK_ALLOW_CONFIG_STDIO_MCP_SERVERS=1` or `_set_allow_config_stdio_servers(True)` is called (2.7.0 change, source-verified) |
| `SseConnectionParams(url, headers=None, timeout=5.0, sse_read_timeout=300.0, httpx_client_factory=...)` | Legacy HTTP+SSE transport | The MCP specification deprecated HTTP+SSE in 2025-03-26 and reclassified it as Deprecated in the 2026-07-28 revision (normative, read 2026-10-08); still served by ADK, prefer Streamable HTTP |
| `StreamableHTTPConnectionParams(url, headers=None, timeout=5.0, sse_read_timeout=300.0, terminate_on_close=True, httpx_client_factory=...)` | `timeout` is the connect timeout; `sse_read_timeout` is the httpx read timeout | Aliases `SseServerParams` and `StreamableHTTPServerParams` exist |

The same `timeout` also bounds every `tools/list` and resource call made
through `_execute_with_session` (`asyncio.wait_for`). A tool call itself
runs under `SessionContext._run_guarded`, which raises when the background
session task dies instead of hanging until the read timeout. Set
`sse_read_timeout` from the slowest legitimate tool, not from the default.

## Lifecycle: pooled sessions and what identity they carry

- `MCPSessionManager` pools one `ClientSession` per key: `stdio_session`
  for stdio, otherwise `session_<md5 of merged headers>` or
  `session_no_headers`. Merged headers are the connection params' `headers`
  plus whatever `header_provider` returned. Two users with different
  `Authorization` headers therefore get different sessions; two users with
  identical headers share one. This is the whole per-user isolation story on
  the client side.
- Idle HTTP sessions are evicted after 900 s (`_SESSION_IDLE_TTL_SECONDS`)
  unless a call is in flight; stdio sessions are never evicted by idleness.
- `retry_on_errors` retries `get_tools` and session creation once, never on
  cancellation. Session creation happens before any tool call exists, so the
  retry cannot duplicate a side effect (docstring in `mcp_tool.py`). A
  failing `tools/call` is not retried by ADK; retries of the call are
  `safe-api-tool-calls`' decision.
- Dead-session detection: `create_session` drops a pooled session whose
  streams are closed or whose background task died
  (`FeatureName._MCP_GRACEFUL_ERROR_HANDLING`, on by default; the kill switch
  env var is named in the feature registry). 2.10.0 adds "rebuild a session
  the server reports it no longer holds" (#7060) and 2.11.0 "detect a dead
  MCP session whose transport sits behind a dispatcher" (CHANGELOG). On 2.8.0
  a Cloud Run instance that scaled to zero and back can still hold a stale
  pooled session until the probe notices; a test that restarts the fake
  server between calls shows your version's behaviour.
- `__getstate__` drops live sessions, so a pickled toolset (Agent Runtime)
  reconnects lazily on first use.
- `await toolset.close()` closes every pooled session and clears the tool
  list cache. `adk web` and `adk api_server` do this for you; a custom
  Runner, worker or test must call it (documented behaviour, ADK advanced
  MCP page).

## Define synchronously, choose transport by environment

Deployment targets import `agent.py` and expect `root_agent` and its
toolsets to exist without an event loop; async factories work only under
`adk web` or your own Runner (documented behaviour, ADK deployment page).
The documented pattern selects the transport with `os.getenv("K_SERVICE")`:
Streamable HTTP with headers on Cloud Run, stdio locally. Keep both branches
behind the same `tool_filter`.

Three gotchas from Google's own ADK recipe notes (Agents CLI 1.11.0,
`google-agents-cli-adk-code` skill, `references/adk-python.md`, read 22
October 2026): the ID token for a private Cloud Run MCP server is minted for
the service root (`fetch_id_token(Request(), MCP_SERVER_URL)`), not for the
`/mcp` path, and through `header_provider` so it is refreshed per call rather
than frozen in `headers`; "agent definition must be synchronous (not async)
for deployment", the same rule as above; and the Agents CLI scaffold's
`google-adk[gcp,otel-gcp]` extras do not include `mcp`, so add the `mcp`
extra and re-lock before the first `McpToolset` import (the 1.11.0 template
pins `google-adk[gcp,otel-gcp,bigquery-analytics]>=2.12.0`, still without
`mcp`).

## Filters, prefixes and reserved names

- `tool_filter` is applied in `get_tools` through `_is_tool_selected`; a list
  matches `tool.name` exactly (before prefixing), a predicate receives
  `(tool, readonly_context)` and can vary by user or state. Without a filter
  every server tool is declared. The ADK docs say to always supply one and to
  prefer read-only filters in production (documented behaviour).
- `tool_name_prefix` is applied by `BaseToolset.get_tools_with_prefix`, so
  the model sees `pg_query` while the server still receives `query`. Use it
  whenever two toolsets could share a verb; `mcp_tool_inventory.py` reports
  `tool_name_collision` across the sources you pass it.
- Tools named `adk_request_credential`, `adk_request_confirmation`,
  `adk_request_input` or `transfer_to_agent` are skipped with a warning in
  `get_tools` (and `McpTool.__init__` raises for them). The inventory
  reports `reserved_adk_tool_name`.
- Tools are returned sorted by name (2.5.0 "stable sorted order for cache
  stability"), which also keeps prompt caches warm.

## Tool list caching

`tool_list_cache_ttl_seconds=None` lists tools on every `get_tools()`, which
is every model request. A positive TTL caches the `tools/list` result per
session-pool key (per header identity) for that many seconds, up to 64
entries, on this toolset instance. ADK does not subscribe to
`notifications/tools/list_changed`, so a tool the server adds or removes is
unseen until the entry expires (constructor docstring). The inventory
reports `server_list_changed_unsubscribed` when a server advertises the
capability. Choose the TTL deliberately: long enough to stop listing on
every turn, short enough that a reviewed manifest and the live list cannot
drift unnoticed, and remember that caching is not review; the committed
manifest is.

The 2026-07-28 specification makes `ttlMs` and `cacheScope` mandatory on
`tools/list` results (normative). ADK 2.8.0 ignores them; the inventory
records them (`list_result_ttl_ms`) so you can align the TTL with what the
server states.

## Authorization facts a consumer pins

When the server is an OAuth resource server, four rules from the
specification decide what the agent's OAuth client must do, whatever library
implements the flow (modelcontextprotocol/modelcontextprotocol commit 80041ab, `docs/specification/2025-11-25/`, read 2026-10-22); (same repository, `docs/specification/2026-07-28/`, read 2026-10-22):

- **Discovery.** Protected Resource Metadata follows RFC 9728, with the
  `WWW-Authenticate` header optional and `.well-known` as the fallback
  (SEP-985); authorization-server discovery adds OpenID Connect Discovery
  1.0; incremental scope consent arrives through `WWW-Authenticate`
  (SEP-835).
- **Registration, in this priority:** a pre-registered client id; a Client
  ID Metadata Document when the authorization server advertises
  `client_id_metadata_document_supported` (the `client_id` is an HTTPS URL
  with a path that serves a JSON document whose `client_id` matches the URL
  exactly and lists `client_name` and `redirect_uris`; `private_key_jwt` is
  allowed for token-endpoint authentication); Dynamic Client Registration
  only as a fallback, deprecated in 2026-07-28 and requiring an
  `application_type` (SEP-837) while it lasts. An agent that registers
  dynamically today should plan the move to a hosted metadata document.
- **Issuer binding.** Persisted client credentials are keyed by the issuer
  identifier, never reused with a different authorization server, and
  re-registered when the server changes (SEP-2352); a present `iss` in the
  authorization response must match the recorded issuer before the code is
  redeemed (RFC 9207, SEP-2468). Both are MUSTs on the client and belong in
  the credential index that `adk-tool-auth-and-secrets` keeps.
- **Enterprise sign-on and headless agents.** The MCP auth extensions
  (modelcontextprotocol/ext-auth commit fb374c7, MIT, read 2026-10-22) define
  Enterprise-Managed Authorization as stable: the client exchanges the
  user's ID token at the identity provider for an identity-assertion grant
  (RFC 8693 token exchange, `requested_token_type` ID-JAG, `audience` the
  resource authorization server's issuer, `resource` the MCP server's
  identifier) and presents it as an RFC 7523 JWT bearer grant to the
  resource authorization server, which lets the enterprise see and police
  every agent-to-server grant; and an OAuth client-credentials profile as a
  draft (`private_key_jwt` or `client_secret_basic`, the server metadata
  naming at least one) for agents with no user present. Prefer the stable
  profile when the server's authorization server supports it; treat the
  draft as vendor guidance to confirm against the current text. The wire
  shape of the stable profile, for the implementer: at the identity
  provider's token endpoint, `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`,
  `requested_token_type=urn:ietf:params:oauth:token-type:id-jag`,
  `subject_token` the user's ID token (or refresh token) with the matching
  `subject_token_type`, `audience` the resource authorization server's
  issuer and `resource` the MCP server's identifier; the response's
  `issued_token_type` is the ID-JAG, a JWT typed `oauth-id-jag+jwt`; at
  the resource authorization server's token endpoint,
  `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer` with the ID-JAG
  as the assertion and the client authenticating with its registered
  credentials or its metadata-document client id. The profile defines no
  refresh-token handling, so the client re-exchanges rather than storing a
  vendor refresh token; cache lifetime, single flight per principal and
  failure classes belong to `adk-tool-auth-and-secrets`' lifecycle
  reference. A headless client's metadata document still has to list
  `redirect_uris` (the document's required fields); list one HTTPS URI on
  your own host and record it as unused.

## Headers and credentials: the client contract

Three header paths merge before a session is created:

1. `connection_params.headers`: static, shared by every user, part of the
   pool key. Fit for an agent-level API key held by the deployment, never
   for a user's token.
2. `auth_scheme` and `auth_credential` (`BaseAuthenticatedTool`): ADK
   exchanges the credential and builds `Authorization` or an API-key header;
   only header-based API keys are supported (`McpTool._get_headers` raises
   for query or cookie). `credential_key` names the stored credential.
   `adk-tool-auth-and-secrets` owns the OAuth flow.
3. `header_provider(readonly_context)`: called on `get_tools` and on every
   tool call with a fresh `ReadonlyContext`; may be async; its result is
   merged last and so wins. It is the right place for a per-user token from
   state or a refreshing service credential (2.11.0 fixed a sample whose
   static ADC header expired after an hour, #7217).

Contract consequences of the MCP Security Best Practices (revision
2026-07-28, supplied by research 2026-10-08, confirm before quoting): a
server MUST NOT accept tokens not issued for it, so `header_provider` must
carry a token minted for that MCP server's audience, never the token the
user gave your agent; per-client consent means your agent is the client,
and it must not let one user's session key serve another. On 2.8.0 the
session manager also tries to configure Google mTLS with
`google.auth.default` for any HTTP connection and, when mTLS is available,
injects a bearer for the target host if no `Authorization` header is
present (`_get_mtls_transport`, `_RefreshableAsyncCredentials`); 2.9.0 and
2.10.0 narrow that bearer to Google API hosts over https (CHANGELOG
f9f4a39, 5a018c9). Set `GOOGLE_API_USE_CLIENT_CERTIFICATE=false` on 2.8.0
when the MCP host is not Google's and you do not want ADC offered to it.

## Google's managed remote MCP servers

Google runs two kinds, and only one is governed by IAM (Google Cloud
documentation, MCP overview and supported products, last updated
2026-10-22, read 2026-10-24). Google Cloud MCP servers (BigQuery at
`https://bigquery.googleapis.com/mcp`, Cloud SQL at
`https://sqladmin.googleapis.com/mcp` and many more; some are regional, such
as `https://apihub.REGION.rep.googleapis.com/mcp`) support MCP
2026-07-28, need `roles/mcp.toolUser` (permission `mcp.tools.call`) beside
the data roles, and can be restricted with IAM allow and deny conditions
(`adk-sql-agent-engineering` carries the read-only deny). A deny stops the
call, not the listing: `tools/list` still advertises the write tools, so
pair it with a `tool_filter`. Authenticate with a `header_provider` that
mints the runtime identity's OAuth token per request (the BigQuery server
asks for the `https://www.googleapis.com/auth/bigquery` scope); `tools/list`
itself needs no authentication on that server. Google's other
remote MCP servers (Maps Grounding Lite at
`https://mapstools.googleapis.com/mcp`, Developer Knowledge, the Workspace
servers in Developer Preview and others) "don't require" that role, and
"you also can't use IAM policies or permissions to control access to" them,
so for those the agent's `tool_filter` and egress policy are the only gates
on which tools it may call. Take the list from the supported-products page
with its date, not from the google/mcp repository, which calls itself
demonstration material and lists a fraction of the servers.

## Google-hosted MCP servers on API Gateway

API Gateway can serve an OpenAPI 3.x REST API as a stateless remote MCP
server at `POST https://<defaultHostname>/mcp` (Public Preview;
https://docs.cloud.google.com/api-gateway/docs/mcp-configure, read
2026-10-21). Client facts that change your `McpToolset`:

- `tools/list` is "by default ... unauthenticated" until the spec names
  exactly one JWT or API-key scheme under
  `x-google-api-management.mcp.tools-list.security`; `tools/call` inherits
  the REST operation's `security`, so a quota-bearing operation needs
  `x-api-key` as well as the JWT. Send `MCP-Protocol-Version: 2025-11-25`
  after `initialize` or the gateway falls back to `2025-03-26`.
- No `Mcp-Session-Id`, no SSE `GET`, no annotations (`readOnlyHint`,
  `destructiveHint`), text responses only; a JSON request body travels under
  `arguments.body`. Tier these tools from your own review.
- OpenAPI `in: header` parameters are exposed as tool arguments and injected
  into the backend request, so a server that declares an identity or tenant
  header as a parameter has handed it to the model; `x-google-mcp-tool: false`
  removes a route from MCP but leaves its REST path live (Google's
  `api-gateway-backend-security-and-rate-limiting` skill, read 21 October
  2026).
- An invalid API key on `tools/list` can return HTTP 200 with JSON-RPC error
  `-32000`; check the JSON-RPC `error` field, not only the status (same
  skill).
- The credential still goes through `header_provider`, minted for the
  gateway's audience and refreshed before expiry; a Google ID token is
  short-lived, and a static `connection_params.headers` entry would share one
  user's token across every session.

When that gateway must be created, annotated or secured, consult the
installed Google skills `api-gateway-mcp-server` and
`api-gateway-backend-security-and-rate-limiting` (from google/skills); if
they are not installed, adk-engineer explains how to get them.

## Confirmation and results

<!-- shared:tool-confirmation -->
**ADK tool confirmation mechanics** (google-adk 2.8.0 and 2.12.0 source, read
2026-10-27; confirm on the installed version):

- `FunctionTool(func, require_confirmation=True)` asks before every call;
  `require_confirmation=` also takes a callable, so the threshold lives in code
  that sees the arguments, not in the prompt. `McpToolset(require_confirmation=...)`
  applies the same to server tools.
- On `FunctionTool` the callable is invoked with the tool function's own
  validated arguments as keyword arguments, plus the context parameter only
  when the tool function declares one, so its parameters must match the
  function's. On `McpTool` it receives the tool arguments plus `tool_context`
  when the callable's own signature names it (or takes `**kwargs`). Sync and
  async callables both work.
- Return a strict `bool`. `None` or another falsy value lets the call run
  unconfirmed (community report #7010), and from 2.10.0 the framework's gate
  holds a call only on exactly `True`.
- Order on 2.12.0 (`flows/llm_flows/tools/_caller.py`): the plugin's
  `before_tool_callback`, each agent `before_tool_callback` in order, the
  confirmation gate, then the tool body. The confirmed resume re-dispatches the
  original call through the same path, so a `before_tool_callback` runs again
  and may refuse it. A bound that must hold whatever the model or the approver
  does lives in the tool body or the store, with the callback as the early
  refusal.
- With no confirmation attached, the call returns `{"error": "This tool call
  requires confirmation, please approve or reject."}`, sets
  `skip_summarization` and records a request through
  `tool_context.request_confirmation(hint=..., payload=...)`, keyed by the
  `function_call_id` (which must be present). A rejected confirmation returns
  `{"error": "This tool call is rejected."}` and the body never runs: report
  it as a cancellation with no attempt, not as an unknown outcome.
- Inside a tool, `tool_context.request_confirmation(hint=, payload=)` pauses
  with a message and the structure the approver must return; the reply
  arrives as `tool_confirmation.payload`. Below 2.10.0 a custom `BaseTool` must
  check `tool_context.tool_confirmation.confirmed` itself; from 2.10.0 the
  framework holds any tool whose `check_require_confirmation` answers `True`,
  and `BaseTool`'s default answers `False`, so a custom tool overrides that
  hook.
- The client answers with a `function_response` named
  `adk_request_confirmation` whose `id` is that request's `function_call_id`
  and whose `response` holds `confirmed` and `payload`; with resumability it
  also carries the original `invocation_id`. On 2.12.0 the framework refuses a
  confirmation whose original call's name or arguments differ from the call in
  history (`flows/llm_flows/tools/_confirmation.py`).
- The answer must come from the authenticated controlling user through the
  application's API, never from A2A, an unauthenticated `/run` or text the
  model wrote. Confirmation records consent; it does not authenticate the
  caller or grant business permission. Forged confirmation responses in
  history were fixed in 2.5.0 and 2.6.0; 2.11.0 adds HMAC stamps with
  `ToolCallIntegrityPlugin`.
- ADK 2.12.0 runs a confirmed tool once per approval (CHANGELOG, bfdeb4a,
  closes #7434); below 2.12.0 a re-sent approval could run the tool again. The
  resume page warns that long-running functions may run more than once when
  resuming. On every version, test a duplicate approval reply and keep an
  operation record or idempotency key: it, not the framework, makes a repeated
  approval converge on one effect.
- 2.12.0 accepts `require_confirmation` on workflow nodes (`@node`,
  `FunctionNode`; 988fd1a), so a gate can sit on the node rather than inside a
  tool; it is absent on 2.8.0. From 2.9.0 a failed node re-runs on resume, so a
  confirmed node whose body writes externally still needs the idempotency key.
- The confirmation page (adk.dev, read 2026-10-22) lists
  `DatabaseSessionService` and `VertexAiSessionService` as unsupported. With a
  persistent session store, a decision that may take hours, another person
  deciding, or completion that must survive restarts, use a durable review
  record instead of the in-session confirmation; approval is permission, not
  completion.
<!-- /shared:tool-confirmation -->

When to require confirmation is `adk-operational-guardrails` territory and
the threat model `adk-agent-security`'s.

- Results come back as `response.model_dump(exclude_none=True, mode="json")`,
  so the model sees `content`, `structuredContent` and `isError` as the
  server sent them. An MCP error (`McpError`) or unexpected exception is
  returned as `{"error": ...}` under the default graceful-handling flag
  rather than raised. Validate `structuredContent` against the tool's
  `outputSchema` in `after_tool_callback` when the server supplies one; the
  specification says clients SHOULD (documented behaviour, tools page). The
  inventory marks tools without one (`tool_without_output_schema`).
- Annotations such as `readOnlyHint` are hints from the server; the
  specification says clients must not trust them from untrusted servers.
  Derive tool tiers from your own review, not from annotations.
- `progress_callback` receives `notifications/progress` for long tools; a
  factory form gets the tool name and a `CallbackContext` to write state.
- `sampling_callback` and `elicitation_callback` answer server-initiated
  requests (SDK 1.x behaviour). The 2026-07-28 revision deprecates Sampling
  and replaces server-initiated requests with Multi Round-Trip Requests
  (`resultType: "input_required"`); see [compatibility](compatibility.md).
  With `ADK_ENABLE_MCP_MODERN_PROTOCOL=1` the connection is 2026-07-28, so a
  tool on an `mcp` 2.x or FastMCP 4 server that calls `ctx.elicit()` fails
  ("elicitation via server-initiated requests is unavailable on 2026-07-28
  connections") and `elicitation_callback` is never reached; a server meant
  for both revisions returns `input_required` instead (PrefectHQ/fastmcp
  commit 37301f9, `docs/getting-started/upgrading/from-fastmcp-3.mdx`;
  python-sdk `docs/run/legacy-clients.md`; read 2026-10-24).
- MCP Apps (the `io.modelcontextprotocol/ui` extension; modelcontextprotocol/ext-apps commit 266a9e3, `specification/2026-01-26/apps.mdx` (Stable), read 2026-10-24). After a
  call to a tool whose `_meta.ui.resourceUri`, or the deprecated
  flat `_meta["ui/resourceUri"]`, starts with `ui://`, `McpTool` adds
  `UiWidget(id=<function call id>, provider="mcp", payload={"resource_uri",
  "tool", "tool_args"})` to the event's `actions.render_ui_widgets`; the
  model still gets the ordinary tool result. ADK 2.12.0 attaches the widget
  even when the result has `isError: true`, so the renderer drops those; the
  payload's `tool` is ADK's dump of the MCP tool, whose metadata came through
  as `meta` rather than `_meta` in an offline trial, so read both. ADK never fetches or renders
  the HTML, and the `adk web` bundled with 2.12.0 does not show these
  widgets, so a UI needs a renderer ticket in `adk-frontend-integration`
  (google-adk 2.12.0 `tools/mcp_tool/mcp_tool.py`; the feature dates from
  1.27.0). Two host duties the extension assigns are not done by ADK 2.12.0.
  It does not advertise the extension: `session_context.py` builds
  `ClientSession` without the `extensions=` argument that `mcp` 2.3.0
  accepts, and servers "SHOULD check client capabilities before registering
  UI-enabled tools", so a server that does gives ADK text-only tools; run
  the inventory against the server before planning UI, where
  `mcp_app_resource_unreferenced` (an MCP App page that no listed tool points
  at) is the trace of such gating. The remedies are the vendor's (list UI
  tools regardless) or a backend MCP session of your own that declares the
  extension (`{"io.modelcontextprotocol/ui": {"mimeTypes":
  ["text/html;profile=mcp-app"]}}` in the client's `extensions`) and serves
  the view, which the frontend's renderer needs anyway; ADK's own session
  stays text-only. The manifest diff counts `ui_resource_uri` and
  `ui_visibility` as definition, so a vendor that drops a tool's UI or makes
  an app-only tool visible to the model raises `rug_pull_signal`.
  And it does not apply `_meta.ui.visibility`: `McpTool.visibility` exists
  but nothing reads it, while the extension says a host "MUST NOT include
  tools in the agent's tool list when their visibility does not include
  `"model"`". Drop app-only tools with `tool_filter` (the inventory flags
  them as `mcp_app_tool_not_for_model`), and have the backend refuse a
  view-initiated call to a tool whose visibility lacks `"app"`.

## Debugging what crossed the wire

At `DEBUG` log level the HTTP exchanges land in
`custom_metadata["http_debug_info"]` with `Authorization`, cookies and API
keys redacted (`_redact_headers`) and bodies truncated to 1000 characters.
With `ADK_EXPERIMENTAL_TELEMETRY` the same exchanges become OTel log records
(`adk.experimental.mcp.http.client.response.end`). Trace context is
injected into `_meta` on each `tools/call` so a server that honours it
joins your trace (`adk-agent-observability`).

## Checklist for one toolset

- Transport chosen by environment; `timeout` and `sse_read_timeout` set from
  measured tool durations.
- `tool_filter` lists names (read-only in production unless a write is
  tiered and gated); `tool_name_prefix` set when more than one toolset.
- Manifest from `mcp_tool_inventory.py --out` committed; a test diffs the
  live list against it.
- Credentials through `header_provider` or `auth_scheme`; nothing shared
  across users in `connection_params.headers`; no passthrough of the user's
  upstream token.
- `tool_list_cache_ttl_seconds` decided and written down with its reason.
- `close()` called by whoever owns the Runner.
- A fake MCP server test covers: normal result, `isError` result, server
  down, server restarted between calls, slow tool past `sse_read_timeout`
  ([evaluation-across-boundaries](evaluation-across-boundaries.md)).
