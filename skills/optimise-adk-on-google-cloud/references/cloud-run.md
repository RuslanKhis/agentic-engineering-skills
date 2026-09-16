# Cloud Run inspection and optimisation

Read this reference for Cloud Run serving, capacity, authentication, deployment
verification or traffic experiments. Use [lifecycle.md](lifecycle.md) before
planning live changes, recovering interrupted operations or deleting resources.
Complete only the modes authorised by the task; local inspection does not require
a deployment.

For source/build failures, ineffective configuration, TLS/authentication errors,
developer-UI failures or delayed lifecycle visibility, read
[cloud-run-troubleshooting.md](cloud-run-troubleshooting.md). It records concrete
repairs and the boundary tests they need. For offline-to-live acceptance and
aggregate provider limits, read [part1-verification.md](part1-verification.md).

## Establish the deployed contract

Locate the real entrypoint, exported ADK `App` or agent, dependency declarations,
Dockerfile, deployment configuration and ownership receipt. Record installed
Python, ADK, storage drivers and Cloud SDK versions. Inspect the deployed revision
and image digest when cloud inspection is in scope. Compare effective settings
with source; defaults and illustrative production commands are different inputs.

Dependency ranges and tagged base images permit builds to differ. A recorded
digest identifies one image; it does not make a later build reproducible. Check
installed signatures and current official documentation before adapting an API
recipe. For native ADK deployment, inspect generated source packaging and the
installed Cloud SDK upload boundary, including source exclusions. An SDK upgrade
requires renewed boundary verification, not an assumption of unchanged staging.

Record effective CPU, memory, concurrency, timeout, billing mode, both minimum
instance levels, maximum instances, traffic, ingress and invocation policy. Derive
values from the target service rather than copying a lab size. Read-only revision
and endpoint inspection can use scoped CLI commands:

```bash
gcloud run services describe "${SERVICE_NAME:?}" \
  --project "${PROJECT_ID:?}" --region "${REGION:?}" \
  --format='value(status.latestReadyRevisionName,status.url)'
```

Inspect other necessary fields with explicit projections; keep secret-bearing
environment values out of routine output.

## Keep serving and state correct

For ADK 2.8.0, resolve the target agent directory, supported session URI, origins,
UI choice and lifespan, then construct the FastAPI application once:

```python
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agents_dir=agents_dir,
    session_service_uri=session_service_uri,
    allow_origins=allowed_origins,
    web=serve_developer_ui,
    lifespan=lifespan,
)
```

`web` is required; `app_name` is unsupported. HTTP callers use ADK routes;
in-process callers use `Runner`. The FastAPI object has no ADK `.process()` method.
Preserve the exported `App` when loading the agent so application cache settings
survive. A shallow health route checks responsiveness, not model or tool readiness.
Inspect the actual routes and client expectations before choosing a probe.

Identify the configured session adapter. In-memory storage and local SQLite lose
continuity across instance replacement or routing to another instance. A revision
tag changes routing, not durability. Before claiming durable sessions, test a
supported adapter through creation, continuation, event storage, restart and
resumption. Test authorised export retrieval separately from session storage.

A production API should disable the developer UI unless deliberately required
and use a small origin allowlist. Cloud Run invocation IAM, browser CORS and
end-user authorisation solve different problems. Bind trusted
user identity to session ownership: caller-supplied ADK `userId` is not identity.
Test missing-session handling in both JSON and streaming clients. Preserve the
HTTP error status; if a client expects SSE frames before checking status, give it
an appropriate error representation rather than a hanging or apparently successful
stream. Test successful streams and unrelated errors for regressions.

## Select identity and verification scope

Keep operator CLI credentials, local ADC, build identity and runtime identity
separate. Verify the intended project, effective impersonation, APIs and billing
through the lifecycle procedure. Retain distinct build/runtime service accounts.
Runtime Vertex AI permission does not establish BigQuery, export or user access.
Separate hosting region from model endpoint, session/data location and export
location; verify support and residency requirements for the selected backend.

Inspect the target's test profile and model-call paths. If necessary, implement a
bounded verification configuration exposing one harmless, representative tool,
with explicit output, SDK-attempt, logical-call and elapsed-time limits. Disable
unneeded caches and nested agents or separately bound and own them. Test that
limits are enforced before deployment. Choose values sufficient for the tool call
and complete answer, not merely a cheap truncated response. Count failed and
browser submissions too. Per-invocation limits are not a distributed spending
cap. A local schema map cannot establish database access; choose the tool boundary
that the proposed change actually needs to verify.

Direct IAM, direct Cloud Run IAP and load-balancer IAP require their own caller,
audience and ingress design. Select a supported token or proxy flow for the actual
credential type and verify the intended caller through the chosen route. Keep
tokens out of logs and command output. Check refresh and expiry behaviour; a
fixed-token proxy needs renewal. ADC configuration alone does not prove that the
service will accept the resulting request.

