# Writes, confirmation and uncertain outcomes

Use this workflow for refunds, orders, cancellations or other external mutations. These are production principles, not verified Chapter 1 features. That example deduplicates internal retries within one invocation; it has no durable operation ledger, business authorisation or deterministic guard against another tool invocation.

## 1. Establish replay safety

Inspect the actual provider operation, SDK retries and application call paths. Unknown write semantics mean **no automatic retries**, including hidden SDK retries. Enable replay only when the provider's contract protects this operation. Record key scope, retention, payload comparison, concurrent-request behaviour and supported status lookup. An HTTP method, timeout or chosen header name does not establish deduplication.

Preserve existing versions, interfaces and result schemas. Implement requested safeguards within the project's architecture; in a review, report missing protections with evidence.

## 2. Prepare one authorised operation

Obtain the principal from authenticated application context. Check authority and current business preconditions. Confirmation records consent; it does not authenticate the caller or grant business permission.

Use exact money where applicable: validate currency, positive finite amount, precision and limits with the project's decimal or minor-unit representation. Validate strings before conversion; reject excess precision instead of silently rounding. Adapt at the existing boundary and make any required public-interface migration explicit.

Bound input size before decimal conversion and follow the supported currency's precision; not every currency has two fractional digits. Keep the provider replay key private. Return an access-controlled application operation reference for recovery, and check authority again when that reference is used.

Derive the business operation identity from trusted state under the actual business rule. A newly generated UUID per tool call cannot recognise a repeated operation. Atomically create or load a durable record with a uniqueness constraint, binding the operation ID to the canonical payload, payload fingerprint, relevant revision, approval and one provider key. Commit before dispatch. Same identity and payload loads the existing operation; changed payload requires rejection or an explicit correction workflow.

Coordinate competing workers through the existing shared store and conditional updates. Define abandoned-claim recovery: lease expiry alone cannot authorise another dispatch while an earlier worker might still finish. Separate operation IDs can still overdraw one balance; enforce balance/precondition changes atomically in the authoritative system.

## 3. Dispatch and reconcile

Every permitted retry uses the same stored key and payload within the provider's scope and retention window. Apply cooperative budgets from [reads and deadlines](reads-and-deadlines.md); cancellation after dispatch leaves the write potentially applied.

Record what is known: prepared/pending, confirmed applied, reliably not applied, or unknown. Preserve the current public schema; add richer outcome/recovery fields only through a compatible change. `not_applied` needs evidence covering **all dispatched attempts**. A later rejected attempt does not resolve an earlier lost response.

Validate provider success data at the [adapter boundary](reads-and-deadlines.md#replace-the-mock-at-a-defined-adapter-boundary) before recording a confirmed result. For an ambiguous result, a recovery field such as `same_operation_only` means a trusted recovery component loads and reconciles the existing operation; it is not permission for the model to call the write immediately again. Separate the question “may this model invoke another tool?” from “may the service safely recover this already authorised operation?”.

On timeout, connection loss, exhaustion or a crash before saving the result, reconcile through the provider's supported lookup or protected same-operation replay. Recover abandoned pending records too. An expired deduplication window needs reconciliation, not a new key. Return an authorised recovery reference and honest uncertainty; never tell the user that an ambiguous refund definitely failed or invite a fresh refund.

If the project has no ledger, keep its limited scope explicit. Reuse existing infrastructure if available; do not invent claims of durability. Permit only recovery justified by the provider contract, and leave cross-invocation or restart recovery as a concrete gap when outside the requested work. Unknown writes remain ineligible for automatic replay.

## 4. Enforce the execution boundary

For ADK, inspect the installed confirmation wrapper and actual session/Runner path. Verify missing or rejected confirmation causes zero provider calls. When ADK returns `"This tool call is rejected."`, report that the action was cancelled and no payment was attempted. This is distinct from an unknown outcome after dispatch.

Direct Python calls bypass ADK's wrapper. Secure every supported entry point at the appropriate service boundary. Without ADK, use the framework's equivalent approval mechanism or application gate. Enforce repeated-operation behaviour in code; prompts, session persistence and model-call limits are not operation deduplication.

Immediately before dispatch, revalidate authority, current business preconditions and the approved action, amount, currency and revision. They may have changed while the confirmation dialog was open. A mismatch follows the defined correction/reapproval flow and sends no provider request. An earlier approval must not silently authorise a different payload. Bind any balance reservation or conditional state update atomically so concurrent operations cannot both pass a stale balance check.

## When the workflow also applies events to owned state

This branch is for an API integration that ingests status events or changes an application-owned projection. It is a production design principle, not a database implementation supplied or tested by the chapter. Keep the project's existing database; do not add one for unrelated API work.

A transaction makes its own changes atomic, but two valid transactions can still apply the same increment twice. Implement the following with the store's actual transactional and uniqueness guarantees:

1. Define an immutable event ID in its source/tenant namespace, its canonical payload and the source's ordering contract. Preserve the source timestamp on replay; local reception time is different metadata.
2. Atomically insert the event under a uniqueness constraint. On an existing ID, compare the stored payload: an identical duplicate is a no-op, while changed data is a conflict, not a successful deduplication.
3. Apply the projection only for an accepted event whose source ordering is newer than the stored projection. Keep ledger insertion and the conditional projection update in the same transaction. A new but stale event can be recorded without regressing current state.
4. Define conflicting ordering ties and ledger retention explicitly. Version-first ordering is suitable only if the source contract says so; timestamps alone are not a universal ordering rule. Expiring an event record can reopen its replay window.

Validate duplicate delivery, changed payload under the same ID, out-of-order delivery, conflicting ties and concurrent acceptance. In PostgreSQL, `ON CONFLICT DO NOTHING` alone does not compare payloads; an accepted-event result can gate the following state update. Adapt to the target dialect instead of copying PostgreSQL into BigQuery or another database. A local transaction still cannot roll back a remote payment; use the provider's protected replay or reconciliation for that side effect.

## Completion criteria

Use deterministic local tests for the relevant changed paths: loss after commit produces one effect; retries preserve identity/payload; repeated calls or workers converge; changed payload is rejected; crash recovery and expired retention avoid fresh dispatch; later rejection preserves earlier uncertainty; invalid/unauthorised/unapproved or stale-approved requests make zero provider calls; direct-call behaviour matches its documented boundary. Exercise the real framework confirmation path when present. Preserve result compatibility and distinguish offline application evidence from live model behaviour. Report missing infrastructure or unverified contracts explicitly.
