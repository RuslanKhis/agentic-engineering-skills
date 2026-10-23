# Human review and truthful outcomes

Read for high-risk writes, payment-like actions, approval gates or uncertain retries. Outcome: the model can propose an operation while trusted application code controls permission and execution.

## Preserve the distinction between permission and completion

Return explicit states such as `invalid_request`, `pending_approval`, `approved`, `executing`, `completed`, `rejected`, `expired`, `failed` and `outcome_unknown`, adapting existing API names. An approval-only action must say no external operation was performed. In a refund demonstration, return `payment_processed: false` and pass that fact into the actual subsequent model request. Only verified execution evidence can justify “paid” or “refunded”.

Test both the actual tool result and the model request that receives it. A scripted final answer proves wiring, not model compliance; an approved, bounded live conversation tests selected model behaviour separately. Where false completion claims are unacceptable, render critical status deterministically from stored state instead of relying solely on generative wording.

Validate amounts before any approval/publication: positive, finite, correct currency/precision, not booleans or unsupported types. Use integer minor units or validated decimals as the application's currency policy requires. Bind order ownership, user and tenant outside the model schema; a model-supplied `user_id` is not authentication. Ask for missing business inputs before calling the tool.

## Decide local demonstration or durable operation

A signing or approval key for a development, in-memory store may be ephemeral and per-process when its lifetime matches the store's and the code says so; the production store names its key source (Secret Manager, KMS) and fails to start without it. A mock publisher demonstrates routing only. Fresh UUIDs on every request, in-memory lists, Pub/Sub delivery and instructions saying “do not repeat” do not create durable review or exactly-once effects. If production explicitly selects a transport/store, fail clearly when configuration is missing instead of silently falling back to a mock.

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

The native surfaces, read on https://adk.dev/tools-custom/confirmation/ and https://adk.dev/runtime/resume/ on 22 October 2026 (confirm against the installed ADK version; this skill's recorded baseline is 2.8.0 and Agents CLI scaffolds `google-adk>=2.12.0`):

