I chose Restate and wired it around ADK, not through its ADK plugin. Nothing has been run: this session had no way to execute Python. The new tests are traced by hand only, and the Restate workflow was never imported.

**Why Restate, and why not the plugin**
- **Dapr:** the `diagrid` ADK integration replaces ADK's agent loop. It drops callbacks, `{user:tier}` templating and confirmation, so the token budget and the approval couldn't stay. Its licence is also free only under 60 staff, and you have about 4,000.
- **Restate plugin:** it takes only an `LlmAgent` root, so your `SequentialAgent` fails. It also skips the budget callbacks and `max_llm_calls`, and approving an ADK confirmation fails. This comes from the skill's reference notes (probed offline on ADK 2.12), not from anything I ran.
- **Result:** the chat turn stays plain ADK, with both callbacks, `max_llm_calls=8` and `{user:tier}` untouched. Restate owns only the approval wait and the payment.

**What changed**
- **Tool:** `request_refund` replaces `issue_refund` and its confirmation. It saves a `refund_ops` row and starts a Restate workflow keyed by the operation id. It returns `pending_approval` with `payment_processed: false`. No ADK pause is left open, so a rescheduled pod no longer strands an approval.
- **Approval endpoint:** `POST /backoffice/refunds/{op_id}/decision` replaces the old ADK approval endpoint. The manager comes from the verified IAP principal and must be in `REFUND_MANAGER_EMAILS`. A manager can't approve their own refund. A second decision never overturns the first. The old endpoint trusted a `user_id` in the request body.
- **Status endpoint:** `GET /api/refunds/{op_id}` is new.
- **Workflow:** `app/workflows/refund_review.py` waits for the decision or a 14-day timer, then pays from the stored operation using the stored `op_id` as the idempotency key. Retries are capped at 6 attempts.
- **Other files:** `app/refund_ops.py` holds the logic, with store transitions in `app/store.py`. `app/clients/restate.py`, `app/wiring.py` and `app/settings.py` carry the Restate client and configuration. Tests are in `tests/test_refund_ops.py`. The rest of the decision write-up is in `docs/refund-durability.md`.
- **Pins:** `restate-sdk` is an optional extra only. No existing pin moved.

**Questions I couldn't ask, and what I assumed**
- Managers are an email allowlist, and the back office uses the same IAP audience as the chat.
- Approvals expire after 14 days.
- A repeat request with the same customer, order and amount is the same refund request (the existing rule).
- Rejected and expired requests can be asked again.

**Left undone**
- **Blocker:** the store is SQLite on a per-pod file, and the deployment mounts no volume for 3 replicas. `refund_ops` must move to the shared Cloud SQL Postgres before this ships, or it will lose operations on reschedule.
- **Restate API calls:** `ctx.run(..., max_attempts=)`, `restate.select` and `TerminalError` on retry exhaustion were written from memory of the 1.x API and may need adjusting.
- **Deploy:** there are no manifests for the Restate server, the worker, the env vars or a NetworkPolicy. The Restate ingress has no caller authentication, so it must be reachable only from the web service.
- **Gaps in the code:**
  - The chat turn itself isn't durable. A crash mid-turn means the customer resends, as today.
  - A direct wake-up on a pending operation ends the workflow with nothing paid.
  - There is no outbox, sweeper, audit table or customer notification.
- **Before you trust it:**
  1. Run `python -m unittest discover -s tests -t .`.
  2. Run the nine live checks in `docs/refund-durability.md` against a non-production Restate and the payments sandbox. They include killing the worker around the payment and restarting Restate during a multi-day wait. Each needs your approval first.