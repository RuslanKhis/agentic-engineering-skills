# Verify GKE changes at the boundary they affect

Read when implementing a GKE optimisation, extending the verified private pattern
or deciding which tests support a production claim. Use
[application integration](gke-application-integration.md) for server and session
wiring, [deployment troubleshooting](gke-deployment-troubleshooting.md) for provider
failures, and [GKE lifecycle](gke-lifecycle.md) before external operations.

## Keep the implementation real and replace the external effect

A fake command that returns the desired object cannot establish the real CLI's
response shape. A dictionary called `app` cannot establish ADK App propagation.
Choose a seam where the actual implementation runs and substitute only the
provider transport, model generation or clock needed to keep the test offline.
Preserve the target's dependencies and inspect imports before running them.

| Claim | Local test boundary | Separate evidence still needed |
| --- | --- | --- |
| Changed code ships | Real staging function, archive members, Docker copy inputs and isolated staged import | Actual build, complete dependency inventory and matching running image digest |
| Rollout fits its envelope | Actual renderer; quota, resources, replica ownership, selectors and strategy together | Target admission, scheduling, terminating overlap and Ready endpoints |
| Settings affect serving | Fresh startup and actual ADK factory/Runner | Effective admitted configuration and deployed workload identity |
| Session history is bounded | Actual service implementation, storage query and returned events | Selected remote backend's real query work and retained-fact quality |
| Shutdown closes storage | Actual Runner/session lifecycle and disposal observer | Driver/backend shutdown, proxy drain and process termination |
| Streams complete | Actual HTTP handler plus deterministic model events and full response consumption | Proxy/browser delivery and authenticated edge behaviour |
| Telemetry excludes sensitive data | Final in-memory exported representation from the actual instrumented path | Intended exporter/collector configuration and backend receipt |
| Repeated setup/cleanup is safe | Real manager with realistic response doubles; mutation counters and durable state | Authorised provider operations and independent inventory |

Guard authentication discovery, socket/DNS and provider transports before importing
application code. A model-name string can still invoke a real provider through a
real Runner. Use a temporary agents directory, database, home and private receipt
location where needed; do not modify global credentials or Kubernetes context.
An in-process HTTP client establishes application semantics, not network delivery.

## Render the actual release and assert relationships

Test the generator or selected release input, including its staging function.
Place a synthetic required module outside the old allowlist and prove that the
staged import sees the reviewed implementation after repair. Check Docker copy
inputs separately: being present in a build context does not guarantee inclusion
in the final image. Inject a synthetic credential/receipt marker outside intended
inputs and assert it is excluded. Never use real secrets for that test.

