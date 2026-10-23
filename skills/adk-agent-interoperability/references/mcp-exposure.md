# Expose an ADK agent or tools as an MCP server

Read this for mode (c). Two shapes exist in google-adk 2.8.0
(source-verified `tools/mcp_tool/_agent_to_mcp.py`, `conversion_utils.py`;
documented in `docs/tools-custom/mcp-tools/agent-as-server.md`).

## Shape 1: `to_mcp_server(agent)` serves the whole agent as one tool

```python
from google.adk.tools.mcp_tool import to_mcp_server

server = to_mcp_server(agent, name=None, instructions=None, runner=None)
server.run(transport="stdio")             # or transport="streamable-http"
```

What the source does:

- Builds a `FastMCP` server (MCP SDK 1.x) and registers one tool named after
  `name` or `agent.name`, with `description=agent.description or f"Run the
  {tool_name} agent."`, taking a single `request: str`, `structured_output=False`.
  The feature is gated behind `FeatureName.MCP_AGENT_SERVER` (experimental
  decorator).
- Without `runner`, builds a `Runner` with in-memory session, artifact,
  memory and credential services; the MCP caller is always user
  `"mcp_user"`. Supply your own `Runner` when sessions must persist or when
  identity must be real.
- Keeps one ADK session per MCP connection (`WeakKeyDictionary` keyed on the
  SDK's per-connection object; falls back to one session per request when the
  SDK gives no connection handle), so successive calls on one connection form
  a conversation and separate clients never share one.
- Streams intermediate (non-final) text as `ctx.report_progress` messages;
  returns the final response as MCP content blocks (text, image, audio, or an
  embedded resource for other inline data).
- The caller chooses the transport. The ADK docs show stdio; the source
  docstring names `streamable-http` as the networked option. Both are
  FastMCP's transports, not ADK code, so their auth and session semantics
  are the MCP SDK's.

Contract consequences:

- The one tool's description is the only text a host model sees. Write it as
  a capability statement; the agent's `instruction` is not included, and the
  2.7.0 CHANGELOG entry "keep agent instructions out of the published A2A
  agent card" shows why the same discipline matters here.
- An MCP host that calls the tool is a client, not a user: its request text
  becomes the user turn of an ADK session owned by `mcp_user`. Approvals,
  confirmations and anything keyed on "the user said so" must not be granted
  on that basis; keep irreversible tools out of an agent you expose this way
  or gate them so that an MCP caller cannot satisfy the gate.
- Progress text leaks intermediate reasoning to the host; if the agent
  handles private data, set `include_contents` and sub-agent structure so
  that only the final answer is sendable (`adk-agent-security`).
- MCP SDK 2.x renames the server class: `FastMCP` is `MCPServer` and the
  old import path is gone rather than deprecated (python-sdk v2
  `docs/whats-new.md`, read 2026-10-22); the 2.11.0 source routes the import
  through a `dependencies._mcp` shim while the public return type stays
  `FastMCP` in the signature. Verify on the installed SDK before promising a
  type to callers.

## Shape 2: hand-built server around individual ADK tools

Use the MCP SDK's low-level `Server`, advertise tools with
`adk_to_mcp_tool_type(tool)` and run `await tool.run_async(args=...,
tool_context=None)` in the call handler (documented behaviour, agent-as-server
page). `adk_to_mcp_tool_type` takes the ADK declaration's
`parameters_json_schema` when present, otherwise converts the Gemini `Schema`
with `gemini_to_json_schema`; it emits `name`, `description` and
`inputSchema` only, never `outputSchema` or annotations (source-verified).
Consequences:

- Tools that read `ToolContext` (state, identity, confirmations) receive
  `None` and will fail or, worse, run unauthenticated. Expose only
  context-free tools this way, or build the context yourself from an
  authenticated caller identity.
- Add `outputSchema` and annotations by hand if your clients validate
  results; consumers of your server will otherwise see
  `tool_without_output_schema` in their inventories.
- Validate inputs server-side and rate limit: the MCP tools specification
  says servers MUST (documented behaviour, supplied by research 2026-10-08).

