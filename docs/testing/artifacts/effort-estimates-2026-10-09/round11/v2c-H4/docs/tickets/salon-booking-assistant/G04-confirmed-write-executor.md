---
goal: G04
title: A confirmed booking, move or cancellation reaches the booking API exactly once
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-tool-auth-and-secrets]
blocked_by: [G01]
mentions_only: [G02, G06, G07, wait]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 6-9
  total: 12-18
  calendar_waits: none
owner: Dev C
status: blocked
---

# G04 A confirmed booking, move or cancellation reaches the booking API exactly once

## Outcome

When Priya presses Confirm, plain code rechecks the proposal and the rules,
claims an operation record and performs the write once, reporting the
authoritative outcome or an honest "uncertain". Implements D2 (execute side),
D4, D5 (rule checks). Built against the D5 proposal schema with fixture
proposals; the real propose tools from G02 and the widget from G06 meet it in G08.

## Scope

- In: `executor.confirm(proposal_id, customer_id)`; `operations` table and
  status machine; booking API write client (create, reschedule or
  book-then-cancel, cancel) using G01's contract; business rules (cutoff,
  horizon, consultation-only list) read from configuration with the D5 values
  as defaults; the staging credential from G01/A5 in a local environment
  variable (Secret Manager is wired in G07); reconciliation helper that
  lists the customer's appointments; structured `operation_status` log events.
- Out: HTTP route and widget (G06, wired in G08), staff screen (later).
- Depth: MVP build with careful, adversarial review (writes to real bookings).

## Acceptance

- [ ] A1 Confirming a booking proposal creates one appointment in the fake (and once on staging); operation `succeeded` with the provider ID; the returned details come from the API response.
- [ ] A2 Two concurrent confirms or a double click on the same proposal → exactly one provider write; the second call returns the same operation; a duplicate `proposal_id` insert is refused by the unique constraint.
- [ ] A3 Proposal expired (over 10 minutes), slot no longer free, or appointment changed/cancelled since the proposal → status `stale`, no write, message offers a new search.
- [ ] A4 A proposal owned by another customer → 404, no provider call.
- [ ] A5 Provider timeout after the request was sent, or a success response missing the booking ID → status `uncertain`; no blind retry unless G01 proved key dedupe; reconciliation by listing appointments resolves it in the test; message "we're checking, please don't book again"; `operation_status=uncertain` logged.
- [ ] A6 Move: if book-then-cancel, new booking succeeds and cancel fails → status `partial`, message says both appointments exist and the team will remove the old one, alert event logged; if atomic reschedule, a failed reschedule leaves the old appointment intact (fake asserts it).
- [ ] A7 Move or cancel inside 24 hours, a date beyond 60 days, or a consultation-only service → refused in code with the salon phone number; no provider call.
- [ ] A8 Booking API rejects the write (4xx validation, 409 slot taken) → status `failed` or `stale` respectively, actionable message, no retry.
- [ ] A9 Connection refused, 5xx before acknowledgement, or 429 → at most 2 retries only where G01 marks the request replay-safe, honouring `Retry-After`; otherwise `failed` with an honest message.
- [ ] A10 Booking API returns 401/403 for our credential → status `failed`, `auth_failed` logged, no retry; the credential never appears in logs or results.
- [ ] A11 Operation-record write fails before dispatch → no provider call; local write fails after provider success → retried once, then the operation is logged as `uncertain` for reconciliation.
- [ ] A12 The database connection drops while committing the claim (commit outcome unknown) → the executor re-reads the row by `proposal_id` before any dispatch; it dispatches only if it finds its own claim, otherwise it returns the existing operation.

Verification: offline `pytest tests/executor/` with a fake booking API that
injects each failure; A1, A2 and A5 repeated once on booking API staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirmed-write-executor.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
