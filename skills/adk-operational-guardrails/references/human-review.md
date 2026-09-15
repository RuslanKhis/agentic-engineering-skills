# Human review and truthful outcomes

Read for high-risk writes, payment-like actions, approval gates or uncertain retries. Outcome: the model can propose an operation while trusted application code controls permission and execution.

## Preserve the distinction between permission and completion

Return explicit states such as `invalid_request`, `pending_approval`, `approved`, `executing`, `completed`, `rejected`, `expired`, `failed` and `outcome_unknown`, adapting existing API names. An approval-only action must say no external operation was performed. In a refund demonstration, return `payment_processed: false` and pass that fact into the actual subsequent model request. Only verified execution evidence can justify “paid” or “refunded”.

Test both the actual tool result and the model request that receives it. A scripted final answer proves wiring, not model compliance; an approved, bounded live conversation tests selected model behaviour separately. Where false completion claims are unacceptable, render critical status deterministically from stored state instead of relying solely on generative wording.

Validate amounts before any approval/publication: positive, finite, correct currency/precision, not booleans or unsupported types. Use integer minor units or validated decimals as the application's currency policy requires. Bind order ownership, user and tenant outside the model schema; a model-supplied `user_id` is not authentication. Ask for missing business inputs before calling the tool.

## Decide local demonstration or durable operation

A mock publisher demonstrates routing only. Fresh UUIDs on every request, in-memory lists, Pub/Sub delivery and instructions saying “do not repeat” do not create durable review or exactly-once effects. If production explicitly selects a transport/store, fail clearly when configuration is missing instead of silently falling back to a mock.

For a production operation:

1. Derive or accept a trusted stable business-operation ID, with canonical payload, tenant, requester and stored provider idempotency key. Persist it before dispatch. Changed payload under the same ID is a conflict. The same payload with a new random ID is not replay protection.
2. Authorise the requester and resolve eligibility/ownership in trusted code. Atomically create the operation and notification outbox record. Enforce a uniqueness constraint and handle insertion races; `SELECT FOR UPDATE` does not lock a nonexistent row.
3. Return the existing operation on repeats, including when it remains pending. Make notification delivery retryable and deduplicated; Pub/Sub is a transport, not the review record or proof a person received it.
4. Authenticate and authorise the reviewer for that operation. Apply a conditional state/version transition once, with expiry and separation-of-duties policy where required. A supplied approval Boolean/dataclass is not authority.
5. Execute only from the authorised state, with a persisted provider key and ownership/concurrency controls. Approval itself moves no money. Duplicate worker delivery and reviewer clicks must not duplicate effects.
6. If the provider outcome is unknown, persist that state and reconcile before retrying. If no safe provider idempotency or lookup contract exists, route to manual reconciliation. Do not mint a fresh key to clear an error.

Retain access-controlled audit facts needed for review without exposing customer payloads to routine model logs. Define cancellation, expiry, rejection, final failure and notification recovery, not just the happy path.

ADK's [Tool Confirmation](https://adk.dev/tools-custom/confirmation/) may supply an interaction mechanism. Check the pinned version, session backend and resumption contract before adoption. An interaction confirmation does not by itself establish a durable authorised business operation.

Acceptance tests: unauthorised or forged identity causes zero writes; invalid amounts cause zero publication; pending repeats return the same operation; concurrent review decisions cause one transition; restart and redelivery cause one external effect; publish failure never reports successful submission unless a durable queued record actually exists; provider timeout leads to reconciliation; final user-visible text reflects approved versus completed state. Treat storage/provider tests as unverified until those integrations are exercised.
