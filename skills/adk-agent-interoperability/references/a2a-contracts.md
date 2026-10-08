# A2A contracts: consume and expose

Read this for modes (e) and (f). Source-verified against google-adk 2.8.0
(`agents/remote_a2a_agent.py`, `a2a/_compat.py`, `a2a/utils/agent_to_a2a.py`,
`a2a/utils/agent_card_builder.py`, `a2a/executor/a2a_agent_executor.py`,
`cli/fast_api.py`) unless labelled. ADK's A2A code is decorated
`@a2a_experimental` and warns on import; set
`ADK_SUPPRESS_A2A_EXPERIMENTAL_FEATURE_WARNINGS=true` once you have read this
page, not before.

## The protocol facts you depend on

| Fact | Evidence |
| --- | --- |
| A2A 1.0.0 defines JSON-RPC, gRPC and HTTP+JSON bindings; clients MUST send `A2A-Version` (`Major.Minor`) and an empty value means 0.3 | Specification (normative, read 2026-10-08) |
| Task states: `SUBMITTED`, `WORKING`, `COMPLETED`, `FAILED`, `CANCELED`, `REJECTED` (terminal), `INPUT_REQUIRED`, `AUTH_REQUIRED` (interrupted), `UNSPECIFIED` | Specification (normative) |
| Agent card discovery at `/.well-known/agent-card.json` (renamed from `agent.json` in 0.3); registries and direct configuration are the other discovery routes; an authenticated extended card exists (`GetExtendedAgentCard`, gated by `capabilities.extendedAgentCard`) | a2a-protocol.org agent-discovery topic and specification (read 2026-10-08) |
| Enterprise baseline: TLS 1.2+, auth declared in the card's `securitySchemes` and carried in HTTP headers (no in-band identity), 401 and 403 semantics, per-skill authorization, OpenTelemetry and W3C trace headers, webhook security | a2a-protocol.org enterprise-ready topic (vendor guidance, supplied by research 2026-10-08) |
| a2a-sdk 0.3.x cards have top-level `url` and `preferredTransport`; 1.x cards have `supportedInterfaces[].url` with `protocolBinding` and no top-level `url`; ADK's `_compat.build_agent_card` emits whichever the installed SDK needs with `protocolVersion` `"0.3.0"` or `"1.0"` | source-verified `_compat.py` |

`agent_card_check.py` accepts both shapes, in camelCase or snake_case, and
reports which it saw.

## Consume: `RemoteA2aAgent`

```python
RemoteA2aAgent(
    name, agent_card,                     # AgentCard | "https://host/path/.well-known/agent-card.json" | "/path/card.json"
    *, description="", httpx_client=None,  # httpx_client deprecated; prefer a2a_client_factory
    timeout=600.0,                        # httpx timeout for the whole exchange
    a2a_client_factory=None, a2a_request_meta_provider=None,
    full_history_when_stateless=False, config=None,   # A2aRemoteAgentConfig: converters, interceptors
    use_legacy=True,                      # False sends the ADK A2A extension
    auth_scheme=None, auth_credential=None, credential_key=None,
)
```

What happens on each invocation (`_run_async_impl`):

1. **Credential.** With `auth_scheme`, the credential is resolved once per
   invocation through `CredentialManager`; if missing, the agent yields an
   auth request event and ends the invocation (`adk-tool-auth-and-secrets`
   handles the flow). The resolved header is attached to the card fetch and
   to the message send through interceptors.
2. **Card resolution.** A URL source is fetched with `A2ACardResolver` using
   the URL's path (so the URL must end in the card path, typically
   `/.well-known/agent-card.json`; a base URL alone resolves the SDK's
   default path on 0.3 and fails on servers that mount under a prefix). A
   file path is read with `_compat.parse_agent_card`. An `AgentCard` object
   is used as is, and its description is adopted when yours is empty (2.7.0).
