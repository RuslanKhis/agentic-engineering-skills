# Production extensions

Read only the sections relevant to the requested product. These are explicit production principles, not claims that the teaching application implements them. Turn each required guarantee into a target-specific implementation and an observable acceptance test. An audit may conclude that a capability is out of scope without building it.

## Persistence and readiness

A frontend's hosted persistence is a data boundary: assistant-ui's `useAdkRuntime({ cloud })` copies settled messages to its proprietary Assistant Cloud service unless telemetry is turned off, and self-hosting it is an Enterprise offering; do not pass `cloud` for client data without the owner's approval. Its ADK package also depends on the cloud SDK at an unpinned `*` range, so pin it in the lockfile (assistant-ui/assistant-ui commit 86040b7, MIT, `packages/react-google-adk`, read 2026-10-26; the published 0.0.40 package read, not run).

When conversation continuity is required, choose a session service supported by the pinned SDK and the target deployment. In-memory history belongs to one process; persistence and protection against concurrent writers are separate decisions. Keep conversation history, long-term memory and retrieval knowledge separate, with explicit ownership, retention and deletion policies for each store.

Implement and verify the storage boundary in this order:

1. Inspect the existing schema/version and migration mechanism. Prepare the required schema before admitting traffic; coordinate migration ownership instead of letting every serving worker race to migrate. Follow the task's approval boundary before changing an external database.
2. Construct session and network resources in worker lifespan, after any fork. Close partially initialised resources on startup failure and close owned clients on shutdown using the installed SDK's lifecycle.
3. Make readiness reflect the dependencies required to accept a conversation. A fixed health response proves process liveness only. Use bounded, non-mutating dependency checks; routine health probes should not invoke the model or a business tool.
4. Create and continue a synthetic conversation, stop the original serving process, then resume the same owned conversation from a fresh process without browser history replay. Confirm that another user cannot retrieve it and that unavailable or incompatible storage prevents readiness or admission under the declared policy.

Acceptance: the restart test retrieves stored history, rejected ownership checks invoke no model/tool, and the storage-failure path settles within its budget. The historical companion demonstrated remote-session recall after a local gateway restart; it did not establish local database migration, readiness or production retention guarantees. Add shared writer admission from the section below when more than one process can write.

## Identity and conversation access

