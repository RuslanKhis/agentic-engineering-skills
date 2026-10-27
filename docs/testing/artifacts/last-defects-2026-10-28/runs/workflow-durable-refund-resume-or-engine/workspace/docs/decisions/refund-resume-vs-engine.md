# Decision: ADK resume with a stable idempotency key, not a durable engine (yet)

Status: proposed. Context: docs/incidents/2026-10-21-double-refund.md.

## Cause of the incident

Not ADK resume. `PaymentsClient.create_refund` sent `Idempotency-Key: uuid4()` on every call, so
the provider could not recognise the replayed call. ADK documents resume as at-least-once for
tools; a tool body re-running after an eviction (or a second approval) is expected behaviour.
The provider already de-duplicates on the key for 7 days. A durable engine would not have fixed
this on its own: every engine checkpoints a step's result, and a crash between the provider
accepting the write and the checkpoint re-runs the step, so the key is still required.

## Decision

1. Derive the key from the operation's identity: sha256(user_id | function_call_id | order_id |
   amount_cents). `function_call_id` is the same across resume and across a second approval of
   the same paused call. The local refund id derives from the same digest and the insert is
   `OR IGNORE`, so a replay writes one row.
2. Keep `ResumabilityConfig` and Postgres `DatabaseSessionService`. A wait of days is a stored
   session, not a held process; nothing in the incident came from the wait length.
3. Revisit a durable engine (DBOS first: Postgres only; Temporal when a cluster exists) if any of
   these become true: nothing can re-invoke after a crash (today the back office is the
   caller and a second click did re-invoke), waits need timers/escalation/expiry, or more
   side-effecting steps follow the refund (mail, ledger) that need saga-style compensation.

## Proof

`tests/test_refund_resume.py` replays the tool body after a simulated crash following provider
acceptance, against a provider double that de-duplicates on `Idempotency-Key`. It asserts two
provider requests, one provider refund and one local row. It fails against the old uuid4 key.

## Not covered (follow-ups)

- Back office showed "pending" after the first approval was applied; it should record the
  decision durably and refuse a second answer for the same `function_call_id` (app/approvals.py).
- Provider rejection of a reused key with a changed body is not modelled.
- Key retention is 7 days; an approval later than that after the first attempt could pay again.
- The test uses `FakeToolContext`; that real ADK `ToolContext.function_call_id` is identical on
  resume is documented behaviour but not verified here (SDK not installed, no network).
