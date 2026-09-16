# Human review and truthful outcomes

Read for high-risk writes, payment-like actions, approval gates or uncertain retries. Outcome: the model can propose an operation while trusted application code controls permission and execution.

## Preserve the distinction between permission and completion

Return explicit states such as `invalid_request`, `pending_approval`, `approved`, `executing`, `completed`, `rejected`, `expired`, `failed` and `outcome_unknown`, adapting existing API names. An approval-only action must say no external operation was performed. In a refund demonstration, return `payment_processed: false` and pass that fact into the actual subsequent model request. Only verified execution evidence can justify “paid” or “refunded”.

Test both the actual tool result and the model request that receives it. A scripted final answer proves wiring, not model compliance; an approved, bounded live conversation tests selected model behaviour separately. Where false completion claims are unacceptable, render critical status deterministically from stored state instead of relying solely on generative wording.

Validate amounts before any approval/publication: positive, finite, correct currency/precision, not booleans or unsupported types. Use integer minor units or validated decimals as the application's currency policy requires. Bind order ownership, user and tenant outside the model schema; a model-supplied `user_id` is not authentication. Ask for missing business inputs before calling the tool.

## Decide local demonstration or durable operation

A mock publisher demonstrates routing only. Fresh UUIDs on every request, in-memory lists, Pub/Sub delivery and instructions saying “do not repeat” do not create durable review or exactly-once effects. If production explicitly selects a transport/store, fail clearly when configuration is missing instead of silently falling back to a mock.

## Durable record and transaction recipe

The following schema and state transitions are **production design**, not a service bundled with this skill or implemented by the companion. Adapt them to the chosen database and provider contract, then verify their concurrency and recovery semantics.

| Durable record | Minimum information and purpose |
| --- | --- |
| Business operation | Stable operation ID scoped to its tenant, canonical payload and payload digest, requester, provider idempotency key, operation state and version; retains the exact authorised action across retries |
| Review | Opaque review reference, operation link, tenant, requester, decision/version, creation/expiry times and authorised decision actor; one decision for the stored proposal |
| Outbox | Stable event ID, schema/event type, opaque review reference and publication state; records notification work in the same transaction as the state change |
| Audit | Actor, action, operation reference, time and allowlisted decision/reason fields; access-controlled history with a retention policy |

Bind the principal at the application/tool adapter; the model supplies business inputs, not tenant, requester, approver or provider key. Verify order ownership and eligibility against trusted records. Keep caller context isolated across concurrent invocations; a mutable process-global principal can bind one user's request to another user.

For creation, authorise first, canonicalise the payload, then atomically create or retrieve the operation, review, outbox and audit records. Enforce a unique tenant/operation key and review linkage; handle competing inserts by reading the committed existing record. `SELECT FOR UPDATE` does not lock a nonexistent row. Reusing the operation ID with a changed payload is a conflict. Reusing it unchanged returns the existing state; issuing a fresh random ID for every retry bypasses that protection.

Choose the business key at the intended operation granularity. An order may legitimately have several distinct partial-refund operations; deduplicating forever by order ID alone would block them. Trusted application code must distinguish a retry of one authorised operation from a new eligible operation.

The notification payload contains only schema version, event type and an opaque review reference. Keep order IDs, amounts, free-text reasons, customer identities and provider keys in the protected record. Consumers authenticate and load the record before acting. An opaque identifier is not authorisation: status lookup also checks the caller's tenant and permission before disclosing a review, its existence or its outcome.

## Authorised transitions and recovery

Implement conditional state/version transitions and audit them in the same transaction. The names below are illustrative; preserve compatible existing API names.

| Transition | Condition and resulting authority |
| --- | --- |
| Pending → approved/rejected | Authenticate the reviewer, check tenant and action permission, enforce separation of duties where required, and check expiry; repeated decisions return the stored result |
| Pending → expired/cancelled | A trusted expiry process or authorised cancellation wins only while the operation is still pending; subsequent approval cannot revive it |
| Approved → executing | A worker atomically claims the authorised operation and uses its stored payload/key; duplicate approval messages observe the existing claim/state |
| Executing → completed | Trusted provider evidence confirms the effect; store the provider reference before reporting completion |
| Executing → failed | A confirmed final provider rejection; distinguish execution failure from a human rejecting the proposal |
| Executing → outcome_unknown | Timeout or crash leaves acceptance uncertain; reconcile by the persisted key/reference before any further write |

Approval is a permission transition. It performs no external effect itself. A claim/lease expiring after a crash also does not prove that the provider did nothing. Where the provider offers neither safe idempotency nor a lookup contract, send uncertain outcomes to manual reconciliation rather than issuing a new key.

Use crash injection at the transaction and external-call boundaries:

| Failure point | Required recovery and observable assertion |
| --- | --- |
| Before creation commits | No review/outbox record is visible and no notification/provider call occurred |
| After commit, before publication | The review remains queryable; a worker retries the committed outbox entry |
| After publish acceptance, before marking published | Publication may repeat with the same event/reference; the consumer performs one authorised transition |
| Concurrent or repeated reviewer decisions | One permitted transition wins; the other observes it, without another execution event |
| After provider acceptance, before storing success | The operation remains uncertain; recovery reconciles with the same key instead of assuming failure |
| After storing completion, before final notification | Status lookup returns completion; notification retries do not execute the operation again |

Publish committed outbox entries, wait for bounded acknowledgement, then mark them published. A failed or timed-out publish leaves retryable notification work. A durable queued record permits “queued for review”; it does not establish delivery to a person. The companion's direct publisher has no outbox: its offline test verifies that an acknowledgement error propagates rather than returning `pending_approval`.

Define final-result notification and authenticated status lookup alongside creation. They let a user learn the outcome after the original agent invocation ends, without replaying the action. For deployment, persistence and worker lifecycle checks, use [serving and lifecycle](serving-and-lifecycle.md).

## Choose confirmation or a separate review service

ADK's [Tool Confirmation](https://adk.dev/tools-custom/confirmation/) can supply an interaction mechanism for a client that promptly resumes its invocation. Before adopting it, inspect the installed version and verify support for the actual session backend. Preserve the function-call identity in the confirmation response and, when the resume contract requires it, the original invocation ID. Test the real client reconnect/resume path; merely sending an approval Boolean does not establish reviewer authority or durable execution.

Use a separate durable review operation when another person decides, decisions may take hours or days, or completion must survive process/client restarts. Historical ADK session-backend restrictions are version-sensitive; recheck official documentation rather than inheriting a compatibility claim from the chapter.

Acceptance tests: unauthorised/forged identity causes zero writes; another tenant cannot read an opaque review reference; invalid amounts cause zero publication; missing required inputs cause clarification and zero tool calls; pending retries return the same operation; changed-payload reuse conflicts; expiry/cancellation race safely with approval; the crash table's recovery assertions hold; final user-visible text reflects approval versus completion. Pair the clarification case with a complete request that creates one appropriate operation. Treat actual storage, reviewer transport and provider guarantees as unverified until those integrations are exercised.
