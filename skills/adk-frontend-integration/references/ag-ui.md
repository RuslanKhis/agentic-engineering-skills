# AG-UI and CopilotKit

Use this mode when the browser needs progressive text or application-owned tool displays. Preserve an existing AG-UI implementation if it already serves that purpose. Confirm the exact SDK/import surface in [compatibility.md](compatibility.md).

## Build the vertical path

1. Define an application agent identifier and use the same value in the browser hook/provider, CopilotKit Runtime registry and adapter. It need not equal the model's name. Define the allowed backend tool names, input schemas, result schemas and state projection first.
2. For local ADK, adapt the existing agent with the pinned `ag-ui-adk` API and attach it to the existing ASGI app. In the recorded stack these are `ADKAgent` and `add_adk_fastapi_endpoint`. Authenticate the endpoint before starting a run and verify how the adapter resolves its user/session identity. The book's fixed demo `user_id` is not a multi-user design; implement request-scoped verified identity for a real app.
3. Keep provider credentials in the server. A Next.js backend-for-frontend forwards to Python; it must authenticate each browser caller and forward a separately verified user assertion when needed. A module-level shared backend token identifies the gateway only. Never mutate a singleton client's headers with one request's user identity.
4. In the recorded CopilotKit stack, the route imports `HttpAgent` from `@ag-ui/client` and `CopilotRuntime` / `createCopilotRuntimeHandler` from `@copilotkit/runtime/v2`. Register the selected agent with its backend URL, pass the runtime and `/api/copilotkit` base path to the handler, and export the HTTP methods required by the installed version. Verify these imports against target pins instead of mixing examples from another major version.
5. Mount the client's matching agent and a server-tool renderer. Render components written by the application; never execute model-generated React source. Validate results with the app's runtime schema library before displaying them. Preserve a safe loading/failure state for missing or malformed results.

The original renderer used TypeScript assertions; robust runtime validation is additional production work. In the support-triage evidence, local `status: "routed"` and managed `status: "success"` were two intentional variants of one bounded queue/reason schema. Inspect actual tool output in the target; do not accept arbitrary statuses or hard-code those book-specific names in a different domain.

## Translate the stream deliberately

Use supported SDK event models and encoders. Keep provider input, translator output, BFF forwarding and browser state separately inspectable. Explicit `StreamingMode.SSE` in the managed ADK run configuration was needed for actual model partial text; an async iterator or SSE response alone did not enable it.

For the explicit lifecycle profile used here:

- Start a run before its content; use distinct stable run, message and tool-call IDs.
- Start text before its deltas and close it once. Forward incremental answer fragments or a completed aggregate, never both forms of the same text. Exclude thought-marked content and define permitted public authors.
- Stream argument fragments only for their established call. `TOOL_CALL_END` closes argument emission; it does not establish that execution succeeded. Announce a provider call once it is confirmed, not once per partial argument event.
- Correlate a result with its exact call ID and validate its public schema. Give each result a unique message ID. Concurrent calls to the same tool require IDs, not name-based guessing. Reject duplicate or ambiguous source results under the product's chosen policy.
- Preserve a run failure after earlier visible text. Emit a controlled `RUN_ERROR`; do not follow it with ordinary success. Close any visible text lifecycle according to the client contract. Once HTTP streaming has begun, a later failure must travel in-band or through an explicit interrupted-run state.

The [AG-UI event reference](https://docs.ag-ui.com/concepts/events) also defines compact events and extensions. The bundled trace checker deliberately validates the explicit start/content/end profile, not every protocol extension. Normalise supported compact events with the installed SDK or use a profile-specific test instead of labelling them intrinsically invalid.

The teaching managed bridge uses fallback IDs and name-order matching for a small sequential tool example, and groups answer text into one message. General parallel tools, replay or multi-agent authors need a stronger translator and new tests.

## Bound state and errors

Project only authorised state keys and validate values, sizes and patch paths. A permitted key can still carry an unsafe or oversized value. Treat browser state as untrusted input; server state that confers identity or permission must remain outside browser-writable state.

Bound event count **and bytes**, output totals, server queues and browser stores. Decide how slow consumers are handled without dropping required terminal tool results. Subscribe and unsubscribe within component lifecycle; cap retained telemetry and batch updates when necessary. A 50-event monitor does not bound the SDK's entire message store.

Keep public error copy fixed and sanitise server diagnostics separately. The local wrapper in the tested adapter closes its wrapped iterator and replaces provider error messages, but this does not prove privacy for all log paths. Test a provider error containing a synthetic secret and confirm that the browser never receives it.

A one-way stream does not implement durable replay, browser-tool continuation or resumable human approval. If requested, use [production.md](production.md) to design and test those explicit capabilities. Finish by tracing one successful tool display and one reported failure through the real BFF and browser, separately from offline protocol checks.
