# Ownership, approval and recovery

Use this procedure when preparing or operating a deployment lifecycle. It generalises the tested lab guards; it is a design contract for your project's implementation, not a bundled cloud deployer. Reuse a suitable existing IaC state system instead of creating a competing one.

## Resolve a concrete plan

Before mutation, resolve every variable and show the following information. Commands in mode references are ingredients for this plan, not authorisation.

| Record | Required detail |
| --- | --- |
| Target | Project ID and verified project number; hosting, build and inference locations; selected mode; exact resource names |
| Identities | Operator/caller, build and workload identities; GKE node/KSA where relevant; proposed permission and resource scope for each grant |
| Source | Application entry point, exact Python/ADK/SDK versions, allowlisted source hashes, image digest when available |
| Baseline | Existing resource UIDs/creation times, IAM members/roles/conditions, staging object generations and shared dependencies |
| Changes | Exact commands or reviewed IaC plan, resource count and mutable properties; APIs and secrets listed separately |
| Bounds | Model attempts, builds, control-action allowance, per-call timeouts, absolute deadline, retry rules and cleanup reserve |
| Cleanup | Only created resources and added grants; object generations, sessions, tunnels and temporary kubeconfig; retained storage/history |

Read-only preflight cannot certify effective runtime permissions, model availability, quota or future costs. Distinguish an absent resource from an inaccessible API. If an expected project lookup fails, fix the selected account/access before provisioning rather than switching targets silently.

SDK subprocesses must inherit the selected project, account and quota-project settings. Sanitize inherited API keys and old deployment IDs when the approved path uses IAM. Never print credential variables or token-bearing commands. Avoid global CLI configuration changes; prefer scoped flags or a dedicated invocation environment.

## Durable state before side effects

Store a versioned **data** record outside the deployment package, readable only by the operator. At minimum record:

- Target project/location and an unpredictable ownership token.
- Source/configuration fingerprint with secret values excluded.
- Baseline resource identities and precise IAM grants already present.
- Intent, operation/build/resource identifiers, and observed result for each submitted action.
- Created resource UID/creation time, object generation, image digest and added IAM grant identity.
- Deletion progress and final receipt.

Use atomic writes and hold a lock across reading state, reconciliation and submission. Refuse a concurrent invocation. A local lock protects one host; use the project's distributed coordination if multiple hosts can deploy. Distributed coordination is production advice, not verified by the chapter lab.

Never execute a journal as shell or Python code. Changing projects requires fresh state. Missing state does not make an existing name safe to adopt. Explicitly approved updates to a pre-existing application are allowed, but that application remains outside cleanup ownership; preserve its rollback information.

## Repeat and recover

| Observation | Next action |
| --- | --- |
| Same target, fingerprint and terminal matching deployment; request is to verify completed setup | Verify identity/readiness and return the existing result; no additional build or create. |
| Existing entrypoint repeats by updating, as the recorded Runtime wrapper does | Treat a repeat as an update requiring the appropriate scope and budget; use reads for a verification-only request. Preserve the saved resource ID. |
| Source/configuration changed | Prepare an explicit update plan. Do not silently create a parallel deployment. |
| Operation/build ID exists | Poll that exact operation within bounds; verify the resulting provider object. |
| Intent saved, no returned ID, timeout or broken connection | Stop new submissions. Inspect exact target, operation/build records and audit/source receipts. Record uncertainty until identity is proved. |
| Explicit rejection before provider acceptance | Record the rejection. Prove target and matching accepted work are absent before a separately approved resubmission. |
| Resource name matches but UID/generation changed | Refuse adoption or deletion; report the replacement. |
| Permissions fail or API is disabled | Report unknown state; do not treat it as not found or broaden IAM automatically. |

The native ADK deployment CLI once printed a rejected source build and returned exit code zero. Check provider terminal state, service identity and source/build evidence in addition to subprocess status. In the tested recovery, the exact rejected archive generation was removed with a generation precondition only after service and matching build absence were established. General timeouts do not qualify for this narrow recovery.

A second model invocation is another paid attempt even when no answer appears. Retry automatically only if the operation is demonstrably idempotent and the approved policy permits it. For non-idempotent tools, use an application idempotency key/deduplication record or establish non-delivery before offering a retry. The chapter proved selected pre-dispatch retries, not arbitrary accepted-timeout safety.

## Cleanup is its own operation

1. Present the exact deletion plan and obtain confirmation. Re-read provider identities against the journal, retaining pre-existing resources and IAM grants. Source-name prefixes and labels alone are insufficient proof.
2. Ensure builds and operations are terminal before revoking permissions they still need. Delete dependants before their owned containers: sessions/workloads, services/runtimes, exact staged objects and owned repositories/buckets/cluster as applicable. Respect existing IaC dependency ordering.
3. Remove only grants that this invocation added, matching member, role and condition. Prefer conditional updates/etags so concurrent policy changes survive.
4. For bucket contents, inspect versions and remove only recorded generations using preconditions. An empty bucket requires its own bucket-delete operation; deleting objects is not deleting the bucket. Shared provider staging buckets remain shared.
5. On GKE, inventory listable persistent namespaced resource types before deleting an owned namespace or disposable cluster. Refuse unknown objects. A provider-created object still needs provenance; reconcile its exact identity against audit/control records. Do not refresh the original baseline to make new objects appear owned.
6. Persist delete-operation IDs and resume the same operations after interruption. After verified completion, preserve a tombstone/receipt. Repeat cleanup should check recorded absence, not repeat destructive calls or a full Kubernetes inventory unnecessarily.
7. Independently inspect the exact services, runtimes, clusters, repositories, buckets/object generations and IAM grants. Stop only the tunnels/processes started here. Remove temporary kubeconfig and synthetic sessions according to the approved scope.

Report `absent`, `retained`, `unknown/inaccessible` and `pending operation` separately. Provider-managed backing resources, build logs, storage soft-delete retention and billing-report delay can limit a zero-cost claim. Do not delete an entire project or unrelated VMs, databases or RAG corpora as a shortcut.

## Budget the teardown

The original campaign recorded 917 non-model action units against 600 approved: 471 before teardown and another 446 for cleanup, provenance and independent checks. A GKE inventory read roughly 68 resource types, and late provider objects caused safe refusals and re-inventory. These figures are historical observations, not exact HTTP counts or billable-operation counts.

Budget setup, testing, diagnostics, full cleanup, one recovery inventory, repeat cleanup and independent verification before allocating optional tests. SDK polling and Kubernetes fan-out mean one shell command may consume many requests. Track conservative action units alongside model/build counts. If the reserve is insufficient, stop optional work and seek a revised explicit scope; do not bypass ownership checks or silently exceed approval.