<!-- shared:verified-principal -->
**Identity comes from a verified principal.** Verify the caller's credential
at the server (signature, issuer, audience, expiry and required claims, with
the pinned provider library) and derive one internal principal from it. An
email address, a client-sent `user_id`, a session or thread locator, an
invocation ID, a model-chosen argument, user text and editable headers or
session state never prove identity. That principal is the only source of the
ADK `user_id` on every Runner and session call, of the owner key on every
record, and of the subject every tool and credential lookup acts for. Tools
read it from trusted context (`tool_context.user_id`, `ToolContext.session.user_id`
or the pinned SDK's accessor), never from their own arguments. Create and load
sessions under it; an unknown or foreign session fails without revealing that
it exists. A verifier outage and an invalid credential both deny access; only
the invalid credential should prompt a new sign-in.

ADK's own API server (`adk api_server`, `adk web`, `get_fast_api_app()`)
authenticates no end user: the session routes take `user_id` from the path and
`/run` and `/run_sse` from the body. ADK 2.12.0's change "take the ADK user id
only from an authenticated principal" (d0c4060) applies to the A2A request
converter only; it authenticates nothing on those HTTP routes. Keep them
behind IAP or the application's verified-principal dependency, or on internal
ingress. A test that sends a different caller-supplied `user_id` checks lookup
partitioning, not cross-user security; a cross-user claim needs distinct
authenticated principals at the real boundary.
<!-- /shared:verified-principal -->

Reuse the application's identity provider and verified session. With several issuers, include the issuer in the identity mapping. Keep trusted user/tenant context separate from browser state and model-selected arguments.

Check the pinned provider's identity length, encoding and character constraints before forwarding the mapped ID. Use a stable internal ID with a persisted unique mapping from the verified issuer/subject and required tenant scope. Preserve distinctions between identities: truncating or normalising subjects merely to fit a provider field can merge callers. A deterministic digest requires an unambiguous input encoding and an explicit collision policy; it is not a substitute for verifying the claims.

Keep application thread IDs separate from provider resource IDs where their creation rules differ. A string safe to interpolate into a path is not necessarily a valid caller-selected provider session ID. Either validate the provider's actual creation constraints or persist an owned mapping between the application thread, exact remote resource and provider-generated session ID. Introducing that mapping also requires the matching browser/BFF create/resume contract. Test long identities, equal subjects from different issuers, and application-valid IDs rejected by provider creation rules. The companion's exercised browser UUIDs do not certify every string accepted by its application regex.

Apply ownership to create/resume, history, state, reconnect, rename, archive, delete and stop operations. Use the same safe not-found response where distinguishing absent and other-user conversations would leak information. A BFF needs access control for its own storage as well as Python's session access control.

Keep the gateway's workload identity separate from its verified end-user assertion. Strip incoming headers that only the trusted proxy may assert; verify signed assertions for the intended recipient. Cookie-authenticated requests need the project's CSRF protection. CORS only controls browser access, and same-origin routing is not authentication.

Enforce tool authorisation inside deterministic code. Scope database queries or external API operations to trusted tenant/account context. The model may choose a tool and propose arguments, but it does not decide permissions. Reject browser tool definitions that shadow trusted backend tools by name.

Acceptance: two synthetic users cannot access or execute each other's conversations or tools through any supported endpoint, and rejection invokes neither model nor side-effect adapter. Live identity-provider verification remains a separate test.

## Input and public output

Validate byte limits at the server edge as well as parsed message counts, text lengths, tool/state schemas and supported request forms. For a one-way new-turn bridge, require the intended fresh user turn; reject unsupported tool-result continuation, browser-defined tools, resume payloads or writable auth state rather than silently selecting an earlier user message.

Define a public author policy and tool success/error envelopes. Exclude hidden thought content. A frontend that consumes raw ADK events needs this filter in the gateway: assistant-ui's stock stream forwards thought parts, every state delta key including `app:` and `user:`, usage and grounding metadata, auth requests, and on an exception the raw message, which its client shows as text; its history adapter rebuilds the same from stored events. Keep the event shape but filter both the stream and loaded history to the public allowlist, and replace error text with fixed copy (assistant-ui/assistant-ui commit 86040b7, MIT, `packages/react-google-adk`, read 2026-10-26; the published 0.0.40 package read, not run). Consume through terminal outcome; an earlier answer is not ordinary success after a later run failure. If partial success is a product feature, give it a separate typed outcome. Validate public state values and JSON Patch operations in addition to key names.

Return fixed safe error copy, a controlled code and an opaque reference when needed. Logs and traces require an independent allowlist. Do not record prompts, credentials, raw exception strings, customer identifiers or tool payloads by default. Disabling message-content capture does not automatically redact application logs. A UUID alone does not configure distributed tracing; propagation, exporter configuration and shutdown flushing require their own integration.

Acceptance: malformed/oversized input is rejected before invocation; wrong-author/thought/private state is absent from browser output; late errors preserve failure; a synthetic private string is absent from public responses and default diagnostics.

## Deadlines and unknown outcomes

Place admission/lock waiting inside the overall request budget. Bound transport calls, retries, worker queues and stream output. Cancellation propagates, but a cancelled await or browser connection does not prove an external operation stopped.

For mutating tools, bind a stable operation key to trusted user, operation and canonical payload fingerprint. Claim it durably and atomically; repeated identical requests return the recorded result, in-progress or unresolved state. Reusing the key for different input fails. Keep the same key during recovery instead of generating a fresh one after timeout.

Commit a database mutation and its outcome record in one transaction where possible. For external effects use provider idempotency, or an outbox plus duplicate-safe delivery and reconciliation. Writing a response cache only after a separate effect leaves a crash window. A browser `Set` is not durable protection.

Retry only a transient failure of an operation whose repetition is safe, under bounded attempts and time. Status lookup or attachment to existing output must not call the agent again. UI controls should expose unresolved/in-progress state instead of making a potentially duplicated business action look like an ordinary retry.

Acceptance: a synthetic external effect occurs once across a timed-out client, duplicate request and process restart; conflicting input under the same key is rejected. Mocked effects establish application policy, not the live provider's idempotency implementation.

## Multiple writers and resource lifetime

Use shared per-conversation admission when several replicas can write. A process-local lock is insufficient. A lease needs an owner, expiry/renewal, ownership-checked release and storage-enforced fencing so a stale worker cannot commit after losing ownership.

Admission must atomically record a durable unsettled run. Keep that gate closed until bounded reconciliation confirms settlement, including when reconciliation fails or is cancelled. Lease expiry or merely withholding lease release cannot safely admit a new writer while old remote work remains unresolved. Fencing protects only writes at boundaries that enforce it; external effects still need idempotency.

Own the lease while consuming **and closing** the event stream. Returning an HTTP streaming response does not mean execution has finished. Create loop-bound SDK clients in application lifespan, retain their owning client and close partial initialisation failures. Follow the installed SDK's supported shutdown methods.

Prefer async network APIs. For unavoidable synchronous calls, use bounded workers and transport deadlines; retain a capacity slot until the underlying call actually finishes even if its awaiting request is cancelled. CPU-heavy tasks may require a separate process. An unbounded executor moves rather than removes the capacity problem.

Acceptance: different replicas cannot overlap writes; a worker resuming after lease loss cannot commit; unresolved work blocks fresh admission after lease expiry; disconnects release local resources only after bounded closure/reconciliation.

## Replay, browser tools and human approval

SSE framing supplies no durable replay. Add a retained run record, stable event IDs, monotonic sequence, authenticated attach endpoint, retention bound and expired-cursor policy before promising reconnect. Preserve identities across delivery attempts and make the browser reducer tolerate repeated events. Give tool calls and result messages distinct IDs; require exact correlation for parallel tools.

Reconnection attaches to the recorded run instead of submitting its user message again. A browser tool result or approval signal requires an authenticated authorised decision, a matching waiting run/call, a persisted continuation state and a duplicate-safe resume operation. A UI confirmation is not itself permission to perform a backend action. A client may send function calls, function responses, thought or code parts in a new message (assistant-ui checks their types only) and may batch held approval answers, cancellation stubs for pending calls and the new text in one message: allowlist part kinds, accept a function response only for a pending long-running call of the verified session, classify approval answers per part so an "unanswered approval is rejected" rule does not reject an answer sent beside text, and test a reload after approving, since answers held in the browser are lost. On google-adk 2.12.0 such a batch cannot be passed through: the Runner raises "Message cannot contain both function responses and text" (`runners.py`, read 2026-10-26), so the gateway splits it into ordered runs, the function responses first and the text after. Accept an approval only as `adk_request_confirmation` with exactly `{"confirmed": bool}` for a call still pending in the session's live history; ADK itself accepts looser shapes, so the gateway is the place to narrow them. On AG-UI, the approval reaches the server under one of two contracts, a plain tool message or a 1.0 interrupt outcome answered by `resume`; the ticket declares which, and the [AG-UI reference](ag-ui.md#choose-the-approval-contract-and-declare-it) carries the enforcement codes and tests.

Acceptance: replaying a retained tool result does not execute the tool or add a duplicate card; another user cannot attach or approve; expired/reused decisions fail safely. These services are not bundled with the skill.

## Widgets emitted by tools

When tools render interface (cards, tables, charts) beside the reply, separate deciding what to show from sending it. Google's `staged-ui-widgets` recipe has every tool write its payload into session state and return a short summary, and one `after_agent_callback` converts what was staged and emits it in a declared order, so `render_ui_widget` is called in exactly one place and a test fails any second call site (google/adk-recipes be63596, `contrib/python/staged-ui-widgets/README.md` and `app/staging/`, read 2026-10-22; vendor sample, "not production use"; pins `google-adk>=2.6.0,<3` and `a2ui-agent-sdk>=0.2.1,<0.3.0`). Two ADK facts make the split necessary, both read in the ADK source on 2026-10-22 (main commit ed76f94; confirm on the pinned version): `Context.render_ui_widget` rejects a duplicate widget id only within the current event's actions (`agents/context.py`), and each function call gets its own context, so two tools that stage the same id ship it twice whether they run sequentially or in parallel; and a callback produces an event only when it returned content or `state.has_delta()` is true (`agents/base_agent.py`), so a render-only callback with no state change emits nothing and the widgets vanish without an error. The staging record's per-widget emitted flag is therefore both the dedupe record and the state delta that forces the event out. The model never writes component JSON; converters produce it and are validated against the published schema in tests, and a re-render that is byte-identical to what is on screen is suppressed so the reply cannot announce a change the user cannot see. The replay rule above applies unchanged: a replayed widget event must not re-run the tool or add a duplicate card.

### Choose the A2UI route and say where validation runs

A2UI is still a preview: its README says "early stage public preview", v0.9.1 is the stable protocol line, v1.0 a release candidate and v0.8 legacy, and the repository moved from `google/A2UI` to `a2ui-project/a2ui` (commit b817d02, 2026-10-23, and release tag `python/a2ui-adk/v0.1.0`; Apache-2.0; read 2026-10-24). An ADK agent reaches it three ways, and each validates in a different place, so a ticket names one route and where the catalogue check runs, in one line such as `A2UI: staged converters, protocol v0.9; agent check: stateful registry against catalogue <id>; client check: MessageProcessor with STRICT_VALIDATION; demo surface: app`:

- **Staged converters** (the recipe above): tools call `render_ui_widget(UiWidget(provider="a2ui", ...))`; the provider is an opaque string, and the converters' tests are the only check. The `adk web` UI bundled with google-adk 2.12.0 reads A2UI only from `<a2ui-json>` text blocks and `a2ui` data parts and never reads `actions.render_ui_widgets`, so these widgets do not show there. The renderer in that bundle also speaks A2UI v0.8 (`beginRendering`, `surfaceUpdate`; no `createSurface`) with the standard catalogue only and logs "Unknown component type" for anything else, so no route shows custom-catalogue widgets in `adk web`, including the toolset route, whose output is a function response; the demo surface is your app, and `adk web` can still show the conversation, tool calls and staged payloads in its state view.
- **`a2ui-adk` 0.1.0 `SendA2uiToClientToolset`** (experimental): the model writes A2UI JSON into the `send_a2ui_json_to_client` tool, which repairs it with `parse_and_fix`, checks it with `validate_payload` against every active catalogue (they must share a protocol version), returns `{"error": ...}` on failure so the model can retry, and on success returns the validated JSON with `skip_summarization` set.
- **AG-UI `generate_a2ui`** in the `ag-ui-adk` middleware: it reuses only the catalogue instructions, without the agent SDK's strict payload validation, which stays with the client toolkit, and emits v0.9 operations.

Neither side checks completely by default. `validate_payload` is stateless: it sees one payload with no record of earlier ones, so an update to an existing surface is accepted against any catalogue that defines its components unless the caller passes `surface_catalog_ids`, which the toolset does not (`a2ui/utils/validation.py`). On the client, `@a2ui/web_core` 0.14.0's `MessageProcessor` keeps `validationConfig` undefined when constructed without options, and its validator then tolerates unknown components; pass a `validationConfig` (`STRICT_VALIDATION` is exported) so unknown elements, orphan components, dangling references and a missing root are refused, and send failures back to the agent as the protocol's `VALIDATION_FAILED` error with `surfaceId`, `path` and `message` (`specification/v0_9/docs/a2ui_protocol.md`). The catalogue is an allowlist only when the client enforces it: treat an inline catalogue supplied by the client as input that widens the allowlist (the docs call it "not recommended in production"), and in a multi-agent setup have the orchestrator set or check `agentDisplayName` and `iconUrl` so a sub-agent cannot pose as another service. Two further facts settle common decisions. Exposed over A2A, a staged widget travels only inside ADK's event metadata (`event.actions` serialised under the `adk_actions` key by `a2a/converters/from_adk_event.py`, 2.12.0), so a partner that does not run ADK renders nothing; sending it real A2UI messages is a separate decision. And `a2ui-agent-sdk` 0.9.0 on its own depends on `a2ui-core` 0.4, `jsonschema`, `pydantic`, `httpx`, `pyyaml` and `antlr4-python3-runtime`, with no A2A dependency, so it can be a development dependency for schema checks without touching the A2A pin; the v0.9 message schemas live in the repository's `specification/v0_9/json/` (`server_to_client.json` for what the agent sends) and the standard catalogues under `specification/v0_9/catalogs/`. On the client, `MessageProcessor`'s options take `validationConfig` beside the catalogues and the outbound listener, and the React renderer is `@a2ui/react` (its component registration was not reviewed here). The two ADK facts the staged route rests on can be proved on the pinned version with a model-free `InMemoryRunner` test: a callback that only renders and changes no state yields no event, and the staged callback emits each widget exactly once. The staged recipe still pins `a2ui-agent-sdk>=0.2.1,<0.3.0`; the agent SDK is at 0.9.0, `a2ui.adk` has moved into `a2ui-adk`, and the AG-UI middleware no longer supports the 0.2.x SDK, so moving a recipe-based app forward is a pin change, recorded in [compatibility](compatibility.md).

### Render an MCP App widget

A widget with `provider == "mcp"` comes from an MCP server's tool, and its payload carries `resource_uri`, `tool` and `tool_args`; `adk-agent-interoperability` covers how ADK attaches it and the tool filtering it needs. The renderer is this skill's ticket (modelcontextprotocol/ext-apps commit 266a9e3, `specification/2026-01-26/apps.mdx` (Stable), read 2026-10-24; `src/app-bridge.ts` and `examples/basic-host/src/sandbox.ts`):

- The browser does not hold the MCP session, so the backend reads the HTML for `resource_uri` with `resources/read` and serves it; `McpToolset.read_resource(name)` looks resources up by name, not by URI. Use a backend MCP session of its own for this, declaring the UI extension so a server that gates on it lists its UI tools and pages; check the resource's MIME type is `text/html;profile=mcp-app`. With `mcp` stdio sessions, open and close the session in the same task: one opened in a test's `asyncSetUp` and closed elsewhere fails with an anyio cancel-scope error.
- Drop widgets whose tool result had `isError: true` (ADK 2.12.0 attaches them anyway), and read the tool's metadata from the payload under `meta` or `_meta`.
- Host the view with `AppBridge` from `@modelcontextprotocol/ext-apps/app-bridge` constructed with a `null` client, register its `oncalltool`, `onlistresources` and related handlers yourself, and route them through the backend, which refuses tools whose visibility lacks `"app"`.
- Wrap the view in a sandbox proxy on a different origin from the page ("The Host and the Sandbox MUST have different origins"; A2UI's guide shows a same-origin proxy, which the specification overrides), build the content security policy from `_meta.ui.csp` with a restrictive default when it is absent and no undeclared domains, and send nothing to the view before its `initialized` notification.
- The server keeps a text result for hosts without UI, so the conversation stays readable when the widget does not render; the demo surface is your app, since `adk web` 2.12.0 does not show these widgets.

## Evidence and scope

The skill supplies an implementation workflow and offline diagnostic helpers, not a certified production framework. Report each required control as implemented/tested, existing/verified, or remaining. Preserve the user's scope: a simple JSON integration does not automatically require a replay service or a new identity platform.
