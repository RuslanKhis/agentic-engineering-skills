I picked Dapr Workflow and wired it in, but none of it has been run. This session had no way to execute commands, so the unit tests are written but unrun. I also couldn't install or import `dapr-ext-workflow`, so `app/dapr_runtime.py` was written from memory of the SDK and is unverified.

## Why Dapr

Dapr Workflow keeps the ADK agent as it is. Restate and Dapr through `diagrid` would each have broken something you need:
- **Restate:** its ADK plugin only accepts an `LlmAgent` root, so your `SequentialAgent` fails. It also skips the model callbacks and `max_llm_calls`, which would disable the token budget and the 8-call limit. I took this from the `adk-workflow-design` skill's notes; I didn't re-test it.
- **Dapr through `diagrid`:** it re-implements the agent loop and loses callbacks, `{user:tier}` templating and confirmation. Its free production licence is also limited to organisations under 60 staff, and you have about 4,000.

## What I changed

- **`app/tools/refunds.py`:** `issue_refund` is replaced by `request_refund`, which validates and submits, then ends the turn. The `require_confirmation` wrapper in `app/agent.py` is gone, and the refund instruction in `app/prompts.py` now names the new tool.
- **`app/approvals.py`:** the approval workflow waits for a manager's decision or a 14-day expiry, then runs the payment. The payment re-checks the order and limits first and uses the idempotency key. A temporary provider failure is retried; a permanent rejection is reported.
- **`app/dapr_runtime.py`:** the only file that imports `dapr`.
- **`app/server.py`:** the back-office endpoints are `GET /backoffice/approvals/{operation_id}` and `POST /backoffice/approvals`.
- **Approval rules:** the reviewer comes from the verified principal and must be in `REFUND_APPROVER_EMAILS`. This fixes the old endpoint, which took `user_id` from the request body and let any signed-in staff member approve. A manager can't approve their own customer's request, and a stale decision is ignored.
- **Smaller edits:** `PaymentsError` now carries the status code, and `record_refund` is safe to replay. Refund ids are derived from the idempotency key.
- **Files and tests:** `docs/durable-approvals.md` has the decision, assumptions and the pre-trust checklist. New and updated tests are in `tests/test_approvals.py`, `tests/test_tools.py` and `tests/fakes.py`.

## Assumptions (nobody to ask)

- **Who counts as a manager:** anyone whose IAP email is in `REFUND_APPROVER_EMAILS`. Whether you want a Google group instead is a question for Sam Okoye.
- **Approval lifetime:** 14 days, then the request expires.
- **Repeat requests:** an identical request (same customer, order, amount) maps to the same operation. If that one already ended declined or expired, the customer is told a colleague must review it.

## What to test before you trust it

The full list is in `docs/durable-approvals.md`. The essentials, on a Dapr 1.15 test cluster with a payments sandbox:
1. Install `dapr-ext-workflow` matching the sidecar, pin it, and confirm `app/dapr_runtime.py` imports and registers.
2. Kill a pod while a request waits, then approve through another pod. The refund should happen once. This is the 14 Oct incident.
3. Kill the pod running the payment after the sandbox accepted it. You should see one refund at the provider and one row in the store.
4. Use a short expiry and confirm no payment is made. After an approval, confirm the workflow finishes promptly rather than waiting on the unfired timer.
5. Try approving twice, after expiry, as the requester, with a stale digest and as a non-approver. None should pay.
6. Change the workflow code while an instance is waiting and confirm it still replays.

## Left undone

- **Dapr itself:** the workflow, timers, events and replay have never run. The unit tests use a scripted stand-in for the Dapr workflow context, so they don't prove Dapr's behaviour.
- **Server tests:** there are none for `app/server.py`.
- **Back office:** there is no list of pending operations, and the back-office UI must change to send `operation_id` and `digest`.
- **Customer notification:** the customer isn't told the outcome after approval.
- **Pinning and deployment:** the dependency isn't pinned in `pyproject.toml`, and `REFUND_APPROVER_EMAILS` isn't set in the deployment.
- **Pod-local storage:** `SUPPORT_DB_PATH` defaults to a local SQLite file. If each pod has its own, the payment can run on a pod that doesn't see the order. Fix this before trusting anything here.
- **14 Oct failure:** I didn't reproduce the "session not found on this worker" error. Approval no longer uses an ADK session, but a crash mid-chat-turn still loses that request, and the customer has to resend.