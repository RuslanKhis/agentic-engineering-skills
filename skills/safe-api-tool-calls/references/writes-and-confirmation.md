# Writes, confirmation and uncertain outcomes

Use this workflow for refunds, orders, cancellations or other external mutations. These are production principles, not verified Chapter 1 features. That example deduplicates internal retries within one invocation; it has no durable operation ledger, business authorisation or deterministic guard against another tool invocation.

## 1. Establish replay safety

Inspect the actual provider operation, SDK retries and application call paths. Unknown write semantics mean **no automatic retries**, including hidden SDK retries. Enable replay only when the provider's contract protects this operation. Record key scope, retention, payload comparison, concurrent-request behaviour and supported status lookup. An HTTP method, timeout or chosen header name does not establish deduplication.

An ADK graph `Workflow` adds a replay path of its own. From google-adk 2.9.0 a node that failed runs again from the top when the workflow resumes; the changelog says it outright: "a node that performs an external side effect and then fails will perform that side effect again on every resume" (CHANGELOG 2.9.0, 91573eb, read 2026-10-22). On 2.8.0 the failed node replayed as completed instead. Treat a node body that writes as a retry site: the same authorised operation, canonical payload and provider replay key apply inside it, and an uncertain outcome is reconciled before the body runs again. `adk-workflow-design` owns the node structure; this reference owns the key and the reconciliation.

Preserve existing versions, interfaces and result schemas. Implement requested safeguards within the project's architecture; in a review, report missing protections with evidence.

## 2. Prepare one authorised operation

