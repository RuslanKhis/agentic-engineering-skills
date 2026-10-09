---
goal: G01
title: Booking API contract and sign-in facts
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Booking API contract and sign-in facts

## Outcome

The team knows exactly what the booking API and website sign-in offer, so D3, D4 and D5 stop being provisional and G04 is either needed or dropped. Implements assumed answers A5, A7; decisions D3, D4, D5.

## Scope

- In: Read-only inspection of the booking API repository (OpenAPI/routes, auth, errors, idempotency, reschedule, business rules, notifications, staging URL) and the website's customer sign-in (token format, verification method). Write `docs/architecture/booking-api-contract.md` and last month's self-service vs front-desk change counts as the baseline.
- Out: Code changes (G03, G04), fake API updates beyond matching the contract.
- Depth: Discovery only. No secrets in the contract file; staging URL only.

## Acceptance

- [ ] The contract file answers: endpoints, auth, error codes, idempotency-key support, atomic reschedule, server-side rules, notifications, staging target, site token verification
- [ ] Each question not answerable is listed as missing with who can answer it
- [ ] No production call and no credential value appears in the repository

Verification: Review by Dev B and Dev C (30 min); decision lines recorded in the plan's open decisions (offline).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
