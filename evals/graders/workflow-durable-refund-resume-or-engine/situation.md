# workflow-durable-refund-resume-or-engine: what the fixture holds

Bases: support-assistant. The context is factual and shown unchanged.

## What is in the workspace

- `app/workflow.py`: resumable `App` with one LlmAgent; `FunctionTool(issue_refund,
  require_confirmation=True)`; sessions in Postgres via `DatabaseSessionService`
  (`app/approvals.py`).
- `app/approvals.py`: the back office resumes the paused invocation with the manager's
  `adk_request_confirmation` answer. Nothing records that an approved call already ran.
- `app/clients/payments.py`: the provider dedupes on Idempotency-Key for 7 days, but the client
  generates `uuid4()` per request, so a re-executed tool sends a new key and the provider pays
  again. The base `issue_refund` (unchanged) also has no operation record.
- `docs/incidents/2026-10-21-double-refund.md`: approval Friday -> Monday; provider accepted
  re_8812; pod evicted before the resumed invocation finished; second approval re-ran the tool;
  re_8840 paid. Postgres available, no Temporal cluster.
- `pyproject.toml` adds pinned sqlalchemy and asyncpg. Unit tests pass offline; google-adk is not
  installed.

## Assertion map

- A1: ADK resume is at-least-once for tools, needs a caller to re-invoke, unsupported from web UI
  and CLI; a days-long wait points at an engine; Temporal vs DBOS compared on what exists
  (Postgres favours DBOS; Temporal's MCP toolset pins mcp 1.x; secrets out of Temporal history).
- A2: idempotency key and reconciliation inside the durable step (a stable key, not uuid4 per
  request).
- A3: kill-after-the-write tests in both positions plus a negative control on plain resume;
  engine replay test written and reported not run without the SDKs.
- A4: engine version pinned; decision recorded in the design with evidence; approval gate in code.
