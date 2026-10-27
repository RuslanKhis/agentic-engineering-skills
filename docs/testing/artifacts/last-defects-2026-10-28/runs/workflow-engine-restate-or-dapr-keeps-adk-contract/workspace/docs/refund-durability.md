# Refund approvals that survive restarts: decision and test plan

Answers `docs/durability-request.md`. Status: application side implemented and unit-tested on
paper only (see "Evidence"); nothing has run, and the Restate wiring is unverified.

## Decision: Restate, around ADK rather than inside it

| | Restate | Dapr (already on GKE) |
| --- | --- | --- |
| ADK integration | `RestatePlugin` exists but cannot carry this app as is (below) | `diagrid` re-implements the agent loop: callbacks, `{user:tier}` templating, sub-agents and confirmation are dropped, so the token budget and the approval cannot be kept |
| Licence at 4,000 staff | Server BSL 1.1 with a grant for production use running your own services | `diagrid`'s modified BSL is free only under 60 staff and US$15M revenue: not usable here without a licence |
| Ops cost | A new stateful server to run | Already running |

Neither engine's ADK integration keeps this contract, so the plugin is not used. ADK keeps running
the chat turn exactly as before (`SequentialAgent`, both model callbacks, `max_llm_calls=8`,
`{user:tier}`); the engine owns only the part that has to outlive a pod, the wait and the payment.

Why not the Restate plugin (read and probed offline against google-adk 2.12.0, 2026-10-25, per the
workflow skill's runtime reference): it accepts only an `LlmAgent` root, so `SequentialAgent` fails;
it answers `before_model_callback` itself, which skips the budget callbacks and `max_llm_calls`;
and an approved ADK confirmation fails non-terminally and the effect never runs.

Why Restate and not native Dapr Workflow wrapping the unchanged ADK runner: it would work the same
way, but Restate's workflow-with-promise-and-timer model is the smaller fit, and its Python SDK was
already trialled by the payments team. Dapr remains a defensible choice if running a second engine
is the deciding cost; the application code here is engine-neutral except `app/workflows/` and
`app/clients/restate.py`.

## What changed

- `request_refund` (replaces `issue_refund` + `require_confirmation`) validates, stores a
  `refund_ops` row in state `pending`, asks the engine to start workflow `RefundReview/<op_id>`,
  and returns `pending_approval` with `payment_processed: false`. No ADK pause is left open, so a
  rescheduled pod no longer strands an approval ("session not found on this worker").
- `POST /backoffice/refunds/{op_id}/decision`: the manager is the verified IAP principal and must
  be in `REFUND_MANAGER_EMAILS`; they cannot approve their own refund. It is a conditional
  `pending -> approved|rejected` update; then it wakes the workflow.
- `app/workflows/refund_review.py`: waits on a promise or a timer (`REFUND_APPROVAL_DAYS`, default
  14), then runs `refund_ops.execute` as a journaled step with up to 6 attempts. `execute` pays
  from the stored payload with the stored key (`op_id`) and never from the wake-up.
- `GET /api/refunds/{op_id}`: status for the requester or a manager.
- States: `pending_approval, approved, rejected, expired, executing, completed, failed,
  outcome_unknown`. Rejected and expired operations let the customer ask again (new generation,
  new key).

## Questions I could not ask, and what I assumed

1. Who is a manager? Assumed an allowlist of IAP emails in `REFUND_MANAGER_EMAILS`, and that the
   back office uses the same IAP audience as the chat. If managers are a Google group, replace the
   check in `refund_ops.review`.
2. How long may an approval wait? Assumed 14 days, then `expired`. The payments provider
   de-duplicates keys for 7 days from the first send, which is why the keyed write happens only
   after approval and why retries are capped at 6 attempts.
3. Where do orders and refund operations live in production? The store is SQLite at
   `SUPPORT_DB_PATH`, and `deploy/gke/deployment.yaml` mounts no volume for 3 replicas. **A
   per-pod file loses `refund_ops` on reschedule and gives each replica a different view.**
   Assumed orders come from elsewhere; the operations table must be in the shared Cloud SQL
   PostgreSQL before this ships. Not done: the `Store` is still SQLite.
4. Is "repeat the same refund" the same request? Kept the existing rule (customer, order, amount).
5. Customer notification when the decision lands: not built (status endpoint only).

## Known gaps

- The chat turn itself (model calls) is not made durable: a crash mid-turn means the customer
  resends, as today. Only the approval wait and the payment survive.
- A wake-up while the operation is still pending (only via the ingress directly) ends the workflow
  with nothing paid; the operation then stays pending until a sweeper or a new request handles it.
  Keep the Restate ingress reachable only from the web service (NetworkPolicy); it has no caller
  authentication.
- No outbox, audit table or sweeper for operations whose workflow was never started.
- `deploy/gke` has no Restate server, worker deployment, env vars or NetworkPolicy yet.
- ADK `ResumabilityConfig` is left on; it no longer carries the approval.

## Before you trust it

Evidence so far: `offline`, `not run` (this session had no way to execute Python; the tests below
were written and traced by hand, not run). First step: `python -m unittest discover -s tests -t .`.

Application contract, `tests/test_refund_ops.py` (offline, fakes only):

- Submit pays nothing and starts one workflow; a repeat returns the same operation; invalid
  amount, foreign order or bad type creates nothing; a failed queueing is healed by a repeat.
- Non-manager, self-approval and unknown operation are refused with zero writes.
- Approval alone pays nothing; execute pays once with `Idempotency-Key == op_id`; duplicate
  approval and repeated execute leave one request and one refund row; a later conflicting decision
  does not overturn the first.
- Crash after the provider answered, before the row is saved: state stays `executing`, the re-run
  uses the same key, one refund row. 503 is retried; 402 is `failed`; exhausted retries are
  `outcome_unknown`, never `failed`.
- Expiry loses to an earlier approval; approval after expiry cannot revive.

Still to do, in this order, against a real Restate server in a non-production namespace and the
payments sandbox (each needs explicit approval first; none done):

1. Install `restate-sdk==1.1.0` in a scratch venv and import `app.workflows.refund_review`. The
   calls `ctx.run(..., max_attempts=)`, `restate.select`, `ctx.promise` and `restate.TerminalError`
   on exhaustion were written from memory of the 1.x API and may need adjusting.
2. Kill the worker pod while the workflow waits; decide after it returns: exactly one payment.
3. Kill the worker after the payment call returns and before the journal entry: one refund at the
   provider sandbox (same key), one `refunds` row.
4. Restart the Restate server and the web pods during a 2-day wait; the decision still pays once.
5. Approve with the timer a second from expiry; the outcome is exactly one of paid or expired.
6. Call the ingress wake-up directly with the operation pending: nothing is paid (known gap above).
7. A full chat through the served app with a scripted model: token budget still refuses at
   40,000, `max_llm_calls=8` still stops a loop, `{user:tier}` still renders, and the reply after
   `request_refund` says waiting for approval, not refunded (test the model request that receives
   the tool result, not only the scripted answer).
8. A second user's session cannot read or decide the first user's operation.
9. Load: one approval per refund at the support volume, many pending workflows sleeping for days;
   measure Restate server memory and storage at that count.
