# Prepare external work and own its lifecycle

Use this reference before a deployment/configuration mutation, model/cache
experiment, cloud query/export or cleanup. Inspection is read-only by default.
Prepare the implementation and exact reviewable plan before requesting approval.

## Make the target and proposed work concrete

Record account, project, billing/quota project, hosting region, model/backend and
model location. Treat session storage, query/data location and export bucket
location separately. Read CLI identity, ADC and deployed workload identity as
different boundaries. A changed root environment file does not replace a nested
key or change which account ADC uses.

Use explicitly scoped project, billing and enabled-API reads. Read-only access
does not imply permission to enable a service. Permission denied or a transport
failure means unknown state, not resource absence. A trial still needs the billing
configuration required by the selected service; verify actual access rather than
inferring it from an account label. Do not silently link billing or raise quotas.

The approval plan contains:

- Exact commands and target identity, project, region and resource names.
- Existing resources to preserve, new resources with unique ownership labels,
  IAM binding/resource scope and any secret versions to create.
- Immutable image/source inputs, security/exposure settings and intended traffic
  change or isolated endpoint. Enabling APIs, provisioning and paid tests are
  separate actions even if a tool combines them.
- Logical model calls, SDK attempts, nested work, query bytes, request counts,
  elapsed-time and resource limits; budget and execution window agreed by the user.
- What happens on refusal, failure or an uncertain response, and the exact
  separate cleanup/absence checks, including cache and retention scope.

Ask for explicit approval before the listed consequential work. Prior approval
applies only while it covers the same scope. Keep authorised offline work moving
when external approval or prerequisites are missing. Never print a token or
credential to prove login. Use synthetic inputs for live tests.

## Record intent before submission

Use a private durable receipt with the planned resource/job/session identity,
creation status and provider-returned stable identity. Record accepted operation
IDs before waiting. A name collision without ownership evidence is a blocker,
not permission to adopt or delete it. On a retry, reconcile known operations and
verify completed configuration before doing new work.

Write reservations before dispatch. Make concurrent receipt updates atomic and
locked using an appropriate single- or multi-process strategy. A shared fixed
temporary filename can lose updates under callbacks. Unique atomic temporary
files solve only part of that problem; multi-process/distributed ownership needs
its own coordination. A portable application should use supported boundaries,
not private SDK monkey-patches copied from a one-off audit harness.

Bound provider polling and dependency operations independently of the outer
request timeout. A lost acknowledgement or client cancellation cannot establish
that remote work did not happen. Keep the same planned identity for recovery;
report an unresolved outcome instead of creating a second campaign to get a PASS.
Reserve time and request capacity for cleanup.

## Clean up only what this workflow owns

Obtain confirmation for the separate deletion plan. Match receipts to provider
identities and ownership markers; remove only resources and IAM grants created
by this workflow. Preserve pre-existing policies, shared services, data and
unrelated user work. For an existing production service, restore the approved
settings/traffic and remove owned experiment artefacts rather than deleting it.

Cloud Run experiments can leave tagged revisions, warm minima, images/build
storage, runtime/build identities and IAM changes after traffic is restored.
Queries/exports can leave jobs, destination tables and objects. Reconcile accepted
work before tearing down dependencies. Check provider absence or restored
configuration independently and repeat cleanup safely using the same receipt.

Caches have their own resource identity and expiry. Session deletion, service
deletion and failed model generation do not delete an already-created provider
cache. Record cache intent/result at its boundary, delete only owned caches and
verify their absence or explicitly retained expiry.

For synthetic sessions, record the target and chosen identity before creation.
Use a separate cleanup budget in `finally`, DELETE the exact owned session and
then verify 404 through the same authorised API. A 401/403 or network failure is
not absence. Preserve the primary error as well as cleanup failure; a cleanup-only
retry must not rerun the paid invocation. Use letter-prefixed session IDs when
required by the selected backend.

Retain the completed receipt. Logical deletion does not imply immediate physical
erasure: build/log history, storage recovery retention and past usage can remain.
Report visibility and retention limits; do not claim zero future charges from an
active-resource inventory alone.