## Validate at the correct boundary

Run existing offline tests in the declared environment. Where coverage is missing,
exercise real ADK routes, tools and session storage with model/cloud calls replaced
at their external boundaries. Starting a local server does not stub its model.
Record skipped compatibility tests as skipped.

Construct the bounded live verifier from the target's actual route definitions,
application name, request schema, events and session API. Use a synthetic fixture
with known expected tool output. Give HTTP operations deadlines and the whole run
a deadline; bound response bytes and event count. Parse SSE framing correctly
when applicable. Restrict credential forwarding to the intended origin, including
redirect handling. Reserve a separate cleanup budget.

Verify unauthenticated rejection and successful intended-caller access separately
from output checks. Read through termination, preserving late errors. Capture one
invocation's complete event array, then use
[validation.md](validation.md) and the bundled
[saved-event checker](../scripts/check_run.py) with an explicit acceptance contract.
The checker validates saved-event consistency only: it makes no requests and
proves neither network behaviour, authentication nor evidence authenticity. Use a
target-specific validator for legitimate unsupported trajectories; retain the
original evidence rather than removing events to satisfy the checker.
Reject errors and truncation, correlate tool results and require an authoritative
complete answer. Partial text is provisional.

Verify synthetic session deletion with a subsequent authorised 404. Test browser
behaviour separately when relevant and stop temporary proxies afterwards. Retain
primary and cleanup errors without repeating the model invocation just to retry
cleanup.

## Tune capacity from observations

Reuse suitable clients per worker, close them during shutdown and keep request
data invocation-scoped. Inspect whether lifespan actually manages those clients.
Assess client concurrency safety before sharing it. Worker and instance memory
are separate; globals do not provide coordination or persistence.

Inspect blocking tool paths before raising request concurrency. A coroutine
containing synchronous database calls still blocks its event loop. Prefer
asynchronous I/O; bound offloaded blocking I/O and its admission queue.
`to_thread()` does not cancel accepted
remote work. Consider bounded process pools for measured pure-Python CPU work,
including serialisation, process memory and shutdown costs.

Test selected concurrency points against throughput, tail latency, errors, CPU,
memory, instances and downstream quotas. Set maximum instances from downstream
capacity and budget. Keep dependency deadlines shorter than the outer request
timeout and reconcile remote operations after cancellation.

Separate warm capacity, startup CPU boost and instance-based billing. Minimum
instances reduce some cold starts; they remain replaceable. Startup boost adds
billed startup CPU. `--no-cpu-throttling` supplies CPU outside requests and changes
billing; it does not make background work durable. An open SSE request is active
request handling. Inspect service-level `--min` versus revision-level
`--min-instances`: tagged revisions with minimum capacity can continue billing.
Check the current [Cloud Run billing settings](https://docs.cloud.google.com/run/docs/configuring/billing-settings)
before preparing the cost and configuration comparison.

## Gate and recover traffic changes

For an authorised production canary, lock deployment, record the stable revision
and declare acceptance thresholds. Deploy the digest with no traffic and a
temporary tag; capture the candidate revision. Test authenticated health,
complete relevant tool responses and sessions directly against that candidate.
Promote explicit revisions through agreed stages, collecting comparable samples.
Traffic splitting is not paired replay: cohorts, affinity and session histories
can differ. Compare equivalent staging workloads before attributing an effect
to one flag. A UI's session-creation request may warm the instance before its
model-bearing request; use platform startup/instance evidence to classify
coldness. Time idle alone does not establish a cold invocation.
Assemble rollback from the recorded stable revision:

```bash
gcloud run services update-traffic "${SERVICE_NAME:?}" \
  --project "${PROJECT_ID:?}" --region "${REGION:?}" \
  --to-revisions="${STABLE_REVISION:?}=100"
gcloud run services update-traffic "${SERVICE_NAME:?}" \
  --project "${PROJECT_ID:?}" --region "${REGION:?}" \
  --remove-tags="${CANDIDATE_TAG:?}"
```

Verify routing convergence and remove experiment-specific revision minimums.
Restore `--to-latest` only when the intended candidate is still latest. Finish
with the lifecycle cleanup and retention report. Report functional, performance,
durability and cleanup outcomes separately.

## Historical evidence boundary

The originating lab verified ADK 2.8.0 Docker and native hosting with a bounded
schema-only profile; the native pass used Cloud SDK 572.0.0. Its local SQLite and
in-memory sessions did not demonstrate durable hosting. A same-image 50/50 CPU
experiment passed functional checks without establishing a speedup. Separate local
full-tool/provider evidence did not extend hosted coverage. These observations
motivate the rules above; the lab's profiles and deployment helpers are not
required or supplied by this skill, and their PASS results do not verify a target.
