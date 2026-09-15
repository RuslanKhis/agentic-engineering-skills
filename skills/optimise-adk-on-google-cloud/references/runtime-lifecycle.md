# Own the Agent Runtime lifecycle

Use this reference when a managed-runtime optimisation requires source packaging,
deployment, configuration changes, recovery or cleanup. Apply the approval and
budget rules in [lifecycle.md](lifecycle.md); this reference supplies the
runtime-specific checks. Adapt the target project's supported interfaces rather
than introducing a second deployment system.

## Establish the target and source boundary

Distinguish remote agent execution from a local ADK runner using managed session
storage. Record the exact runtime resource, project ID and number, runtime region,
model/backend and endpoint, agent/App entrypoint, source hashes and dependency
resolution. Agent Runtime prose can coexist with SDK/API identifiers
`agent_engines` and `reasoningEngines`; do not rename working identifiers.

Inspect the installed deployment interface and generated source before proposing
changes. The originating source path used `google-adk[a2a]==2.8.0`,
`google-cloud-aiplatform[agent_engines]==1.153.1` and `google-genai==2.19.0`.
Preserve a target's pins and extras unless a justified change is approved. These
three pins do not fix every transitive dependency. Record the resolved environment
and check compatibility rather than silently installing newer packages.

For that SDK interface, capacity configuration fields included `min_instances`,
`max_instances`, `resource_limits` with `cpu` and `memory`, and
`container_concurrency`. Derive their values from the target and check effective
provider state. A local environment variable is not a deployment control unless
the actual adapter reads and applies it. A configuration update is consequential
even when the resource ID stays the same.

Use an explicit source allowlist and inspect the actual generated archive.
Include required application modules and dependency declarations; exclude
credentials, environment files, receipts, logs, datasets and unintended mocks.
Verify that the intended `App` and its configuration reach the deployed wrapper.
The tested source path uploaded an inline archive without a customer staging
bucket. Other deployment paths or versions can differ; neither provision nor
delete a bucket merely because a generic recipe mentions one.

Keep CLI operator, ADC identity/quota project, build identity and runtime identity
separate. Inspect impersonation, enabled APIs, billing and model/data permissions
through their actual boundaries. Runtime invocation access does not prove
BigQuery or tenant access. Missing credentials permit offline packaging and tests
to continue; they do not justify creating keys or changing shared IAM.

## Separate setup verification from updates

Before submission, prepare a private durable receipt binding the target, source
fingerprints, deployment profile, intended configuration and unique ownership
marker. Inspect all relevant inventory pages. A display-name match is a collision
requiring reconciliation, not ownership evidence or permission to adopt a service.

Record creation intent before dispatch and persist the exact returned resource
and accepted operation before polling. Attach ownership at the earliest supported
creation boundary. If the selected SDK conceals an accepted operation or performs
automatic compensating deletion, inspect that behaviour and design recovery before
using it. The historical adapter intercepted private SDK internals; that is not a
portable deployment recipe or a compatibility guarantee. Prefer supported APIs
with explicit operation handles.

On repeat setup, compare the receipt with provider identity, ownership, source and
effective configuration. Completed matching setup should verify without another
build or update. An unexpectedly absent runtime is not permission to create a
replacement. Source/configuration drift or a replaced ownership marker requires
review; do not overwrite either the service or its recovery evidence.

A deliberate update needs its own authorised plan, recorded previous
configuration/source, acceptance criteria and supported rollback route. Do not
generalise a disposable lab's refusal of all source changes into a prohibition on
controlled production updates. Conversely, do not treat “setup again” as implicit
approval for a changed deployment.

## Reconcile accepted and uncertain operations

Track submission intent, accepted identity, pending, terminal success and terminal
failure separately for create, update and delete. Bound each transport request,
polling loop and whole workflow. Preserve receipts across process exits and use
coordination appropriate to the target; an atomic file write alone does not lock
multiple deployers.

If a response is lost before its operation ID is recorded, the outcome is unknown.
Retain the original target and reconcile provider operations and audit evidence.
One empty inventory or a client timeout does not authorise another submission.
Resume polling an accepted operation rather than replaying the mutation. Settle
prior create/update operations before considering deletion; pending work can still
change the resource.

In the verified API path, create/update operations appeared beneath
`projects/.../locations/.../reasoningEngines/ID/operations/OPERATION`, while the
actual delete operation appeared at
`projects/.../locations/.../operations/OPERATION`. A regional delete operation is
usable only when evidence binds it to the exact owned runtime and matching
project/region. Do not loosen validation to accept any regional operation for
create/update, another project or another runtime.

If parsing fails after DELETE was accepted, recover the exact operation from
provider evidence, verify its target and terminal result, and preserve the
original receipt alongside the recovery record. Do not submit another DELETE
solely to obtain a cleaner test result.

## Close sessions and resources independently

Record synthetic session intent with trusted owner and runtime identity before
creation, then persist the returned session ID. A missing acknowledgement leaves
a pending session to reconcile. A cleanup-only retry must not repeat the model
turn. Preserve primary and cleanup failures separately.

For the supported API, use `async_delete_session` for the recorded session and
verify absence through an authorised exact read or a complete, validated
`async_list_sessions` result. Authentication failures, malformed responses and
incomplete listings mean unknown state. Reuse one session for continuity tests,
then verify its stored events and remove it explicitly.

After separately confirmed resource cleanup, verify terminal deletion, exact
runtime absence and relevant child-session absence. Retain the completed receipt
so repetition verifies rather than recreates. Preserve shared APIs, identities,
IAM and pre-existing resources. Report provider-managed build/log/storage
retention separately; active-resource absence does not establish physical erasure
or zero later charges.

## Historical evidence boundary

The originating live campaign verified a routing-only profile, remote session
continuity, negative authentication/session reads and repeat setup. Its capacity
was min 0/max 1, CPU 1, memory 4 GiB and concurrency 1: bounded test values, not
production defaults. Cleanup passed after the regional-operation parser failure
and evidence-based recovery; it was not an uninterrupted first-run lifecycle pass.
Cross-principal isolation, full metrics/compaction, local execution with managed
sessions, live failure injection, fresh-project activation and performance/load
guarantees were not established. A target project needs its own scoped validation.
