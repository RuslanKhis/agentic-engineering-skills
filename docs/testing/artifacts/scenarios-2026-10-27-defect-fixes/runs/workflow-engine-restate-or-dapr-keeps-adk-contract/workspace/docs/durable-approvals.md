# Durable refund approvals (Dapr Workflow)

Answers `docs/durability-request.md`. Status: implemented and unit-tested against doubles; **not yet
run on Dapr** (no network or cluster in the authoring session). Do not trust it in production until the
checks under "Before you trust it" pass.

## Decision

Dapr Workflow, using the Dapr 1.15 already on the cluster and its Postgres actor state store. The ADK
agent is unchanged: `SequentialAgent`, `{user:tier}` templating, the budget callbacks and
`RUN_CONFIG(max_llm_calls=8)` all stay. Only the pause moved out of ADK.

- Chat turn: the refund agent calls `request_refund`, which validates and submits, then the turn ends.
- Workflow `refund_approval` (instance id = payments idempotency key): waits for a manager decision or
  a 14-day timer, then runs the payment activity. State lives in Dapr, not in a pod or ADK session.
- Back office: `GET /backoffice/approvals/{operation_id}` (request and digest), `POST /backoffice/approvals`
  `{operation_id, approved, digest}`. The reviewer is the verified principal and must be in
  `REFUND_APPROVER_EMAILS`.

### Why not the others

- **Restate** (ADK plugin): root must be an `LlmAgent` (our `SequentialAgent` fails); the plugin
  skips agent and plugin model callbacks and `max_llm_calls`, which would disable our budget; ADK
  confirmation approval fails on resume. It would need the same submit-and-wait redesign plus a new
  server to run and a re-architecture of the agent. Source: this repo's `adk-workflow-design` skill,
  `references/runtime.md` (probed offline on 2.12.0, not re-probed here).
- **Dapr via `diagrid`**: re-implements the agent loop and drops callbacks, templating and
  confirmation; its licence free tier is under 60 staff, we have about 4,000.

### What this does not make durable

A worker crash mid-chat-turn still loses that HTTP request; the customer resends and the session
(Postgres) carries on. Model calls are not journaled. The long wait and the money write are the durable
parts, which is what the request needs.

## Assumptions (questions nobody could answer in the session)

1. Who is a manager? Assumed: the verified IAP email is in `REFUND_APPROVER_EMAILS` (comma list). Ask
   Sam Okoye whether a Google group is wanted instead.
2. Approval lifetime? Assumed 14 days (`REFUND_APPROVAL_TTL_DAYS`), then `expired`.
3. A manager cannot approve their own customer-side request (reviewer id == requester id).
4. A repeat of an identical request (same customer, order, amount) maps to the same operation; if it
   already ended declined/expired the tool tells the customer a colleague must review.
5. The back-office UI changes contract: it needs `operation_id` and `digest`, and a way to list
   pending operations, which is not built.

## Before you trust it

Offline (run in CI, `python -m unittest discover -s tests -t .`): decision checks, workflow paths,
crash after provider accepted gives one effect, activity re-run records once, terminal vs retryable
provider errors. These use a scripted context, so they do not prove Dapr behaviour.

Needs a Dapr 1.15 test cluster and a payments sandbox (not run):

1. Install `dapr-ext-workflow` matching the sidecar (pin it in `pyproject.toml` at that point) and
   confirm `app/dapr_runtime.py` imports and registers; its API calls were written from memory of the
   SDK, unverified.
2. Kill a pod while a request waits; approve from the back office through another pod; the refund
   happens once. This is the 2026-10-14 incident.
3. Kill the pod running the payment activity after the sandbox accepted the write; one refund at the
   provider, one row in the store.
4. Wait past the timer with a short TTL: status becomes `expired`, no payment. After an approval the
   instance completes promptly (the unfired 14-day timer must not hold it open).
5. Approve twice, approve after expiry, approve as the requester, approve with a stale digest, approve as
   a non-approver: each is refused or ignored with no payment.
6. Deploy a workflow code change while an instance waits: it must replay (Dapr requires deterministic,
   versioned orchestrators). Keep `refund_approval_workflow` unchanged in shape or add a new name.
7. Scheduler service and actor state store (`actorStateStore: "true"`, already set) healthy on the
   cluster; confirm retention of completed workflow history and that no secrets are in workflow input.
8. `SUPPORT_DB_PATH` defaults to a local SQLite file. If pods each have their own file, the payment
   activity can run on a pod that does not see the order. Orders and refunds must be in shared storage
   before this is trusted.
9. The 14 Oct "session not found on this worker" failure was not reproduced; the new path does not use
   an ADK session for approval, but confirm the chat path itself does not depend on a pod-local session.
