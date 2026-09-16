# Operate and validate a memory application

Use this reference when planning paid acceptance, resuming a failed campaign, or cleaning up created resources. A request to review architecture or write documentation does not authorise a live campaign.

Use [managed-deployment.md](managed-deployment.md) for configuration, identity
and deployment ordering; use [failure-recovery.md](failure-recovery.md) for
specific retry, quota, credential, probe and cleanup failure decisions.

## 1. Establish a read-only baseline

- Locate the application, deployment guides, configuration schema, dependency constraints, source hashes and latest dated evidence. Resolve paths in the current repository; source paths in the provenance reference are not a required layout.
- Record the intended account, project, quota project, resource locations and workload identities. Pin these per command or client; inspect access without changing global CLI defaults.
- Check required APIs, billing availability and effective quotas through read-only interfaces. Preserve missing permissions, disabled APIs and unreachable regions as unresolved checks.
- Inspect nested application configuration without printing secrets. A changed root environment file does not prove that child configuration or API keys changed.
- Inventory existing resources and retained deployment journals. For a new project or campaign, allocate fresh state and resource IDs; retain old journals for reconciliation.
- Record the dependency set in the target’s existing selected environment. Distinguish a reproducible package snapshot from a requirements file containing version ranges.
- List required functional gates: authentication/isolation, model/tool calls, exact-scope memory generation and recall, restart/recall, and personal-state erasure with a populated control user.

Complete this phase when target identity, readable prerequisites, existing ownership and unresolved gates are recorded. Do not provision capacity to discover a known missing prerequisite.

## 2. Make the campaign reviewable and establish authority

- Write the exact resource and regional scope, permitted mutations, identities, synthetic fixtures, proposed commands, expected costs and cleanup inventory.
- Bound elapsed time, model/write attempts, query bytes, setup retries, worker executions and one full-smoke allowance. Reserve capacity and time for audit export and cleanup.
- Separate a planning allowance from a provider-enforced spending cap; neither an estimate nor a request counter is an invoice.
- Reuse explicit approval already given for the same scope. Obtain missing approval before paid resource creation, API/billing/quota changes, or broader irreversible deletion; identify the precise new action requiring it.
- Treat a quota request as submitted until independent readback confirms its effective grant. Read existing preferences before resubmitting an uncertain request.
- For regional RAG teardown, establish exclusive scope and stopped external writers/readers. Visible corpora, local locks and recorded operations alone cannot prove that another process has no outstanding work.

Complete this phase when the concrete campaign is authorised and its prerequisites support the permitted attempt. Approval of a quota request does not mean the provider granted capacity.

## 3. Run within the recorded bounds

- Freeze the source and resolved dependencies used for execution. Use fresh resource state and the repository's supported setup, verification and recovery paths.
- Record a stable operation/job identity before a potentially accepted mutation where supported. Persist returned long-running operation handles immediately, with scope and reconciliation status.
- After timeout, cancellation or lost response, inspect the saved handle. An absent local result does not prove that the provider accepted no work.
- Resume a recorded setup operation rather than starting replacement work. Retry only eligible failures within the approved attempt budget; never blindly repeat model turns, memory writes or the full smoke.
- Measure protection-call fan-out. Per-process concurrency limits do not enforce a shared per-minute quota across replicas. Validate any pacing or batching change at the actual protection boundary.
- On a stop condition, preserve safe diagnostics and switch to reconciliation and authorised cleanup. Keep fail-closed screening intact.
- When a tool result is blocked after execution, reconcile its possible side effect before retrying. A user-visible failure can coexist with a provider-side write.

Complete this phase with each gate labelled PASS, FAIL, NOT RUN or UNKNOWN and linked to its actual evidence. A listing of resources is not application acceptance.

## 4. Preserve evidence before deleting it

- Record source hashes, interpreter/platform, resolved packages, configuration profile, timestamps, exit statuses, safe outcome codes and operation identities.
- Before deleting jobs or parent resources, export the complete execution inventory and final audit evidence. Preserve missing snapshots as missing; absence checks cannot recreate them.
- Keep raw sessions, provider errors, tokens and private metadata out of public reports. Store necessary private evidence under restrictive permissions and publish allowlisted summaries.
- Separate dispatch intents, accepted operations, completed operations, retrieval readiness, retained bytes and billed usage. Count nested/child operations according to their service semantics.
- Test erasure through the authorised subject workflow, including uncertain writes, repeat, exact absence and control-user preservation. Whole-lab teardown does not prove privacy deletion.
- Report changed scope or source explicitly. A historical PASS, a doubled SDK failure or an offline suite does not verify an unexecuted hosted path.

Complete this phase when another operator can tell what happened, which assertions passed, and which evidence cannot support a stronger claim.

## 5. Clean up owned resources and regional backends separately

- Reconcile accepted writes and stop owned serving/worker activity before teardown. Use the ownership journal to remove only the created resources and added grants in the authorised scope.
- Verify terminal deletion operations and independent resource absence; repeat the supported cleanup command to check completed-state recovery.
- Delete the ordinary lab before a separately owned RAG foundation. Zero corpora does not establish that a regional Spanner-backed RAG backend is unprovisioned.
- Setting a Spanner-mode RAG backend to Unprovisioned is a broader irreversible regional action. Perform it only with specific authority and exclusivity checks; preserve unrelated backends and data.
- An empty Basic configuration alone does not prove running billable capacity or ownership. Read provider state and retained provenance; report ambiguity rather than guessing.
- If a provider-managed serverless IP reservation blocks subnet deletion, observe its release and retry scoped cleanup. Do not delete the provider reservation or an unrelated address to force progress.
- Schedule a cleanup monitor only when requested, with a defined scope and stop condition. Keep unchanged polling quiet and notify on meaningful progress or required action.
- Inventory retained object versions, soft-deleted data, pending operations and inaccessible regions. Preserve original credentials/configuration and explicitly retained API/quota changes.
- State separately: active resources removed, retention still running, checks unavailable, and earlier charges possibly arriving later. Active-resource cleanup is not a zero-cost guarantee.

Complete cleanup when every owned target is absent, terminal/inactive or explicitly pending with an owner and next action. Never convert unknown inventory or retained billable data into an all-clear.

Historical outcomes, source anchors and unverified hosted gates are recorded in [provenance.md](provenance.md). They do not certify the current target.
