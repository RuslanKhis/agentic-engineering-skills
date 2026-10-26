# AG-UI and CopilotKit

Use this mode when the browser needs progressive text or incremental tool lifecycle displays. Preserve an existing AG-UI implementation if it already serves that purpose. Confirm the exact SDK/import surface in [compatibility.md](compatibility.md).

When implementing the CopilotKit route, client mounting, result renderer or streaming HTTP boundary, read the [pinned CopilotKit recipe](copilotkit-recipe.md). It supplies composable v2 API snippets for the recorded 1.69.0 packages, a bounded result parser, fresh-turn admission and wire-level checks. Adapt these pieces to the target rather than replacing its application.

## Build the vertical path

1. Define an application agent identifier and use the same value in the browser hook/provider, CopilotKit Runtime registry and adapter. It need not equal the model's name. Define the allowed backend tool names, input schemas, result schemas and state projection first.
2. For local ADK, adapt the existing agent with the pinned `ag-ui-adk` API and attach it to the existing ASGI app. In the recorded stack these are `ADKAgent` and `add_adk_fastapi_endpoint`. Authenticate the endpoint before starting a run and verify how the adapter resolves its user/session identity. The book's fixed demo `user_id` is not a multi-user design; implement request-scoped verified identity for a real app.
   ag-ui-adk's `user_id_extractor` is called with the client's `RunAgentInput` (`Callable[[RunAgentInput], str]`, 0.11.0), so anything it reads (`context`, `forwardedProps`, `state`, `threadId`) is client input; its built-in default is `thread_user_{thread_id}` and the USAGE example falls back to `anonymous_{thread_id}`. Neither is identity. Bind identity on the server instead: pass the verified-principal dependency through `add_adk_fastapi_endpoint(app, agent, path=..., dependencies=[Depends(get_principal)])` (forwarded to the run route through `**kwargs`) and resolve the user from request state, for example with `extract_state_from_request` or a per-request agent resolver, never from the run input. `dependencies=` protects only the run route: the adapter's `GET {path}/capabilities` and `POST /agents/state` routes are not covered, and `/agents/state` can read a `userId` from its body, so leave them unmounted or put them behind the same dependency at the router. `adk-fastapi-backend` builds the dependency (SB03). Read on ag-ui-adk 0.11.0 source on 2026-10-23, not exercised.
3. Keep provider credentials in the server. A Next.js backend-for-frontend forwards to Python; it must authenticate each browser caller and forward a separately verified user assertion when needed. A module-level shared backend token identifies the gateway only. Never mutate a singleton client's headers with one request's user identity.
4. Wire the BFF's agent registry, optional catch-all route and HTTP methods to the matching client provider, chat and stylesheet using the recipe. Verify the pinned imports instead of mixing examples from different API generations. The `/v2` import path is distinct from the package's 1.69.0 version number.
5. Mount the server-tool renderer inside the provider. Its argument schema does not validate the returned result. Distinguish pending execution, malformed completed output and a valid business result using runtime validation. Render components written by the application; never execute model-generated React source.

The original renderer used TypeScript assertions; robust runtime validation is additional production work. In the support-triage evidence, local `status: "routed"` and managed `status: "success"` were two intentional variants of one bounded queue/reason schema. Inspect actual tool output in the target; do not accept arbitrary statuses or hard-code those book-specific names in a different domain.

## Admit the supported request before invocation

For a new-turn-only bridge, require a fresh final user message before session creation, provider work or response streaming. Reject unsupported browser tools, writable state, resume/parent-run fields and tool-result continuation with zero agent invocations; selecting the last user message anywhere in history can accidentally repeat an earlier turn. The recipe shows one deliberately narrow profile. If the product supports any of those features, define their authorised contract instead of copying its rejections. Prior browser history is display data when the server owns conversation history.

The companion's `last_user_text` searches backwards and does not enforce this stronger admission policy. Its successful chat tests do not establish rejection of continuation or browser-provided tool/state features.

## Translate the stream deliberately

Use supported SDK event models and encoders. Keep provider input, translator output, BFF forwarding and browser state separately inspectable. Explicit `StreamingMode.SSE` in the managed ADK run configuration was needed for actual model partial text; an async iterator or SSE response alone did not enable it.