## Serving over the network

For Cloud Run, the ADK deployment page's pattern is a Starlette app with
`StreamableHTTPSessionManager(stateless=True)` mounted at `/mcp` (documented
behaviour). Stateless mode means no `Mcp-Session-Id` continuity across
instances, which matches the 2026-07-28 specification's direction (sessions
removed) and means a `to_mcp_server` conversation-per-connection guarantee
does not survive a scale event; use your own `Runner` with a shared session
service if conversations must persist. Authentication at the edge
(`--no-allow-unauthenticated`, IAP, Agent Gateway egress policy on the
consuming side) is `deploy-adk-on-google-cloud`'s and
`adk-tool-auth-and-secrets`' concern; this page only insists the exposed
server declares what it requires.

## Checks before publishing

- Run `mcp_tool_inventory.py --command "python my_server.py"` (or `--url`
  against the local instance) and read your own description findings; your
  consumers will.
- A test client (stdlib JSON-RPC, as the inventory does) calls `initialize`,
  `tools/list` and one `tools/call` against the server started from the same
  entry point production uses, and asserts the content blocks and the
  per-connection session behaviour you promise.
- The published description, name and schema are committed next to the
  server so a consumer's manifest diff has something to compare with. The
  helper lives in this skill, not in the project: copy
  `scripts/mcp_tool_inventory.py` into the project's tooling directory with
  its header intact (MIT), or run it from a pinned checkout of this
  collection in CI, and record which.
- Bind the address explicitly. `MCPServer.run(transport, **kwargs)` on `mcp`
  2.3.0 forwards keyword arguments to the transport runner, and
  `run_streamable_http_async(*, host="127.0.0.1", port=8000,
  streamable_http_path="/mcp", json_response=False, stateless_http=False,
  event_store=None, retry_interval=None, max_request_body_size=4194304,
  session_idle_timeout=1800, max_sessions=10000, transport_security=None)` is
  what receives them (signature read in the installed SDK on 2026-10-22), so
  `to_mcp_server(agent).run(transport="streamable-http", host="127.0.0.1",
  port=int(os.environ["PORT"]))` is the whole bind; there is no
  `settings.host` to set on 2.x. Observed on that SDK with google-adk 2.12.0:
  the server negotiates `initialize` with a 2025-06-18 client and answers
  2026-07-28 stateless requests on the same `/mcp` path, and an unknown tool
  name returns a result with `isError: true` rather than a JSON-RPC error;
  stdio framing was not exercised in that spike.
- Decide which specification revision the server speaks and write it down
  with the `mcp` major version. On 2026-07-28 (same repository, `docs/specification/2026-07-28/`, read 2026-10-22) there is no
  `initialize` handshake and no `Mcp-Session-Id`: every request carries its
  protocol version and client capabilities in `_meta`, servers must implement
  `server/discover`, list results carry `ttlMs` and `cacheScope`, every result
  carries `resultType` (`complete` or `input_required`), server-initiated
  sampling and elicitation give way to multi round-trip `input_required`
  results, SSE resumability is gone (a broken stream loses the request and the
  client re-issues it with a new id), and Roots, Sampling, Logging and the
  HTTP+SSE transport are deprecated. The SDK implements the wire changes; two
  of them change your design. First, cross-call state travels as "explicit,
  server-minted handles passed as ordinary tool arguments", so a handle the
  model sees is data: make it unguessable, bind it to the caller's identity and
  expiry, and never let it select another user's session. Second, servers
  "SHOULD return tools from `tools/list` in a deterministic order" for client
  caching and prompt-cache hits, so sort the exposed tools and keep names
  stable across deploys; the inventory manifest diff enforces that.
- Run the official conformance suite against the local instance, pinned, and
  commit its baseline (the procedure and the observed results are in
  [validation](validation.md#6-protocol-conformance-local-pinned)):

  ```bash
  npx -y @modelcontextprotocol/conformance@0.2.0-alpha.12 server --url http://127.0.0.1:$PORT/mcp --requirements 2026-07-28 --expected-failures conformance-baseline.yml
  ```
