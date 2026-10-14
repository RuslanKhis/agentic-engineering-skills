---
goal: G01
title: We know exactly how the booking API behaves on repeated and failed writes
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
mentions_only: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4.5-6
  review_and_verify: 1-2.5
  total: 5.5-8.5
  calendar_waits: none
owner: Dev C
status: ready
---

# G01 We know exactly how the booking API behaves on repeated and failed writes

## Outcome

Discovery and setup goal. Settles the open questions behind D4, D5 and D7
(design Q6, Q7) so the executor in G04 knows whether it may retry and how a
move works, and gives everyone a staging credential and repeatable test data.
Stops when A1–A6 are recorded; it does not build the executor.

## Scope

- In: reading the booking API's create, reschedule, cancel and availability
  handlers; bounded tests against **staging only**; re-checking the model ID;
  issuing the assistant's staging credential (the team owns the booking API);
  a staging seed script.
- Out: executor code (G04); any production call.
- Depth: discovery; floor kept: staging test customers only, no credentials in
  the contract note.

## Acceptance

- [ ] A1 `docs/architecture/booking-api-contract.md` answers: idempotency key support, its scope and retention; atomic reschedule endpoint (yes/no); slot hold or race behaviour on create; error codes for slot taken, validation, auth and rate limit; timeouts; the credential type the assistant will use; where the list of consultation-only services comes from; whether staging notifications can be routed to a test inbox; whether an audit log of writes is readable.
- [ ] A2 Staging replay test: the same create sent twice with the same key yields one appointment, or the note records that the API cannot dedupe and D4's reconcile-only path applies.
- [ ] A3 Model ID `gemini-3.8-flash` re-checked against the current Gemini/Vertex lifecycle pages with the date recorded, or the fallback `gemini-3.5-flash` chosen with the reason. (The ADK pin is fixed in design D11 and confirmed in G02/A10.)
- [ ] A4 D4 in the design updated with the move path (atomic reschedule, or book-then-cancel with `partial`) and the retry rule.
- [ ] A5 A staging read/write credential for the assistant exists in the team's secret store (never in the repo) and is shared with Dev A and Dev B.
- [ ] A6 `scripts/seed_staging.py` creates or resets two test customers with appointments relative to today (one inside 24 h, one next week), a fully booked day and one consultation-only service; running it twice gives the same state.

Verification: live against booking API staging, bounded to 30 write calls on
test customers; results pasted in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
