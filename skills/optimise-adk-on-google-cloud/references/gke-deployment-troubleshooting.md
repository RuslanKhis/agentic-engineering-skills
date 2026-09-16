# Diagnose GKE deployment and recovery boundaries

Read when preflight disagrees with a provider response, a build succeeds but Pods
fail, an interrupted mutation has an uncertain outcome, repeated setup refuses
drift, or a capacity attempt needs closure. Use [gke-lifecycle.md](gke-lifecycle.md)
for ownership, approval and teardown scope, and [gke.md](gke.md) for workload
capacity and startup analysis. This reference supplies no deployer.

## Classify the failed boundary before changing configuration

| Symptom | Evidence that decides the next step |
| --- | --- |
| Billing inspection names an unexpected consumer project | Check the CLI/ADC quota project independently of the resource project. Explicit billing-project selection repaired the historical inspection; enabling an API in the unexpected project would have addressed the wrong boundary. |
| Resource inspection says “not found” inside an error | Preserve status and error category. A genuine not-found response can establish absence; permission, authentication and unavailable responses cannot, even when their text mentions absence. |
| Bucket creation fails before any source upload | Inspect the actual method, API version, collection path and response. A permissive transport double can accept a malformed URL. |
| Build succeeds but image pull fails | Inspect the node identity, exact repository, image digest and pull/network events. Build publication permission is distinct from node read permission. |
| Pod is Ready but the first agent request fails | Inspect the exact namespace/KSA principal, model/session endpoints and application error. A shallow HTTP probe does not establish those permissions. |
| A repeated deployment refuses changed source or workload | Establish whether this command verifies a completed exercise or implements release updates. Refusal can be its intended contract. |
| Cluster creation or node scale-up stalls | Inspect the accepted cluster operation separately from scheduler/autoscaler events. Capacity, quota, placement and application startup are different findings. |

