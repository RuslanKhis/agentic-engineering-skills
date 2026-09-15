# Writes, confirmation and uncertain outcomes

Use this workflow for refunds, orders, cancellations or other external mutations. These are production principles, not verified Chapter 1 features. That example deduplicates internal retries within one invocation; it has no durable operation ledger, business authorisation or deterministic guard against another tool invocation.

## 1. Establish replay safety

Inspect the actual provider operation, SDK retries and application call paths. Unknown write semantics mean **no automatic retries**, including hidden SDK retries. Enable replay only when the provider's contract protects this operation. Record key scope, retention, payload comparison, concurrent-request behaviour and supported status lookup. An HTTP method, timeout or chosen header name does not establish deduplication.

Preserve existing versions, interfaces and result schemas. Implement requested safeguards within the project's architecture; in a review, report missing protections with evidence.

## 2. Prepare one authorised operation

Obtain the principal from authenticated application context. Check authority and current business preconditions. Confirmation records consent; it does not authenticate the caller or grant business permission.

Use exact money where applicable: validate currency, positive finite amount, precision and limits with the project's decimal or minor-unit representation. Validate strings before conversion; reject excess precision instead of silently rounding. Adapt at the existing boundary and make any required public-interface migration explicit.

Derive the business operation identity from trusted state under the actual business rule. A newly generated UUID per tool call cannot recognise a repeated operation. Atomically create or load a durable record with a uniqueness constraint, binding the operation ID to the canonical payload, payload fingerprint, relevant revision, approval and one provider key. Commit before dispatch. Same identity and payload loads the existing operation; changed payload requires rejection or an explicit correction workflow.

Coordinate competing workers through the existing shared store and conditional updates. Define abandoned-claim recovery: lease expiry alone cannot authorise another dispatch while an earlier worker might still finish. Separate operation IDs can still overdraw one balance; enforce balance/precondition changes atomically in the authoritative system.

## 3. Dispatch and reconcile

Every permitted retry uses the same stored key and payload within the provider's scope and retention window. Apply cooperative budgets from [reads and deadlines](reads-and-deadlines.md); cancellation after dispatch leaves the write potentially applied.

Record what is known: prepared/pending, confirmed applied, reliably not applied, or unknown. Preserve the current public schema; add richer outcome/recovery fields only through a compatible change. `not_applied` needs evidence covering **all dispatched attempts**. A later rejected attempt does not resolve an earlier lost response.

On timeout, connection loss, exhaustion or a crash before saving the result, reconcile through the provider's supported lookup or protected same-operation replay. Recover abandoned pending records too. An expired deduplication window needs reconciliation, not a new key. Return an authorised recovery reference and honest uncertainty; never tell the user that an ambiguous refund definitely failed or invite a fresh refund.

If the project has no ledger, keep its limited scope explicit. Reuse existing infrastructure if available; do not invent claims of durability. Permit only recovery justified by the provider contract, and leave cross-invocation or restart recovery as a concrete gap when outside the requested work. Unknown writes remain ineligible for automatic replay.

## 4. Enforce the execution boundary

For ADK, inspect the installed confirmation wrapper and actual session/Runner path. Verify missing or rejected confirmation causes zero provider calls. When ADK returns `"This tool call is rejected."`, report that the action was cancelled and no payment was attempted. This is distinct from an unknown outcome after dispatch.

Direct Python calls bypass ADK's wrapper. Secure every supported entry point at the appropriate service boundary. Without ADK, use the framework's equivalent approval mechanism or application gate. Enforce repeated-operation behaviour in code; prompts, session persistence and model-call limits are not operation deduplication.

## Completion criteria

Use deterministic local tests for the relevant changed paths: loss after commit produces one effect; retries preserve identity/payload; repeated calls or workers converge; changed payload is rejected; crash recovery and expired retention avoid fresh dispatch; later rejection preserves earlier uncertainty; invalid/unauthorised/unapproved requests make zero provider calls; direct-call behaviour matches its documented boundary. Exercise the real framework confirmation path when present. Preserve result compatibility and distinguish offline application evidence from live model behaviour. Report missing infrastructure or unverified contracts explicitly.