For workload changes, check exact selectors and references, Service target ports,
immutable image digest, service account, consumed session key and intended
exposure. Evaluate HPA maximum, worker count, per-Pod requests, rollout overlap
and quota together. Preserve a user's capacity ceiling; show the availability
trade-off if it prevents surge. Account for admitted sidecars and terminating Pods
when estimating resources and pool connections. Kubernetes documents that
terminating Pods can temporarily exceed replicas plus surge in
[Deployment behaviour](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

Separate local parsing, target server-side dry-run and live scheduling. A manifest
can be accepted without its requested replica count being achievable. Test a
completed repeat with changed source, changed workload spec, replaced immutable
identity and a missing grant: verification should report drift, not silently
create, apply, build or grant again. Updating that release is a separate operation.

## Exercise the real HTTP and session path

Keep the SDK loader, session routes, Runner and event serialisation in the test.
Supply a deterministic model through the target's supported loader/model boundary.
Check both a successful tool result and complete answer, malformed requests,
stored state/events and exact-session removal. A GET under a different user key
tests routing-key behaviour only; there is no authenticated principal in that
assertion. A production authorisation test needs the actual authentication gate.

For ADK 2.8, test explicit-ID and generated-ID session creation separately. Their
request-body shapes differ. Distinguish the application directory name used by
the HTTP API from the agent author used in completion assertions. Set configuration
before constructing/importing the application and verify the actual factory
receives the intended full managed URI. Session location is independent of the
model endpoint.

For history, create distinguishable stored events, fetch a limited view and then
fetch the original history again. Observe the backend call or SQL, not just the
length returned to Python. A managed adapter may fetch all events before slicing;
a database implementation can apply a SQL limit. Neither operation summarises
or deletes the original conversation. `num_recent_events=0`, positive limits,
tool-pair boundaries and old approvals deserve explicit target acceptance rather
than an assumption that a fixed number of events is a safe number of turns.

For service lifecycle, observe preparation, use, Runner flush and engine disposal
independently. Force startup failure before yield, request failure, cancellation
and a secondary cleanup failure. Check that owned resources still receive cleanup,
that failure does not become readiness, and that the original failure remains
visible. A fixed cleanup code is sufficient; avoid logging the database URL or
raw exception. SQLite tests establish SDK orchestration, not PostgreSQL pooling,
driver deadlines, migrations or production connection capacity.

## Consume errors after HTTP success

Exercise `/run_sse` with streaming omitted, false and true. Capture the model's
actual stream flag, partial events and final event. HTTP 200 means headers were
accepted; a later generator error may arrive inside the event stream. Consume
that tail and fail the run. An ASGI test client may buffer output, so its passing
test does not establish first-token timing, client disconnect propagation or
browser rendering.

Use [check_run.py](../scripts/check_run.py) for a saved invocation with declared
named function tools and a text answer. It requires correlated calls/results and
a designated author's STOP completion. Unsupported non-null Part payloads,
including code-execution, server-side tools and media, fail explicitly rather
than letting accompanying narration satisfy the answer assertion. Nested tool
media, partial arguments, continuation and scheduling fields also require a
different contract. Null SDK defaults remain supported; ordinary business keys
inside the declared JSON args/response are not protocol fields. A target that
supports additional protocols needs its own acceptance rules.

For asynchronous decoded consumption, adapt the existing
[finite answer component](../assets/finite_answer_stream.py) under its
[integration contract](runtime-verification.md#test-streaming-without-confusing-it-with-a-tool-verifier).
It keeps previews provisional and handles bounded completion/closure; it does not
validate the business meaning of a routing response. Do not strip tool events to
make either checker pass. Parse and bound the actual transport separately, then
test proxy/browser behaviour if incremental delivery is part of the requirement.

The companion's simpler routing validator accepted a synthetic mismatched call
ID plus partial-only model text in this review. Its historical successful live
answers remain useful evidence, but that validator alone cannot prove the stronger
contract. The original companion was left unchanged; use the stronger acceptance
boundary when extending the workflow.

## Inspect native telemetry and the final export

The custom session-observation component has local privacy tests. Extend that
evidence to real native ADK/HTTP/database instrumentation when using it. Set capture
flags before construction, supply synthetic markers in content and identifiers,
and collect spans with an in-memory exporter. Inspect names, resource and span
attributes, events, links and status descriptions, including parent spans.

Native ADK 2.8 can retain `gen_ai.conversation.id` with message capture disabled.
Treat a test that reproduces this as a negative control demonstrating the need
for an export policy, not a privacy pass. A clean custom span does not clean its
parent. Developer-UI telemetry-consent persistence with telemetry disabled does
not test Cloud Trace ingestion. For actual export, inspect the installed provider,
receiver, credential source, shutdown result and backend read surface separately;
follow [GKE serving](gke-serving.md#add-timing-without-content-export).

## Keep failure and cleanup evidence attributable

Fault-inject before submission, after acceptance but before receipt persistence,
during polling and during cleanup. Use realistic CLI/API shapes from the target
version, and reject old, ambiguous or wrong-target operation candidates. A
confirmed rejection differs from a timeout with an unknown outcome. Preserve
the accepted identity and prohibit a second mutation while it remains unresolved.

Exercise cleanup independently of model work. Persist exact session intent before
creation, retain uncertain receipts, and provide cleanup-only recovery. For
infrastructure, cover dependencies and only the grants the workflow added. Test
successful absence separately from permission denial and incomplete inventories.
The provider's resource API can be more current than an aggregate asset inventory.

For a live continuity claim, retain original events and a distinctive synthetic
fact, replace the serving Pod under the approved plan, verify its replacement UID
and reconnect specifically to that replacement. Inspect stored events before the
follow-up. Two Ready Pods on one node prove neither node nor zone resilience.
Close the exact test sessions and tunnel afterwards; record provider retention
and incomplete inventory scopes alongside active-resource absence.
