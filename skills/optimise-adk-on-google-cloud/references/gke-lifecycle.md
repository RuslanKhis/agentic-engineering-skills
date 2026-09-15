# Own the GKE lifecycle

Use this reference when an ADK optimisation changes a GKE image, workload,
identity, capacity or cloud resources, or requires recovery and cleanup. Apply
[lifecycle.md](lifecycle.md) for the exact approval and budget contract. Adapt the
target's deployment system; this skill supplies no automatic cloud deployer.

## Establish the actual deployment boundary

Trace the command that builds and applies the workload. Determine whether the
authoritative inputs are generated objects, Helm/Kustomize output, another
release pipeline or checked-in YAML. Inspect the rendered output as well as the
source. Do not apply every manifest in a directory because its examples parse.

The originating private lab generated its own objects: two fixed Pods, a two-Pod
namespace quota, `maxSurge: 0`, `maxUnavailable: 1` and a `ClusterIP` Service.
Its reference directory contained different rollout settings and a
`LoadBalancer` example. Editing those reference files did not change the lab.
An HPA or surge policy cannot exceed quota merely because it was accepted as an
object. A new public Service is an exposure and cost change requiring its own
plan, ownership and acceptance tests.

Before contacting a cluster, record the intended project ID and number, cluster
location and identity, namespace, workload and Kubernetes service account. Verify
the kubeconfig context's actual target rather than trusting its display name.
Use explicit context, namespace and request timeouts for commands. A temporary
kubeconfig can avoid changing the operator's default context; track its associated
authentication-plugin cache and remove only those owned temporary files later.

Keep operator CLI identity, ADC/quota project, build service account, node service
account and Pod principal separate. The model endpoint and session-storage region
are independent of the cluster location. Check project access, billing, selected
APIs, required CLI/authentication-plugin versions, quota and network ranges through
their actual boundaries. An enabled API does not establish available capacity.
Missing credentials or prerequisites permit offline work to continue. Do not
create keys, link billing, enable APIs or raise quotas to bypass the missing gate.
Inspect combined commands carefully: an `--enable-apis` mode may also deploy.

## Prepare the release and permissions

Build from a reviewed source allowlist. Include new server modules, drivers and
dependency declarations deliberately; exclude credentials, receipts, local data
and unintended test doubles. Preserve the target's pins and package manager.
Record source hashes, resolved dependencies, builder identity and accepted build
ID. A successful build must return the exact published image and full digest;
deploy that immutable reference, not a mutable tag or a string merely containing
`@sha256:`.

Diagnose permissions at the failing boundary:

| Identity | Boundary to verify |
| --- | --- |
| Build account | Staged-source reads, image publication and build logging |
| Node account | Node operations and image pulls from the selected repository |
| Exact namespace/service-account principal | The model, session and tool APIs actually invoked by the Pod |

Workload Identity Federation for GKE addresses Pod access to Google services. It
does not supply node image-pull permission or authenticate an end user. The
historical lab used a direct Kubernetes service-account principal with
`roles/aiplatform.user`; treat that as the lab's role set, not a universal
least-privilege policy for production tools. Derive the target principal from the
verified project number, workload identity pool, namespace and service account.

Capture the existing IAM bindings before a change. Record each exact scope,
member, role and condition, whether it pre-existed, and whether this workflow
added it. Preserve concurrent and pre-existing policy changes. Do not grant broad
build rights to a default account or inject the operator's credentials into the
image to make a smoke test pass.

Before an approved apply, render all placeholders, validate the selected objects
locally, and prepare a separately scoped server-side dry-run against the target.
The latter contacts admission and checks permissions; it is not proof that Pods
can start or the application works. Compare selectors, referenced identities and
Secrets, ports, quota, rollout and scaling bounds. Check immutable-field changes
and retain the previous image/configuration with a compatible rollback plan.

## Record ownership and reconcile uncertain work

Use private durable, atomically written and appropriately locked receipts. Bind
creation intent to target configuration, source hashes, a unique ownership marker
and the existing-resource baseline before dispatch. Save stable provider
identities as they become available; a name or matching label alone is insufficient
after a resource has been replaced. A collision without a matching receipt is not
permission to adopt or delete a resource.

For builds, cluster operations and managed-session resources, distinguish
submission intent, accepted operation, pending, terminal success and terminal
failure. Save accepted identities before polling. Bound transport, polling and the
whole campaign, reserving time for cleanup. On a lost response, reconcile the same
target and submission evidence instead of starting another build or cluster.