<!-- shared:verified-principal -->
**Identity comes from a verified principal.** Verify the caller's credential
at the server (signature, issuer, audience, expiry and required claims, with
the pinned provider library) and derive one internal principal from it. An
email address, a client-sent `user_id`, a session or thread locator, an
invocation ID, a model-chosen argument, user text and editable headers or
session state never prove identity. That principal is the only source of the
ADK `user_id` on every Runner and session call, of the owner key on every
record, and of the subject every tool and credential lookup acts for. Tools
read it from trusted context (`tool_context.user_id`, `ToolContext.session.user_id`
or the pinned SDK's accessor), never from their own arguments. Create and load
sessions under it; an unknown or foreign session fails without revealing that
it exists. A verifier outage and an invalid credential both deny access; only
the invalid credential should prompt a new sign-in.

ADK's own API server (`adk api_server`, `adk web`, `get_fast_api_app()`)
authenticates no end user: the session routes take `user_id` from the path and
`/run` and `/run_sse` from the body. ADK 2.12.0's change "take the ADK user id
only from an authenticated principal" (d0c4060) applies to the A2A request
converter only; it authenticates nothing on those HTTP routes. Keep them
behind IAP or the application's verified-principal dependency, or on internal
ingress. A test that sends a different caller-supplied `user_id` checks lookup
partitioning, not cross-user security; a cross-user claim needs distinct
authenticated principals at the real boundary.
<!-- /shared:verified-principal -->

Check authority and current business preconditions. Confirmation records consent; it does not authenticate the caller or grant business permission. Where the store or a downstream auditor must detect a tampered or fabricated write, sign the canonical payload with a key the agent process holds and the model never sees, and verify the signature where the write lands: Google's zero-trust blueprint does this with a local HMAC in its demo and names Cloud KMS as the production key holder, with a ledger audit that fails on an edited amount (GoogleCloudPlatform/generative-ai commit 3a716a8, `agents/adk/zero-trust-agents/README.md`, read 2026-10-22; vendor sample). The signature proves origin and integrity; the idempotency key and the operation record below still own replay and reconciliation.

Use exact money where applicable: validate currency, positive finite amount, precision and limits with the project's decimal or minor-unit representation. Validate strings before conversion; reject excess precision instead of silently rounding. Adapt at the existing boundary and make any required public-interface migration explicit.

Bound input size before decimal conversion and follow the supported currency's precision; not every currency has two fractional digits. Keep the provider replay key private. Return an access-controlled application operation reference for recovery, and check authority again when that reference is used.

Derive the business operation identity from trusted state under the actual business rule. A newly generated UUID per tool call cannot recognise a repeated operation. Atomically create or load a durable record with a uniqueness constraint, binding the operation ID to the canonical payload, payload fingerprint, relevant revision, approval and one provider key. Commit before dispatch. Same identity and payload loads the existing operation; changed payload requires rejection or an explicit correction workflow.

Coordinate competing workers through the existing shared store and conditional updates. Define abandoned-claim recovery: lease expiry alone cannot authorise another dispatch while an earlier worker might still finish. Separate operation IDs can still overdraw one balance; enforce balance/precondition changes atomically in the authoritative system.

## 3. Dispatch and reconcile

Every permitted retry uses the same stored key and payload within the provider's scope and retention window. Apply cooperative budgets from [reads and deadlines](reads-and-deadlines.md); cancellation after dispatch leaves the write potentially applied.

Record what is known: prepared/pending, confirmed applied, reliably not applied, or unknown. Preserve the current public schema; add richer outcome/recovery fields only through a compatible change. `not_applied` needs evidence covering **all dispatched attempts**. A later rejected attempt does not resolve an earlier lost response.

Validate provider success data at the [adapter boundary](reads-and-deadlines.md#replace-the-mock-at-a-defined-adapter-boundary) before recording a confirmed result. For an ambiguous result, a recovery field such as `same_operation_only` means a trusted recovery component loads and reconciles the existing operation; it is not permission for the model to call the write immediately again. Separate the question “may this model invoke another tool?” from “may the service safely recover this already authorised operation?”.

On timeout, connection loss, exhaustion or a crash before saving the result, reconcile through the provider's supported lookup or protected same-operation replay. Recover abandoned pending records too. An expired deduplication window needs reconciliation, not a new key. Return an authorised recovery reference and honest uncertainty; never tell the user that an ambiguous refund definitely failed or invite a fresh refund.

If the project has no ledger, keep its limited scope explicit. Reuse existing infrastructure if available; do not invent claims of durability. A durable-execution engine around the agent (Temporal, DBOS or Restate through their ADK plugins) does not retire the key or the reconciliation: the engine checkpoints a step's result, so a crash after the provider accepted the write and before the checkpoint re-executes the step, and only the key makes that second execution a no-op at the provider. The kill-after-the-write test proves this: kill the process after the tool returns and its step is checkpointed (the body ran once), and after the provider accepted but before the checkpoint (one effect at the provider double through the key, two without it); the same kill on plain resume shows the duplicate the key absorbs. Permit only recovery justified by the provider contract, and leave cross-invocation or restart recovery as a concrete gap when outside the requested work. Unknown writes remain ineligible for automatic replay.

## 4. Enforce the execution boundary

For ADK, inspect the installed confirmation wrapper and actual session/Runner path. Verify missing or rejected confirmation causes zero provider calls. When ADK returns `"This tool call is rejected."`, report that the action was cancelled and no payment was attempted. This is distinct from an unknown outcome after dispatch. The operation record from section 1 is the guard against a repeated approval.

<!-- shared:tool-confirmation -->
**ADK tool confirmation mechanics** (google-adk 2.8.0 and 2.12.0 source, read
2026-10-27; confirm on the installed version):

- `FunctionTool(func, require_confirmation=True)` asks before every call;
  `require_confirmation=` also takes a callable, so the threshold lives in code
  that sees the arguments, not in the prompt. `McpToolset(require_confirmation=...)`
  applies the same to server tools.
- On `FunctionTool` the callable is invoked with the tool function's own
  validated arguments as keyword arguments, plus the context parameter only
  when the tool function declares one, so its parameters must match the
  function's. On `McpTool` it receives the tool arguments plus `tool_context`
  when the callable's own signature names it (or takes `**kwargs`). Sync and
  async callables both work.
- Return a strict `bool`. `None` or another falsy value lets the call run
  unconfirmed (community report #7010), and from 2.10.0 the framework's gate
  holds a call only on exactly `True`.
- Order on 2.12.0 (`flows/llm_flows/tools/_caller.py`): the plugin's
  `before_tool_callback`, each agent `before_tool_callback` in order, the
  confirmation gate, then the tool body. The confirmed resume re-dispatches the
  original call through the same path, so a `before_tool_callback` runs again
  and may refuse it. A bound that must hold whatever the model or the approver
  does lives in the tool body or the store, with the callback as the early
  refusal.
- With no confirmation attached, the call returns `{"error": "This tool call
  requires confirmation, please approve or reject."}`, sets
  `skip_summarization` and records a request through
  `tool_context.request_confirmation(hint=..., payload=...)`, keyed by the
  `function_call_id` (which must be present). A rejected confirmation returns
  `{"error": "This tool call is rejected."}` and the body never runs: report
  it as a cancellation with no attempt, not as an unknown outcome.
- Inside a tool, `tool_context.request_confirmation(hint=, payload=)` pauses
  with a message and the structure the approver must return; the reply
  arrives as `tool_confirmation.payload`. Below 2.10.0 a custom `BaseTool` must
  check `tool_context.tool_confirmation.confirmed` itself; from 2.10.0 the
  framework holds any tool whose `check_require_confirmation` answers `True`,
  and `BaseTool`'s default answers `False`, so a custom tool overrides that
  hook.
- The client answers with a `function_response` named
  `adk_request_confirmation` whose `id` is that request's `function_call_id`
  and whose `response` holds `confirmed` and `payload`; with resumability it
  also carries the original `invocation_id`. On 2.12.0 the framework refuses a
  confirmation whose original call's name or arguments differ from the call in
  history (`flows/llm_flows/tools/_confirmation.py`).
- The answer must come from the authenticated controlling user through the
  application's API, never from A2A, an unauthenticated `/run` or text the
  model wrote. Confirmation records consent; it does not authenticate the
  caller or grant business permission. Forged confirmation responses in
  history were fixed in 2.5.0 and 2.6.0; 2.11.0 adds HMAC stamps with
  `ToolCallIntegrityPlugin`.
- ADK 2.12.0 runs a confirmed tool once per approval (CHANGELOG, bfdeb4a,
  closes #7434); below 2.12.0 a re-sent approval could run the tool again. The
  resume page warns that long-running functions may run more than once when
  resuming. On every version, test a duplicate approval reply and keep an
  operation record or idempotency key: it, not the framework, makes a repeated
  approval converge on one effect.
- 2.12.0 accepts `require_confirmation` on workflow nodes (`@node`,
  `FunctionNode`; 988fd1a), so a gate can sit on the node rather than inside a
  tool; it is absent on 2.8.0. From 2.9.0 a failed node re-runs on resume, so a
  confirmed node whose body writes externally still needs the idempotency key.
- The confirmation page (adk.dev, read 2026-10-22) lists
  `DatabaseSessionService` and `VertexAiSessionService` as unsupported. With a
  persistent session store, a decision that may take hours, another person
  deciding, or completion that must survive restarts, use a durable review
  record instead of the in-session confirmation; approval is permission, not
  completion.
<!-- /shared:tool-confirmation -->

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