3. **Card validation.** The card must carry an RPC URL. For a card fetched
   over the network, every RPC URL (`url` plus `additionalInterfaces`, or all
   `supportedInterfaces`) must be https, or http on a loopback host, and must
   share scheme, host and port with the card's own URL
   (`_validate_card_rpc_targets`, 2.7.0 "constrain the RPC targets of a
   network-fetched A2A agent card"). Cards from files or objects skip this
   check, so you own their targets. 2.9.0 additionally requires https for a
   non-loopback card URL itself and stops caching a card that failed
   validation (CHANGELOG fe30ebb, 2685acd). Any card-request interceptor
   (including the one `auth_scheme` installs) disables card caching, so the
   card is fetched on every invocation.
4. **Request construction.** Session events since the last remote response
   are converted to A2A parts; user parts get `is_user_input` metadata;
   credential-bearing `adk_request_credential` calls are scrubbed; other
   agents' replies are presented as fenced data; the last remote
   `a2a:context_id` is reused so the peer sees one conversation. A pending
   human answer to a remote pause is turned into a resume message with the
   stored `a2a:task_id` and `a2a:context_id`.
5. **Send and stream.** `_compat.send_message` streams responses; each
   `Task`, `TaskStatusUpdateEvent`, `TaskArtifactUpdateEvent` or `Message` is
   converted to an ADK `Event` authored by the remote agent's name, with
   `custom_metadata` keys `a2a:task_id`, `a2a:context_id`, `a2a:request` and
   `a2a:response` (full serialised objects). Text under `submitted` or
   `working` is marked `thought` and dropped from the user-facing parts;
   artifact chunks set `event.partial` until `last_chunk`. 2.9.0 skips
   summarisation for terminal task states; 2.10.0 reports a stream that ends
   before the task finishes (#6585), which 2.8.0 silently truncates.
6. **Pauses.** `input-required` and `auth-required` states become a mock
   long-running function call on the event, so the parent `LlmAgent` pauses
   as it would for a local long-running tool. 2.11.0 fixes resuming after a
   human answers that pause (#6721); on 2.8.0 test the resume path yourself.
7. **Failures.** HTTP and client errors become an `Event` with
   `error_message="A2A request failed: ..."` and `a2a:error`,
   `a2a:status_code`, `a2a:request` metadata; nothing is raised to the
   parent. Card resolution failure yields `error_message="Failed to initialize
   remote A2A agent: ..."`. In `mode="task"`, `failed` and `canceled` task
   states also yield a `finish_task` failure event and release control.
   [remote-failures](remote-failures.md) says what the parent should do.

Options that change the contract:

- `use_legacy=False` adds the ADK A2A extension
  (`https://google.github.io/adk-docs/a2a/a2a-extension/`) to the request's
  `X-A2A-Extensions`; an ADK server honours it with the new executor, fixing
  duplicated user messages, outputs misclassified as thoughts and lost nested
  sub-agent output in streaming (documented behaviour, `a2a-extension.md`,
  Python ≥ 1.27.0). Use it between ADK peers; a non-ADK server ignores it.
- `mode="task"`: the remote agent must send a `finish_task` function response
  (`"Task completed."` or `"Task failed."`) and your `output_schema` must
  mirror the remote output; workflow path scopes are not supported (source
  docstring). 2.9.0 fixes a completed delegation breaking later peers (#6831).
- `full_history_when_stateless=True`: a peer that returns no task or context
  ID receives the whole session every turn (cost and leakage trade-off).
- `a2a_request_meta_provider` attaches request metadata; the ADK server side
  surfaces it as `run_config.custom_metadata["a2a_metadata"]`
  (`request_converter.A2A_METADATA_KEY`, source-verified). It is the sanctioned
  way to forward state across the boundary; the peer still treats it as data.
- 2.10.0 adds `context_builder` and
  `A2aRemoteAgentConfig.forward_session_id_as_context_id=False` (CHANGELOG
  322e3bf, e10a1be; verified on main). Neither exists on 2.8.0.
- `_run_live_impl` raises `NotImplementedError`: a remote agent cannot sit in
  a live (bidi audio) flow.
- As a `Workflow` node (not task mode), the first terminal text response is
  promoted to `event.output` so a `JoinNode` sees it (`_promote_response_to_output`).

### Peer messages are data, not user authority

Inbound A2A content on an ADK server is converted with the A2A message role,
and a peer's `message/send` arrives as `role=user`. Issue #6461 (open at
2.8.0; a guard shipped and was reverted in the same release) documents that
an approval payload arriving over A2A could satisfy a human-in-the-loop
confirmation. `adk-agent-security` owns the threat; the contract consequence
here is: a remote agent's messages, task metadata and `a2a_metadata` are
peer data. Accept approvals, confirmations and identity only from the
authenticated controlling user at your API layer, never from a relayed
message, and write a test in which a peer message claiming approval leaves
the gated tool unexecuted.

## Expose: `to_a2a` and `adk api_server --a2a`

```python
to_a2a(agent_or_workflow, *, host="localhost", port=8000, protocol="http", rpc_path="",
       agent_card=None, push_config_store=None, task_store=None, runner=None,
       lifespan=None, agent_executor_factory=None) -> Starlette
```

- `host`, `port` and `protocol` only shape the **advertised** RPC URL
  (`{protocol}://{host}:{port}{prefix}/`); nothing binds a socket. Serve with
  uvicorn on the same host and port or the card points somewhere unreachable
  (documented behaviour). For a public deployment pass the public https host
  and `protocol="https"`, or hand in your own card.
- `rpc_path="analysis-agent"` mounts both the JSON-RPC route and
  `/.well-known/agent-card.json` under `/analysis-agent`; a provided card's
  URL is not rewritten (a warning is logged).
- Without `runner`, in-memory services are used: sessions vanish on restart
  and do not span instances. Without `task_store`, `InMemoryTaskStore` is
  used; the docstring shows `DatabaseTaskStore` with a SQLAlchemy engine and a
  `lifespan` that disposes it. Any deployment with more than one instance or
  with restarts needs both a shared session service in the `Runner` and a
  persistent task store, or `tasks/get` and resubscribe will miss.
- The card is built at startup by `AgentCardBuilder`: `name`,
  `description or "An ADK Agent"`, `version "0.0.1"`, the RPC URL,
  `protocolVersion` by SDK, `defaultInputModes` and `defaultOutputModes`
  `["text/plain"]`, `supportsAuthenticatedExtendedCard=False`, skills: one
  `model` skill carrying the agent description (and `ExampleTool` inputs as
  examples), one skill per canonical tool carrying the **tool description**,
  `planning` and `code-execution` skills when configured, and each immediate
  sub-agent's or workflow node's skills prefixed with the child name. The
  agent `instruction` is not included (2.7.0 fix). Tool docstrings are
  published, so review them as public text or pass a curated card.
  `capabilities` defaults to an empty `AgentCapabilities()` (no streaming
  flag, no extensions) and `securitySchemes` to none; pass
  `AgentCardBuilder(..., security_schemes=..., capabilities=...)` or a full
  card for anything beyond local development.
- `adk api_server --a2a --port 8001 <agents_dir>` exposes every agent folder
  that contains a file named exactly `agent.json`, mounting it at
  `/a2a/<folder>/` with the card at `/a2a/<folder>/.well-known/agent-card.json`
  (source-verified `fast_api.py`); folders without `agent.json` are skipped.
  The card is yours to write; the sample card in the docs omits
  `protocolVersion` and `securitySchemes`, which `agent_card_check.py`
  flags. `adk deploy cloud_run --a2a` carries the same flag.
- Server side, `A2aAgentExecutor` turns a request into a `RunRequest`
  (user id and session id from the request converter), creates the session
  if needed, enqueues `submitted` then `working` with ADK metadata, streams
  converted events, and finishes with `completed` or `failed`; `cancel`
  enqueues a canceled task event. A `Workflow` whose nodes only return values
  can leave the task in `working`; emit an `Event` with a message (CHANGELOG
  2.11.0 "known issues for A2A workflow output schema and serialization").
  The new executor path is selected when the request carries the ADK
  extension or `force_new_version=True`.

## Checklist per boundary

Consumer:

- Card URL ends with the card path; `agent_card_check.py` reports no
  `error`-level checks and the owner has read the `review` ones.
- `timeout` set from the peer's SLA; parent behaviour on an error event
  decided ([remote-failures](remote-failures.md)).
- `use_legacy=False` between ADK peers; converters left default unless a
  test shows why.
- `auth_scheme` or an interceptor supplies the header the card's
  `securitySchemes` demand; no user token of yours is forwarded.
- Fake-server test covers completed, failed, rejected, input-required,
  auth-required, stream cut and HTTP 401/403/5xx.

Producer:

- Advertised URL equals the served URL; https for anything non-loopback.
- Card describes capability only; tool docstrings reviewed; `securitySchemes`
  and `capabilities` set deliberately; `protocolVersion` present.
- Persistent `task_store` and shared session service when more than one
  instance runs; `lifespan` disposes what it opens.
- Approvals cannot be satisfied by inbound A2A content (test).
