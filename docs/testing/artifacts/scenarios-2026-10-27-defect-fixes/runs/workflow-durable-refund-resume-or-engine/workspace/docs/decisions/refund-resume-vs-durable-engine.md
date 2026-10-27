# Decision: keep ADK resume; make the refund write replay-safe (no durable engine yet)

## Why the 2026-10-21 double refund happened
Not because the wait was long. The paused session is a row in Postgres and survives days.
The refund was paid twice because the resumed tool ran twice and `PaymentsClient` sent a fresh
`uuid4()` as `Idempotency-Key` each time, so the provider's de-duplication never applied.
A durable engine would not fix that on its own: Temporal activities are at-least-once too and
need the same stable key.

## Decision
- Stay on ADK resumable approval for the multi-day wait.
- Derive the idempotency key from (user, order, amount, tool `function_call_id`), stable across
  replays; derive the local `refund_id` from it and skip the call if already recorded.
- Test: `tests/test_refund_resume.py` replays the incident (second approval; crash after the
  provider accepted) and asserts one provider refund and one local row.

## Revisit and move to a durable engine if
- the flow grows several side effects that must be ordered or compensated (refund + ledger +
  mail), or waits need timers/escalation/cancellation;
- the provider stops supporting idempotency keys;
- an approval may be answered after the provider's 7-day key window (the local row covers
  replays only after a successful record, not a crash in that gap).

## Assumptions (nobody to ask)
- ADK 2.12 re-runs the tool on resume with the same `tool_context.function_call_id`.
  **Not verified here** (no SDK, no network); verify against a real resume before relying on it.
- Back office can send a second approval for an invocation that already completed. Not
  blocked here; `app/approvals.py` should also reject answers for non-pending confirmations.
- Questions for the team: should the back office show "approved, processing" state; is the
  provider's 7-day window measured from first use of a key?