Do not assume the CLI returns an operation object. In the tested CLI path,
asynchronous cluster creation returned a cluster and deletion returned no operation
object. Recovery used the pre-submission operation inventory and one uniquely new
operation with matching project, location, exact cluster target and operation type.
Reject old, unrelated or ambiguous matches. Resume polling a known accepted
operation; a client timeout, empty response or missing resource is not permission
to replay its mutation. Record failed creation as failure even when partial owned
infrastructure remains available for cleanup.

A completed repeat should verify resource identities, ownership, image, admitted
workload spec and required grants without another build or apply. Drift requires
review; do not silently recreate missing resources or re-add permissions. A
deliberate update has its own authorised plan and rollback path. Retain completed
deletion receipts; use fresh ownership for a separately authorised future lab.

## Verify the result and explain capacity failures

After an approved apply, inspect rollout conditions, observed generation, Pod
UIDs, Ready endpoints, actual image IDs and admitted resources. Autopilot admission
can change submitted requests. Confirm the running namespace/service account and
session URI, then test the complete model/tool result through the intended access
path. For persistence, retain event IDs and a synthetic marker, replace a serving
Pod under the approved plan, verify a different Pod UID and continue the same
session through that replacement. Plausible recalled text alone is weak evidence.

An authenticated localhost-only Kubernetes tunnel is an operator access boundary.
It does not establish end-user authentication or cross-tenant session isolation;
URL user IDs and CORS are not those controls. Record synthetic session intent and
returned identity, validate the full invocation and clean up the exact session
independently of whether the answer passed. A cleanup retry must not repeat the
paid turn. Public HTTPS and streaming paths need their own acceptance gates.

When provisioning stalls, preserve cluster operation errors and Pod scheduling
events. Distinguish regional capacity, quota, placement constraints, image-pull
permissions and application readiness. Report the stage reached and resources
still owned; do not call a Pending Pod an application performance result. A later
successful attempt does not prove a code repair resolved provider capacity. Do
not change region, machine policy or quota, or start another campaign, without a
newly covered scope and reconciliation of the previous attempt.

## Close the whole owned environment

After separate cleanup confirmation, stop owned tunnels and close test sessions.
Settle or cancel accepted owned builds and reconcile cluster create/delete
operations before deleting dependencies. Verify the exact cluster's terminal
deletion and absence. Managed session storage has an independent receipt and
lifecycle; deleting a Deployment or cluster alone does not remove it.

Remove only added IAM grants, then the owned image repository, staged-source
bucket/objects, build and node accounts, subnet and network in dependency order.
Recheck ownership immediately before deletion. If a network has remaining
dependencies, identify their owner before acting. For a production optimisation,
restore the approved prior configuration and remove experiment artefacts rather
than deleting the shared cluster or service.

Independently compare relevant inventories with the baseline: clusters, VMs,
disks, instance groups, addresses, forwarding/load-balancing resources, firewall
rules, routes, networks, repositories, buckets, identities, IAM and session
resources. Cover the correct projects, regions and all result pages. Permission
denied, unavailable APIs and incomplete listings mean unknown state. If a deleted
service-account GET denies access, only a successful complete project inventory
that excludes both its email and recorded unique identity can support absence;
the denial alone cannot. Reconcile stale aggregate inventory with the owning API.

New Gateways, databases, certificates, Secrets, snapshots or capacity buffers need
their own receipts and teardown design before creation. Inspect provider resources
behind Kubernetes controllers, not only the controller objects. Preserve shared
APIs, pre-existing identities and unrelated infrastructure.

Report retained source-object soft deletion, build/log/audit history, past usage
and any unverified inventory scope. Active-resource absence does not prove physical
erasure or zero future charges. Keep the completed receipts so repeating cleanup
verifies absence instead of reconstructing ownership from names.

## Historical evidence boundary

The final 14 September 2026 existing-project retry passed private routing, real
managed-session continuity through Pod replacement, repeated setup, repeated
cleanup and independent absence checks. It used two Ready Pods on one node, so
it established neither node/zone failure tolerance nor production availability.
Earlier capacity failures remain part of that evidence; the final same-region
attempt succeeded without a quota or region change. The unchanged deployed source
had passed 89 offline tests, including ownership and uncertain-operation cases.

First-time API activation and fresh-project onboarding were not run. Public edge
access, HPA/VPA, production load, database alternatives, full trace export,
streaming delivery and production rollback were outside the live result. Later
inventory checks found no active campaign infrastructure in their recorded scope,
while soft-deleted storage and provider history could remain. These historical
results guide a new target's tests; they do not certify its deployment.
