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
| A2A 1.0.1 (2026-05-26) prefers the `application/a2a+json` media type in the HTTP binding (#1753); 1.0.0 (2026-03-12) removed the implicit and password OAuth 2.0 flows from security schemes and added device code and PKCE (#1303), renamed `supportsAuthenticatedExtendedCard` to `supportsExtendedAgentCard` and moved `extendedAgentCard` into `AgentCapabilities` (#1222, #1307) | A2A `CHANGELOG.md`, read 2026-10-22; a2a-sdk 1.2.3 on PyPI 2026-10-19. A card that still declares an implicit or password flow is a 0.3 card; `adk-tool-auth-and-secrets` owns the flow the client implements |
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

On 2.12.0 the same signature carries two more keyword parameters,
`security_schemes: dict[str, SecurityScheme] | None` and
`default_skill_security: list[dict[str, list[str]]] | None`, so the generated
card can declare its schemes without a hand-written card (signature read in
the installed 2.12.0 package with a2a-sdk 1.2.3, 2026-10-23).
`default_skill_security` puts the requirement on each generated skill and
leaves the card-level `securityRequirements` empty by design (so a tool can
override it through `custom_metadata['security']`; `agent_card_builder.py`
docstring); a caller or registry that reads only the card-level list sees no
requirement, which `agent_card_check.py` reports as
`security_requirements_missing`, so add a card-level requirement when you
hand in or post-process the card. The 1.0 card
shape, as a2a-sdk 1.2.3 serialises it (protobuf JSON, read the same day):
`supportedInterfaces[]` entries carry `url`, `protocolBinding` and
`protocolVersion` (no top-level `url` or `protocolVersion`);
`securitySchemes` is a map from the author's scheme name to a wrapper that
names the kind (`oauth2SecurityScheme`, `httpAuthSecurityScheme`,
`apiKeySecurityScheme`, `openIdConnectSecurityScheme`, `mtlsSecurityScheme`);
the requirement list is `securityRequirements[].schemes` mapping the scheme
name to `{"list": [scopes]}`; `signatures` and `iconUrl` are optional. A
complete example lives in [assets/agent-card-1.0.example.json](../assets/agent-card-1.0.example.json)
beside the 0.3 template, and `agent_card_check.py` accepts both shapes.

- `host`, `port` and `protocol` only shape the **advertised** RPC URL
  (`{protocol}://{host}:{port}{prefix}`; 2.12.0 advertises it without a
  trailing slash); nothing binds a socket. Serve with
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
  `securitySchemes` demand; no user token of yours is forwarded. Pin the
  peer's origin as well: the a2a-sdk client takes the endpoint the card
  declares and "never compares that host against the URL the card came
  from", so a hostile or compromised card can aim your authenticated request
  at a third-party host; agents-cli's A2A client rewrites every advertised
  endpoint back onto the card's origin and attaches credentials per request
  for that reason (google/agents-cli main, `src/google/agents/cli/run/_a2a_pinning.py`,
  read 2026-10-22; vendor code, not executed). On ADK, `RemoteA2aAgent`'s own
  same-origin check on RPC URLs (2.7.0) covers the card it fetched; a raw SDK
  client in your code does not get it for free. When the peer signs its
  card, follow [signed agent cards](#signed-agent-cards): passing a verified
  card object to `RemoteA2aAgent` switches that origin check off.
- Fake-server test covers completed, failed, rejected, input-required,
  auth-required, stream cut and HTTP 401/403/5xx.

Producer:

- Authenticate inbound calls yourself; `to_a2a` serves whatever the card
  declares and verifies nothing. The recipe this skill owns for the boundary
  (the token lifecycle on the caller's side belongs to
  `adk-tool-auth-and-secrets`): a Starlette authentication middleware in
  front of the `to_a2a` app verifies the bearer token with the pinned
  library against the issuer's JWKS, checks `iss`, `aud` (the served
  origin), `exp` and `nbf` with a small leeway, the scope the card's
  requirement names and a subject; answers 401 with `WWW-Authenticate` for
  a missing or invalid token, 403 for a valid token without the scope, and
  503 when the verifier cannot reach its keys; leaves only the well-known
  card unauthenticated; and sets `request.scope["user"]` to an
  authenticated user whose name is the principal. That last step is how the
  principal reaches ADK: a2a-sdk's HTTP routes build the call context's
  user from `request.scope["user"]` (`server/routes/common.py`, 1.2.3) and
  ADK 2.12.0's request converter takes the ADK user id from that user only
  when it `is_authenticated`, otherwise ignores the claimed name once with a
  warning and runs the call as `A2A_USER_<context_id>`
  (`google/adk/a2a/converters/request_converter.py`, `_get_user_id`, read
  2026-10-23), so sessions, `user:` state, artifacts and memory are scoped
  to a verified principal or to the conversation, never to a name the caller
  merely asserted.
- The A2A project's TCK (a2aproject/a2a-tck v0.2.5, commit 5daf014;
  Apache-2.0; `README.md`, `run_tck.py`, `tck/requirements/*.py`,
  `scenarios/core_operations.feature`, `tck/transport/jsonrpc_client.py`,
  read 2026-10-22; not run here, see below) is the acceptance check for the
  card and versioning requirements of an exposed agent. Run it scoped,
  against a local `to_a2a` instance, never against Agent Runtime or a
  registered endpoint: `./run_tck.py --sut-host http://127.0.0.1:$PORT
  --level must -- -k 'agent_card or versioning'`. It fetches the card from
  `{sut-host}/.well-known/agent-card.json`, drives each interface the card's
  `supportedInterfaces` declares, treats MUST as a hard failure, SHOULD as an
  expected failure that does not block, MAY as skipped when the capability is
  not declared, and writes `reports/compatibility.json`,
  `compatibility.html`, `tck_report.html` and `junitreport.xml`. Most of its
  core-operation scenarios drive a scripted system under test through
  `messageId` prefixes (`tck-complete-task`, `tck-input-required`,
  `tck-reject-task` and others), which a real agent does not honour, and its
  JSON-RPC client sends only `A2A-Version` and `Content-Type`, with no
  authentication header option, so an authenticated server fails
  `AUTH-SERVER-002` by design; that is why the run is scoped and the
  deferred requirement ids are listed in the evidence. The ids worth naming in a ticket are tabled under
  [TCK ids for an exposed agent](#tck-ids-for-an-exposed-agent).
  `agent_card_check.py` checks a signed card's structure
  ([signed agent cards](#signed-agent-cards)) but not the signature itself,
  caching headers or extended-card authentication; those stay manual items
  beside its report. The TCK ships `run-tck`, `learn-requirement` and
  `diagnose-failure` skills under `.agents/skills/` that a ticket may name as
  companions. Because this programme's rules forbid executing code from a
  downloaded repository and the TCK is not published to PyPI, it was not
  run; on the pinned a2a-sdk, run the scoped command once and record the
  exit code and the deferred ids before trusting the wording above.
- Advertised URL equals the served URL; https for anything non-loopback.
- Card describes capability only; tool docstrings reviewed; `securitySchemes`
  and `capabilities` set deliberately; `protocolVersion` present. A signed
  card is signed once at startup ([signed agent cards](#signed-agent-cards)).
- Persistent `task_store` and shared session service when more than one
  instance runs; `lifespan` disposes what it opens.
- `tenant` on an interface is an opaque routing string (the specification's
  `AgentInterface.tenant` defines no format or meaning), a2a-sdk 1.2.3's
  client copies the card's value into every request
  (`client/transports/tenant_decorator.py`), and ADK 2.12.0 does nothing
  with it. Derive the tenant from the verified principal, never from the
  request field. One task store per sub-path, the shape of the a2a-samples
  `multitenancy` sample (which has no authentication), routes callers but
  does not isolate callers who share a path.
- Approvals cannot be satisfied by inbound A2A content (test).
- `to_a2a` needs the `a2a` extra (`google-adk[a2a]`); without it the import
  fails with `ModuleNotFoundError: a2a`. The task history the server returns
  to the caller includes the agent's tool calls and their arguments, refused
  ones too, and tool results such as document text, so decide what an
  authenticated caller may see before exposing an agent that reads personal
  data (observed on google-adk 2.12.0 in an offline trial, 2026-10-24).

## Signed agent cards

A2A 1.0 lets a producer sign its card with JWS (specification §8.4,
a2aproject/A2A main 98279d6 and tag v1.0.1, read 2026-10-24). Each
`signatures[]` entry has a base64url `protected` header and a `signature`,
both required, and an optional unprotected `header`. The protected header
must carry `alg` and `kid`, `typ` should be `JOSE`, and `jku` may point at a
JWKS. The signed payload is the card without `signatures`, defaults removed,
canonicalised with RFC 8785.

Consumer, in this order:

1. ADK 2.12.0 does not verify a signature on a card it fetches by URL:
   `RemoteA2aAgent._resolve_agent_card_from_url` calls
   `A2ACardResolver.get_agent_card` without a verifier. To require one,
   resolve the card yourself with
   `get_agent_card(signature_verifier=create_signature_verifier(key_provider, ["ES256"]))`
   (`a2a.utils.signing`, needs `a2a-sdk[signing]`), let a failed check fail
   the delegation, and pass the `AgentCard` object to `RemoteA2aAgent`. The
   fetch is async, so this agent cannot be built at module level the way the
   unsigned case is: build it in an async factory the server's startup awaits
   (a Starlette or FastAPI `lifespan`, or `asyncio.run(build_agent())` before
   serving), and keep the module-level rule for everything that needs no
   fetch.
2. A card passed in as an object skips ADK's https and same-origin check on
   its RPC URLs ("a card passed in directly or read from a local file did not
   come off the network here, so its target is left to the caller"). Before
   constructing the agent, check that every `supportedInterfaces[].url` is
   https on the origin the card came from; `agent_card_check.py`'s
   `rpc_url_origin_mismatch` is the same rule. For defence in depth, give
   the agent an HTTP client that refuses any other host:
   `httpx.AsyncClient(event_hooks={"request": [guard]})`, where `guard`
   raises when `request.url`'s scheme, host or port differ from the pinned
   origin, passed as
   `RemoteA2aAgent(..., a2a_client_factory=ClientFactory(ClientConfig(httpx_client=client)))`.
3. The key provider is the trust anchor. Build it on a key set agreed out of
   band (a pinned JWKS file or a configured key host), never on the `jku`
   inside the card being verified. In an offline probe against a2a-sdk 1.2.3,
   a card re-signed with an attacker key and an attacker `jku` verified with
   a provider that follows `jku` and was rejected with a pinned one. Allow
   asymmetric algorithms only. For an unknown `kid`, raise a subclass of
   `jwt.PyJWTError`: the verifier moves to the next signature only on that
   type, so any other exception aborts verification and breaks rotation
   across several signatures. Rejecting expired or revoked keys is also the
   provider's job (§8.4.3).
4. a2a-sdk parses the card with `ignore_unknown_fields=True` before
   canonicalising, so a field outside its schema (a 0.3 `security` list on a
   1.0 card, a vendor field, an extra skill key) is not covered by the
   signature; the probe verified a card with an added field. Take nothing
   security-relevant from such fields; `agent_card_check.py` lists them as
   `signature_fields_uncovered`. A verified card's text is still the peer's
   text and stays data for your model.

Producer:

- a2a-sdk's signer (`create_agent_card_signer`) appends to the card it is
  given, and the card route hands its shared card to `card_modifier` on every
  request, so signing that card in place, as the a2a-samples sample does,
  adds one signature per request (1, 2 and 3 over three requests in the
  probe). Sign a copy. Set `alg` explicitly: without it the signer uses HS256
  and fails with an EC key. `to_a2a` (2.12.0) has no card modifier and serves
  a supplied card as it is, so on ADK sign once at startup and pass
  `agent_card=`; rotating the key is a redeploy. Load the private key from
  Secret Manager or Cloud KMS through the runtime identity; the sample
  generates one at import, which is a demo shape. With Secret Manager, store
  the PEM as the secret, read a pinned version number rather than `latest`
  so a rotation is a reviewed deploy, load it with `cryptography`'s
  `serialization.load_pem_private_key`, and publish the matching public key
  (with its `kid`) in the key set partners pin.
- Check the result with
  `agent_card_check.py --file signed.json --key-host <jwks host> --require-signature`.
  It reports a missing `protected` or `signature`, a missing or symmetric
  `alg` (`none`, `HS*`), a missing `kid`, a `typ` other than `JOSE`, a `jku`
  that is not https or sits off the card's origin and the `--key-host` list,
  unprotected header values and uncovered fields. It does not verify the
  signature; a test does that with a `create_signature_verifier` round trip
  on a key you control. For a new service there is no "before" report: check
  the generated card with `--file`, and use `--url` only where the card's
  advertised origin is the origin you fetch from, since a local `to_a2a`
  advertising its public https URL fails `rpc_url_origin_mismatch` by
  design.

Sources: a2aproject/a2a-samples at 6603ba3 (2026-08-04; Apache-2.0; quiet
since August), `samples/python/agents/sign_and_verify_agent_card` (pins
a2a-sdk 1.1.0), read 2026-10-24; a2a-sdk 1.2.3 `a2a/utils/signing.py` and
`a2a/client/card_resolver.py`; google-adk 2.12.0
`a2a/agent/_remote_a2a_agent.py` and `a2a/utils/agent_to_a2a.py`. The probe
was two scratch scripts against the installed a2a-sdk; no sample code ran.
The repository's CIBA sample is covered in `adk-tool-auth-and-secrets`.

## TCK ids for an exposed agent

From a2aproject/a2a-tck v0.2.5 (commit 5daf014, read 2026-10-22; the kit
was read, not run). "Real agent" means the check needs no scripted system
under test; "authenticated" means the check still passes when the server
requires a bearer token the kit does not send.

| Id | Level | Checks | Real agent | Authenticated server |
| --- | --- | --- | --- | --- |
| `CARD-DISC-001` | MUST | Card served at `/.well-known/agent-card.json` | yes | yes (card is public) |
| `CARD-SIGN-001`, `CARD-SIGN-002` | MUST | JCS canonicalisation before signing; `signatures` excluded from the signed content | yes, when the card is signed | yes |
| `CARD-CACHE-001` to `CARD-CACHE-003` | SHOULD | `Cache-Control` and `ETag` on the card endpoint | yes | yes |
| `CARD-EXT-001` | MUST | Extended card requires authentication | yes | yes |
| `VER-SERVER-001` to `VER-SERVER-003` | MUST | `A2A-Version` handling; an empty header means 0.3 | yes | only if the kit's unauthenticated RPC is let through, so expect failure and keep the project's own test |
| `AUTH-TLS-001` | MUST | Encrypted transport in production | deployment check | yes |
| `AUTH-SERVER-002` | MUST | Server authenticates every request | yes | fails by design (the kit sends no credential); the project's own 401 test is the evidence |
| core-operation scenarios | MUST/SHOULD | Scripted `messageId` prefixes | no | no |
