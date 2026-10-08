# Consume an MCP server from ADK

Read this for mode (b). Statements are source-verified against google-adk
2.8.0 (`tools/mcp_tool/mcp_toolset.py`, `mcp_session_manager.py`,
`mcp_tool.py`, `session_context.py`) unless labelled otherwise. The threat
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

## Confirmation and results

- `require_confirmation=True` makes every tool request confirmation;
  a callable receives the tool arguments (plus `tool_context` if it accepts
  one) and must return a strict `bool`. On 2.8.0 the check lives in
  `McpTool.run_async`: without a confirmation it calls
  `tool_context.request_confirmation(...)` and returns an error dict; a
  rejected confirmation returns `{"error": "This tool call is rejected."}`.
  The hold mechanics and forgery fixes are `adk-operational-guardrails` and
  `adk-agent-security` territory.
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
- MCP App UI resources (`_meta.ui.resourceUri`) are rendered as a
  `UiWidget` after the call; `adk-frontend-integration` owns the renderer.

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