The tested Storage JSON API v1 failure was a POST to `/storage/v1/buckets` instead
of the [documented `/storage/v1/b` collection](https://docs.cloud.google.com/storage/docs/json_api/v1/buckets/insert). The repair was verified by a test
asserting the complete endpoint, method, ownership label and enforced public
access prevention. The historical installed bucket CLI lacked the desired
creation-time labels flag, which motivated that specific REST implementation.
Treat this as a wire-contract lesson, not a reason to replace a target's supported
SDK or CLI. Check the selected version's actual contract before adapting it.

Keep environment interpretation explicit. Shell wrappers may read configuration
relative to the caller's working directory while resolving their Python helper
relative to the script. Compare the loaded configuration with the receipt before
mutation; a familiar script path does not prove which project settings it uses.
An API-enablement option may continue directly into deployment. Establish its
whole behaviour before describing it as an activation-only step.

## Diagnose each permission with its actual owner

The retained private campaign used the following six grants. This is a useful
diagnostic map, not a universal production role policy or an instruction to add
them to an existing project:

| Scope | Principal | Recorded role |
| --- | --- | --- |
| Project | Dedicated build account | `roles/logging.logWriter` |
| Source bucket | Dedicated build account | `roles/storage.objectViewer` |
| Image repository | Dedicated build account | `roles/artifactregistry.writer` |
| Image repository | Dedicated node account | `roles/artifactregistry.reader` |
| Project | Dedicated node account | `roles/container.defaultNodeServiceAccount` |
| Project | Exact namespace/KSA federated principal | `roles/aiplatform.user` |

Build and node accounts were distinct. Existing managed service agents retained
their prior standard grants. A successful campaign in that project therefore did
not verify service-agent bootstrap or first-time API activation. Check that
baseline on a new target instead of granting broad roles to the default Compute
account when a prerequisite is missing.

For direct federation, the workload principal includes the verified project
number, the project's workload identity pool and the exact namespace and KSA.
A different namespace is a different principal even when the KSA name matches.
For impersonation, inspect the additional relationship deliberately; the
historical direct-principal grant does not establish that relationship.
See the [official identity configurations](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity).

For every policy change, preserve scope, member, role and condition together.
The historical manager checked unconditional bindings and used
`--condition=None`; a conditional grant is not automatically equivalent. Record
whether the matching binding pre-existed and whether addition was attempted.
Cleanup removes the added binding, retaining unrelated members and pre-existing
grants. Compare effective bindings, not IAM etags: an etag can change after
legitimate additions and removals even when the final bindings match the baseline.

## Preserve the exact release boundary

A local module must pass both the source-staging allowlist and Docker copy rules
before it exists in the deployed image. Dependency installation must also include
its driver or instrumentation package. A helper that works in a borrowed test
environment may be absent from the declared GKE environment; the historical
preparation discarded such an environment and verified the declared dependencies.

Retain staged-source hashes, source-object identity/generation when available,
accepted build ID, build account and the build's published image result. Require
one result matching the intended image name and a complete SHA-256 digest. Bind
the Deployment and observed Pod image IDs to that result. An arbitrary digest
string is not evidence that the approved source produced the running image.

An immutable application image and a reproducible rebuild answer different
questions. The historical image used a tagged Python base, a tagged build helper
and some ranged dependencies. Its deployed digest fixed the selected bytes;
future resolution could produce different bytes. The final campaign also lacked
full container package-install logs through its inspected retrieval paths. Report
declared pins, local resolution and image identity at their actual evidence levels.

A completed setup repeat in the retained manager checked resource ownership,
source/configuration agreement, grants, Deployment UID, a hash of the admitted
Deployment spec and two available replicas. It performed no second build or
manifest apply. An interrupted setup instead refused a fresh deployment and
directed recovery toward cleanup. Do not promise resumable rollout or automatic
upgrades from that behaviour. A source change, missing grant or changed spec needs
the target's deliberate release workflow and compatibility plan.

## Reconcile accepted work without replaying it

Keep submission intent distinct from accepted identity, pending status and terminal
result. Persist the evidence needed to recover before waiting:

| Operation | Evidence to retain and reconcile |
| --- | --- |
| Cluster create/delete | Pre-submission operation inventory; exact project/location/cluster target; operation type; accepted operation name; terminal status and error; cluster identity/owner when observable |
| Image build | Unique ownership tag, intended image and submission intent; accepted build ID; terminal status; source record; exact published image/digest |
| IAM addition | Original matching binding status; exact scope/member/role/condition; intent; observed result |
| Resource creation | Original absence/collision check, unique owner marker, create intent, rejection or accepted evidence, stable provider identity |

In the tested Cloud SDK 572.0.0 path, asynchronous cluster creation returned a
Cluster and deletion returned no operation object. A double returning Operations
for both concealed the defect. Recovery compared the saved inventory with the
provider's regional operation inventory and required one uniquely new operation
with the exact target and type. Canonical target links could contain project ID
or project number. Old, unrelated, missing or multiple candidates remained
unresolved; sorting by newest time is not sufficient attribution.

For an unknown build response, reconcile the unique ownership tag and then verify
the accepted build. For cleanup, cancel an accepted nonterminal build at most
once under the recorded workflow and keep checking its terminal result before
removing source storage or accounts. A client timeout does not establish build
cancellation. Keep inventory pagination and time limits explicit.

A terminal failed CREATE can still leave owned infrastructure. Record the error
and let the authorised cleanup path continue; the deployment path must still
report failure. Conversely, even a missing cluster does not settle a recorded
DELETE whose operation remains pending or unknown. Reconcile that operation
without submitting another DELETE merely because the first client lost its
response.

## Classify absence and partial cleanup precisely

A synchronous, documented rejection plus independently verified absence can
resolve a failed creation intent. The historical Storage handler recorded its
definite rejection status; transport/server uncertainty such as HTTP 503 retained
an unresolved intent. Derive this classification from the particular API instead
of treating every non-2xx response as proof that nothing happened.

IAM introduced a separate absence case: describing a deleted service-account
email returned `PERMISSION_DENIED` with “or it may not exist.” Recovery required a
successful complete project account inventory excluding both the email and its
recorded immutable unique ID. A still-listed account, unreadable inventory,
wrong-project list or authentication failure retained uncertainty. This fallback
was specific to already-recorded owned accounts, not general permission to ignore
denied resource reads.

If a final network deletion command stops before receipt completion, reconcile
the exact Compute operation's target identity and terminal error-free result,
then verify network absence. The historical recovery did this and completed the
original cleanup receipt without another deletion. Attribute remaining managed
dependencies before acting. An independently documented concurrent cleanup can
explain a baseline difference; the difference alone does not authorise deletion.

## Interpret the historical capacity sequence correctly

1. The first attempt failed at the Storage URL after creating only two owned
   accounts. No build, cluster or model work occurred. Endpoint and IAM-absence
   repairs enabled partial cleanup.
2. The corrected attempt built the image, then exposed the CLI response-shape
   defect. The already-accepted cluster CREATE later reached terminal error 14
   reporting insufficient regional Compute resources. That finding was provider
   capacity, not proof of quota denial. Recovery and cleanup closed the attempt.
3. A separately authorised fresh campaign succeeded in the same region with no
   quota increase. Transient scale-up events still reported quota exhaustion
   before both Pods became Ready on one node. Successful routing, actual Pod
   replacement/session continuity, repeat setup and cleanup were then verified.

The source used for the final campaign matched the 89-test clean-copy suite; no
application change during that campaign explains the newly available capacity.
Preserve all three outcomes. Two Ready replicas on one node establish neither
node/zone failover nor a production availability result. Capacity retries need
fresh covered scope and closure of prior owned work; a deadline reserves cleanup
time rather than permitting abandonment.

## Test the repaired boundary

Exercise real orchestration and original shell entry points while doubling only
external transports. Preserve observed wire shapes and error cases. Checks include
no mutations after a collision or unreadable preflight, one build/apply across completed setup repetition,
preserved pre-existing IAM members, rejection of replaced resource identities,
uncertain submission refusal, one DELETE across a lost-response recovery, and
cleanup of terminal failed creation in the same recovery invocation.

Those tests establish local control flow. Retained live evidence supplies the
separate proof of actual provider acceptance, admitted configuration, workload
identity, functional requests and independent absence. Neither proof establishes
untested first-time onboarding, public access, autoscaling or production rollback.