- `FunctionTool(fn, require_confirmation=True)` asks before every call; `require_confirmation=` also takes a callable such as `async def needs_approval(amount: int, tool_context: ToolContext) -> bool`, so the threshold lives in code that sees the arguments (calling convention read in google-adk 2.12.0 `tools/function_tool.py`, `check_require_confirmation`: the callable is invoked with the tool's validated arguments as keyword arguments, plus `tool_context` when its signature names that parameter, sync or async; it runs inside `FunctionTool.run_async` on every attempt, after the agent's `before_tool_callback` chain and before the tool body, and a `tool_confirmation` that is present but not confirmed returns "This tool call is rejected." without running the body), not in the prompt.
- Inside a tool, `tool_context.request_confirmation(hint=..., payload=...)` pauses with a message and the structure the approver must return; the reply arrives as `tool_confirmation.payload`.
- The client answers with a `function_response` whose `id` equals the `function_call_id` of the `adk_request_confirmation` call, whose `name` is `adk_request_confirmation` and whose `response` holds `confirmed` and `payload`; with resumability it also carries the original `invocation_id`.
- Resumability is enabled on the app: `App(..., resumability_config=ResumabilityConfig(is_resumable=True))` (ADK Python from 1.16.0). The resume page warns that long-running functions "may run more than once when resuming a workflow", so the tool itself must check for and prevent a duplicate run; that is the operation record this reference already requires.
- `LongRunningFunctionTool(fn)` returns an initial result (for example an operation identifier with `status: "pending"`) and pauses the run until the client sends the final result under the same function-call identity. A built-in `request_input` tool lets the model itself ask the user and read the answer from `ctx.resume_inputs` (Agents CLI 1.11.0, `google-agents-cli-adk-code` skill, `references/adk-python.md`, read 22 October 2026; vendor guidance: `request_input` and `resume_inputs` were not found on the adk.dev resume page, so verify the symbols in the installed package).
- The confirmation page's known limitations still list `DatabaseSessionService` and `VertexAiSessionService` as unsupported; a persistent session store therefore needs the separate review service below, or a test proving the installed version resumes on that backend.
- ADK 2.12.0 (`CHANGELOG.md`, read 2026-10-22) runs a confirmed tool once per approval (bfdeb4a, closes #7434) and accepts `require_confirmation` on workflow nodes (`@node` and `FunctionNode`, 988fd1a), so a gate can sit on the node rather than inside a tool. Below 2.12.0 a re-sent approval could run the tool again; the duplicate-reply test below is the guard on every version, and the operation record stays required.
- For an ambient agent fed by a trigger, 2.12.0 exposes the trigger delivery id so a tool can detect a redelivery (74cd0ef, closes #7322). The tool still owns the idempotency check, keyed on that id: a redelivered trigger is a repeat of the same request, not a new one.

Whichever surface is used, the gate is code: the callable, the callback or the adapter decides, the hint only tells the approver what will happen, and the resume path is tested against the real session backend with a scripted model (approve, reject, duplicate reply, reply after expiry). When the approver sits in an AG-UI frontend, the answer arrives under one of two client contracts (a plain tool message, or a 1.0 interrupt outcome answered through `RunAgentInput.resume`, which the `ag-ui-adk` middleware enforces with `INTERRUPT_RESUME_REQUIRED` and `INTERRUPT_RESUME_INCOMPLETE` when its flag is on); `adk-frontend-integration` owns that choice and its tests, and the gate here decides the same way under both.

Three reference recipes in `google/adk-recipes` implement approval differently and are worth reading before designing a custom gate: `long-horizon-harness` (durable, mid-turn human-in-the-loop with per-user secrets), `ambient-expense-agent` (a graph `Workflow` that pauses for approval on high-value cases, with no chat loop) and `deep-search` (plan approval before an iterative loop) (Agents CLI 1.11.0, `google-agents-cli-adk-code` skill, `references/samples.md`, read 22 October 2026). When the project has `agents-cli-manifest.yaml`, consult the installed `google-agents-cli-adk-code` skill (`references/adk-python.md`, "Human-in-the-Loop", or one of those recipes); if it is not installed, adk-engineer explains how to get it. The recipe supplies wiring; the state table and crash table above remain the acceptance contract.



### Unanswered approvals and unreadable arguments

Two more rules close the gate from the sides. An approval left unanswered is rejected, not carried: when the next invocation on the session starts and a confirmation request from an earlier turn has no answer, the gate records a rejection for it and the tool does not run, because "a missing answer must never authorize tool execution"; an answer that arrives after that rejection cannot authorise the call and the caller starts a new request (microsoft/agent-framework commit 0200599, MIT, `docs/decisions/0045-dotnet-unanswered-tool-approvals.md`, status proposed, dated 2026-10-02, read 2026-10-23). And the approval rule itself fails closed on arguments it cannot read: when the `require_confirmation` callable or the gate receives arguments that are missing, empty, malformed or not an object, or carry non-standard constants such as `NaN` or infinities, the call requires manual review rather than being approved by a rule that could not inspect it (openai/openai-agents-python commit 841dfdd, MIT, `docs/guardrails.md`, `docs/human_in_the_loop.md`, `docs/testing.md`, read 2026-10-23; another framework's documented behaviour, restated as a rule for ADK). The ADK hook for the first rule is a `before_agent_callback` that classifies the new user content: a `function_response` named `adk_request_confirmation` is an answer to a pending request (2.12.0 reads confirmations from exactly those responses, `flows/llm_flows/tools/_confirmation.py`), anything else is a new message that closes every pending request as rejected before the model runs. Keep the pending record in session state under one top-level key and reassign the whole value on every change, because ADK records a state delta on assignment, not on in-place mutation of a nested object (the workflow skill's runtime reference).

### No human present

When no human is present (a scheduled routine, a background sub-agent, a trigger-fed ambient run), an approval request resolves as denied and is recorded; Google's long-horizon-harness recipe passes `ask_is_deny=True` to its policy guard on headless chains and runs routines in a disjoint sandbox scoped to their declared secrets, while a blocking sub-agent resurfaces its child's approval to the parent turn tagged `[delegated: <name>]`, one confirmation per tool call, a second different approval in the same run denied with guidance to split the task or pre-grant (google/adk-recipes be63596, `core/python/long-horizon-harness/docs/security-model.md`, read 2026-10-22; vendor sample). The ambient-expense-agent recipe shows the other half: the approval UI finds pending approvals by listing the user's sessions on the ADK server and answers the paused `RequestInput` from an IAP-protected frontend (same commit, `core/python/ambient-expense-agent/expense_agent/fast_api_app.py`, `README.md`).

Use a separate durable review operation when another person decides, decisions may take hours or days, or completion must survive process/client restarts. For the combined case, a persistent session store and a pause of days, the verdict is: the review record lives outside the session (this section), the run that resumes after the decision is either re-invoked by a caller with idempotent tools or driven by a durable-execution engine (`adk-workflow-design`'s runtime reference, "Resume and durable execution are different promises"), and the write behind the decision keeps its idempotency key either way (`safe-api-tool-calls`). The requester and the call identity a record needs come from the tool context without private attributes: `tool_context.user_id` (a property of the read-only context, 2.12.0) and `tool_context.function_call_id`. Historical ADK session-backend restrictions are version-sensitive; recheck official documentation rather than inheriting a compatibility claim from the chapter.

Acceptance tests: unauthorised/forged identity causes zero writes; another tenant cannot read an opaque review reference; invalid amounts cause zero publication; missing required inputs cause clarification and zero tool calls; pending retries return the same operation; changed-payload reuse conflicts; expiry/cancellation race safely with approval; the crash table's recovery assertions hold; final user-visible text reflects approval versus completion. Pair the clarification case with a complete request that creates one appropriate operation. Treat actual storage, reviewer transport and provider guarantees as unverified until those integrations are exercised.