Perform auth/input rejection before starting the response; after streaming starts, consume the run's terminal event rather than treating HTTP 200 as success. Use the installed `EventEncoder` for aliases, framing and negotiated content type. The recipe includes the streaming response boundary and explains why completed-response HTTP tests cannot prove progressive delivery or prompt disconnect cleanup.

For the explicit lifecycle profile used here:

- Start a run before its content; use distinct stable run, message and tool-call IDs.
- Start text before its deltas and close it once. Forward incremental answer fragments or a completed aggregate, never both forms of the same text. Exclude thought-marked content and define permitted public authors.
- Stream argument fragments only for their established call. `TOOL_CALL_END` closes argument emission; it does not establish that execution succeeded. Announce a provider call once it is confirmed, not once per partial argument event.
- Correlate a result with its exact call ID and validate its public schema. Give each result a unique message ID. Concurrent calls to the same tool require IDs, not name-based guessing. Reject duplicate or ambiguous source results under the product's chosen policy.
- Preserve a run failure after earlier visible text. Emit a controlled `RUN_ERROR`; do not follow it with ordinary success. Close any visible text lifecycle according to the client contract. Once HTTP streaming has begun, a later failure must travel in-band or through an explicit interrupted-run state.

The [AG-UI event reference](https://docs.ag-ui.com/concepts/events) also defines compact events and extensions. The bundled trace checker deliberately validates the explicit start/content/end profile, not every protocol extension. Normalise supported compact events with the installed SDK or use a profile-specific test instead of labelling them intrinsically invalid.

The teaching managed bridge uses fallback IDs and name-order matching for a small sequential tool example, and groups answer text into one message. General parallel tools, replay or multi-agent authors need a stronger translator and new tests.

## Choose the approval contract and declare it

AG-UI 1.0 splits human approval into two client contracts that do not mix,
and `ag-ui-adk` implements both (ag-ui-protocol/ag-ui
`integrations/adk-middleware/python/CHANGELOG.md` 0.7.1 of 2026-10-01 and
0.8.0 of 2026-10-07, and `README.md`, read 2026-10-22; vendor middleware,
confirm on the installed version):

- **Plain tool-message answers** (the 0.x shape). The approval travels back
  as a `role: "tool"` message for the pending `adk_request_confirmation`
  call; CopilotKit's `useHumanInTheLoop` and the predictive-state
  `confirm_changes` dialog answer this way. This is the default: the
  middleware's `emit_interrupt_outcome` flag is `False`.
- **Interrupt outcomes with resume** (the 1.0 shape). With
  `emit_interrupt_outcome=True` on `ADKAgent` or `ADKAgent.from_app()`, a
  tool confirmation ends the run with `RUN_FINISHED.outcome.type ==
  "interrupt"` (`reason: "confirmation"`, the hint as `message`, the
  original call under `metadata.adk`; `reason: "confirm_changes"` for a
  predictive-state review), and the client must answer through
  `RunAgentInput.resume` (CopilotKit `useInterrupt`). The middleware then
  enforces the contract from session state on every instance: a run without
  a `resume` while an interrupt is open, including an answer sent as a tool
  message, is rejected with `RUN_ERROR` code `INTERRUPT_RESUME_REQUIRED`; a
  `resume` that leaves an interrupt unanswered is rejected with
  `INTERRUPT_RESUME_INCOMPLETE`; a `resume` entry naming no pending call ends
  the run with `UNKNOWN_INTERRUPT`; a rejection changes nothing. The flag is
  off by default precisely because `@ag-ui/client` 1.0 refuses the next run
  until reported interrupts are answered by `resume`, which breaks a
  tool-message frontend. assistant-ui's AG-UI adapter answers only through
  `resume` and auto-cancels pending calls on a new message, so it needs the
  flag on. A `resolved` entry whose payload is not a boolean, a `confirmed`
  object or `{"approved": bool}` (a null payload included) becomes
  `confirmed: true` in the middleware (ag-ui-protocol/ag-ui commit 85a427d on
  main, `_resume_entry_content`, read 2026-10-26; confirm on the installed
  release): custom approval UIs send `{"approved": bool}`, and a test proves
  any other payload does not approve.

A ticket declares which contract the frontend uses; a test with the flag on
sends a tool-message answer and asserts `INTERRUPT_RESUME_REQUIRED`, and a
test with the flag off asserts the tool message resumes the run. The wire
shapes those tests need, read in the middleware source and the 1.0 pattern
page (ag-ui-protocol/ag-ui main at 85a427d, `integrations/adk-middleware/python/src/ag_ui_adk/adk_agent.py`,
`docs/spec/1.0/basic/patterns/interrupt-resume.mdx`, read 2026-10-23;
confirm on the installed version): the error code is the `code` field of the
`RUN_ERROR` event (`RunErrorEvent(type=RUN_ERROR, message=..., code=...)`);
a resume entry is `{"interruptId": ..., "payload": ...}` where
`interruptId` must name an interrupt from the run being resumed and
`payload` is any JSON value, with optional `metadata`; a tool-message answer
for `adk_request_confirmation` is accepted as `{"confirmed": bool}` or
`{"approved": bool}` (`accepted` also works) or a bare word such as
`approve`, `confirm`, `yes` or `true`, and the middleware maps it to the
ADK `ToolConfirmation`; `emit_interrupt_outcome` defaults to `False` in
the `ADKAgent` constructor on that commit. `ADKAgent.from_app(app,
user_id=None, user_id_extractor=None, session_service=None, ...)` takes
the services and configuration the constructor takes; `App` and
`ResumabilityConfig` import from `google.adk.apps`. To learn which contract
a running backend emits, record one paused run and look at `RUN_FINISHED`:
an `outcome` of type `interrupt` means the interrupt contract; the bundled
`check_agui_trace.py` validates the explicit 0.x profile and does not
diagnose this, so the probe is that one recorded event or `verifyEvents`. Either way
the decision is permission, not completion, and the backend gate in
`adk-operational-guardrails` still owns the effect. For the ADK side, use
`ADKAgent.from_app(app)` with `ResumabilityConfig(is_resumable=True)`
(google-adk 1.16.0 or later): the middleware README deprecates the
fire-and-forget HITL path of the direct `ADKAgent(adk_agent=...)`
constructor and restores the paused position, including a `SequentialAgent`
sub-agent position, only through `from_app()`. Two more 1.0-line facts to
build against: every `RUN_STARTED` carries `protocolVersion` (0.8.0), and
0.11.0 (2026-10-21) discards client-supplied `app:` and `user:` state keys
at the HTTP endpoint, with `allow_scoped_state_keys=True` plus the
server-side `extract_state_from_request` hook as the only way to write
trusted scoped state (its security fix #2927); apply that stripping on any
version. The TypeScript client exports `verifyEvents`
(`sdks/typescript/packages/client/src/verify/`) to validate a recorded 1.0
stream, including `outcome` and `protocolVersion`; the bundled
`check_agui_trace.py` validates the explicit 0.x start, content and end
profile and ignores reasoning, subagent and `outcome` fields, so a 1.0
stream needs `verifyEvents` or a project test for those.

## Bound state and errors

Project only authorised state keys and validate values, sizes and patch paths. A permitted key can still carry an unsafe or oversized value. Treat browser state as untrusted input; server state that confers identity or permission must remain outside browser-writable state.

Bound event count **and bytes**, output totals, server queues and browser stores. Decide how slow consumers are handled without dropping required terminal tool results. Subscribe and unsubscribe within component lifecycle; cap retained telemetry and batch updates when necessary. A 50-event monitor does not bound the SDK's entire message store.

Keep public error copy fixed and sanitise server diagnostics separately. The local wrapper in the tested adapter closes its wrapped iterator and replaces provider error messages, but this does not prove privacy for all log paths. Test a provider error containing a synthetic secret and confirm that the browser never receives it.

A one-way stream does not implement durable replay, browser-tool continuation or resumable human approval. If requested, use [production.md](production.md) to design and test those explicit capabilities. Finish by tracing one successful tool display and one reported failure through the real BFF and browser, separately from offline protocol checks.
