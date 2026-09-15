# GKE sessions, HTTP and observability

Read when a GKE optimisation changes session access, serving, drain, traces or
delivery. Combine only the applicable sections with [gke.md](gke.md). The
historical private lab verified managed-session continuity through Pod replacement;
the public edge, PostgreSQL and exported tracing below are production extensions.

## Wire storage into the actual request path

Trace the server factory to the Runner and session service. Check which
environment key it reads and how missing configuration behaves. In the recorded
ADK server, `SESSION_SERVICE_URI` chooses the backend; an omitted value selects
SQLite under `/tmp`. A `DATABASE_URL` Secret alone changes nothing. A local file
is neither shared across Pods nor durable through replacement. Validate the
intended production backend before readiness; keep a deliberate local mode if
the user needs it rather than silently changing development behaviour.

Managed `agentengine://projects/.../locations/.../reasoningEngines/...` sessions
can store events while the agent executes in GKE. A session-only managed resource
does not mean hosted Agent Runtime execution. Verify backend and application
locations separately from the model endpoint. Run continuity against stored
event identities and a unique synthetic fact, through a different Pod UID and
connection to that replacement. Recall alone is weak persistence evidence.

For an explicitly chosen PostgreSQL alternative:

1. Resolve a compatible asynchronous driver and connection/authentication path;
   a declared ADK package does not supply every database driver.
2. Construct one `DatabaseSessionService` per worker after fork. Prepare expected
   tables during bounded startup and reuse that service in the actual Runner.
   Preserve `Runner(app=...)` when App settings are required.
3. Budget pool checkout, connection, queries and transactions independently.
   Calculate connections as `(active + surge + terminating Pods) × workers ×
   (pool_size + max_overflow)`, plus migration/admin/other consumers. This is a
   planning envelope, not observed connections or a universal hard upper bound.
4. Close the Runner and the owned database service within shutdown budgets.
   In ADK 2.8, Runner closure flushes sessions; database-service closure disposes
   of its engine. Preserve an original failure if cleanup also fails.
5. Rehearse backup/migration and old/new session compatibility. `prepare_tables()`
   is not a general historical migration tool. A controlled migration job owns
   schema changes; every starting Pod must not perform an unsolicited migration.

Test service selection and lifecycle with doubles first, then the chosen real
backend in approved isolation. Include old tool events, concurrent same-session
turns, process replacement and mixed application versions. Storage locking does
not supply complete-turn ordering or retry idempotency.

History optimisation uses the same rules as
[Agent Runtime](agent-runtime.md): recent-event limits count events, not turns,
and do not delete or summarise old records. Verify whether the backend limits
remote reads or slices after retrieval. Test retained facts, approvals and
unresolved work before reducing context.

## Preserve access while changing the HTTP path

A private ClusterIP plus an authenticated loopback tunnel establishes operator
access. It provides no separate end-user or tenant authentication. CORS and a
disabled developer UI do not authorise sessions. Public exposure is a separately
approved architecture change, with its own resource ownership and cleanup.

For an existing Ingress, inspect its actual policy attachments. For a proposed
Gateway, verify supported class, ClusterIP ports, HTTPS certificate/DNS ownership,
HTTPRoute and Service-targeted backend/health policies. Ingress BackendConfig
and Gateway policies are not interchangeable. Keep health endpoints shallow.
Validate selected class/features against
[GKE Gateway configuration](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/configure-gateway-resources).

