# workflow-engine-restate-or-dapr-keeps-adk-contract: what the fixture holds

Bases: support-assistant. The context is factual and shown unchanged.

## What is in the workspace

- `app/agent.py`: `App(name="refunds", root_agent=SequentialAgent(intake LlmAgent, refund
  LlmAgent), resumability_config=ResumabilityConfig(is_resumable=True))`; `RUN_CONFIG =
  RunConfig(max_llm_calls=8)`; both agents carry `before_model_callback` / `after_model_callback`
  from `app/budget.py` (40,000-token budget in `temp:` state); the refund tool is
  `FunctionTool(issue_refund, require_confirmation=True)`.
- `app/prompts.py`: both instructions template `{user:tier}`; the refund step reads `{intake}`.
- `app/tools/refunds.py` + `app/clients/payments.py`: a deterministic Idempotency-Key per
  customer/order/amount sent to the provider (7-day dedupe). The key is computed inside the tool
  body, i.e. outside any durable step today.
- `app/server.py`: manager approval resumes via an `adk_request_confirmation` function response
  posted from `/backoffice/approvals` (any authenticated caller; no review record).
- `deploy/gke/`: Dapr 1.15 annotations and a `state.postgresql` statestore (actorStateStore true).
- `docs/durability-request.md`: approvals take days, pods are rescheduled, ops prefer Restate or
  the existing Dapr over Temporal, ~4,000 staff, budget and 8-call limit must stay.
- `tests/test_budget.py`: callback unit tests with duck-typed contexts (pass offline).

## Assertion map

- A1: RestatePlugin journals model calls only; tool bodies need run_typed; a SequentialAgent root
  fails terminally, so the root becomes an LlmAgent or Workflow graph.
- A2: the plugin short-circuits model callbacks: budget callbacks and max_llm_calls stop running;
  guards move before the plugin or into the tool path, with a test counting their firings.
- A3: confirmation replaced by a code-enforced authenticated review record; an exclusive Virtual
  Object key queues other calls during the wait.
- A4: the Dapr diagrid runner re-implements the loop, dropping callbacks, templating, sub-agents
  and confirmation; its BSL size gate (4,000 staff) needs an owner licence decision.
- A5: the idempotency key moves inside the durable step; engine and server versions pinned.