Bind a trusted caller to the application's user/tenant on every run and session
operation. If using IAP, validate signed assertion signature, issuer, expiry and
expected audience; arbitrary identity headers and supplied `user_id` are not
authority. Protect alternate backend paths. Reference:
[IAP assertion validation](https://docs.cloud.google.com/iap/docs/signed-headers-howto).
Keep traffic denied during provisioning; withholding DNS does not protect a
reachable IP. Never add a public Service to debug a private readiness problem.

Make production acceptance executable and bounded: current-generation Gateway
programming, route acceptance/resolved references and required policy acceptance;
correct hostname/TLS; anonymous, invalid-audience and unauthorised caller denial;
one authorised complete run; cross-user session denial; no alternate-path bypass.
Readiness and a browser page load cannot establish this contract.

## Drain within a coherent request budget

Coordinate edge request timeout, backend drain, endpoint-removal propagation,
`preStop`, server shutdown, clients/pools and proxies. GKE's documented hold
relationship is `preStop >= backend drain + propagation allowance`, with
termination grace covering that hold plus process shutdown and margin.
The grace countdown includes `preStop`; a long grace alone does not keep a
server serving after it receives its termination signal. Consult
[GKE drain configuration](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration)
and the target server/sidecar lifecycle.

Test an in-flight authenticated request/stream during replacement, while new
requests continue. Observe client completion or explicit failure, endpoint
removal and process closure. Account for terminating Pod capacity and database
pools. The lab's successful session continuation after replacement did not test
an in-flight public-edge stream or graceful drain.

## Add timing without content export

Trace missing boundaries such as session retrieval, pool admission and delivery;
retain native ADK model/tool spans where appropriate. Use one intended provider
and export path per process. Check actual installed exporter endpoint and API/IAM
needs before making a deployment plan. ADK 2.8's Google Cloud tracing path uses
OTLP to the Telemetry API; its support requirements differ from assuming that
Cloud Trace API activation is enough. Viewer access is separate. Follow the
current [Trace troubleshooting guidance](https://docs.cloud.google.com/trace/docs/troubleshooting).

Set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and
`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=false` before constructing
instrumented objects. They do not filter every identifier or escaping exception.
Native ADK 2.8 can still attach `gen_ai.conversation.id`. A safe `error.type`
followed by re-raising can still let a span context manager export the full
exception message and stack.

When adding a custom session-load span, adapt
[session_observation.py](../assets/session_observation.py). It accepts the tracer
and existing service, disables automatic exception events/status descriptions,
uses fixed operation/store/outcome values and preserves results/exceptions. It
does not create a provider, change timeouts, authorise the caller, or sanitise
parent/native spans and logs. Copy it into the target's package, include it in
build staging, and wire it only at the session boundary actually used. Adding a
file without a caller leaves the application unchanged.

For the complete telemetry path, enforce an allowlist before external export,
at an in-process exporter or a trusted collector before its egress. Cover span
names, resource/span attributes, events, links, status descriptions and logs.
Allow fixed operation names, route templates, approved model family/revision,
bounded durations and outcomes. Remove prompts, responses, tool data, SQL,
credentials, URLs with secrets and raw user/session/business/idempotency IDs.
Sampling limits volume, not sensitivity. A dashboard display filter is too late.

Use synthetic markers in normal results, exceptions, native spans and HTTP
failures. Inspect the final export representation, including resource attributes
and status. Stop the affected rollout on prohibited export. The bundled
[observation tests](../tests/test_gke_observation.py) establish only the custom
span's behaviour with an in-memory exporter. FastAPI instrumentation, export,
parent propagation and backend receipt require their own integration tests.
Do not confuse developer-UI telemetry consent tests with Cloud Trace validation.

Flush the provider under a separate shutdown budget and inspect its result and
backend receipt. For structured logs, use approved fields and Cloud Logging's
`logging.googleapis.com/trace`, `logging.googleapis.com/spanId` and
`logging.googleapis.com/trace_sampled` formats when that integration is selected.
A generic `trace_id` field alone does not establish
[Cloud Logging correlation](https://docs.cloud.google.com/logging/docs/structured-logging).

## Completion, delivery and exact session cleanup

Use [validation.md](validation.md)'s saved-event checker for one declared bounded
tool trajectory. Set the actual answer author and tool-result assertions;
an application directory name can differ from the root agent's name. Require
successful correlated results followed by one visible `STOP` answer. Consume the
entire invocation so late failures cannot become a false pass.

Completion and partial delivery are separate. ADK API `/run_sse` needs
`"streaming": true`; a custom Runner needs
`RunConfig(streaming_mode=StreamingMode.SSE)`. Measure first event, first nonempty
visible partial text and accepted completion independently. Exclude thoughts/tool
protocol; SSE frames are not token counts. The HTTP adapter must parse multiline
SSE, bound frames/total bytes and idle/total time, surface transport errors, and
validate every event. The bundled checker neither fetches nor parses SSE.
Test the actual proxy/browser path for delivery claims; keep partials provisional
until the final accepted answer. See [state and streams](runtime-state-and-streams.md)
for bounded consumers and failure-aware cancellation.

Before any real request, bind the approved exact origin and caller. Require HTTPS
remotely, verified TLS and safe redirect handling; allow HTTP only for exact
loopback hosts. A prefix such as `localhost.example.invalid` is not loopback.
Record intended app/user/session and target before creation; use a fresh
letter-prefixed managed session ID. Reserve independent cleanup time. Delete
only that owned session and verify authorised absence; 401/403 or network failure
is not 404. Keep unresolved receipts and expose cleanup-only recovery without
repeating model work. Full infrastructure cleanup belongs to
[gke-lifecycle.md](gke-lifecycle.md).
