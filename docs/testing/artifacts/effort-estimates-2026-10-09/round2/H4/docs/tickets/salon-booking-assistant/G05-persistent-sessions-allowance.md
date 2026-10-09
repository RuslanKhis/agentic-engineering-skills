---
goal: G05
title: Conversations survive restarts; per-customer turn allowance
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-operational-guardrails]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 2–3.5
  review_and_verify: 2.5–4
  total: 4.5–7.5
  calendar_waits: none
owner: Dev C
status: blocked
---

# G05 Conversations survive restarts; per-customer turn allowance

## Outcome

a customer's chat continues after an instance restart, and nobody can run up model spend. D6, D7; I5.

## Scope

- In: `DatabaseSessionService` on Postgres; proposals and allowance tables (migrations); `app/admission.py` with 50 turns/customer/salon-local day checked before the Runner; daily deletion of sessions older than 30 days. Out: erasure on request (G13).
- Route: local Postgres container for tests; Cloud SQL in G08.
- Prerequisites: G02.
- Depth: MVP; DB URL from environment/Secret Manager. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-operational-guardrails` (allowance admission and exhaustion message)

## Acceptance

- [ ] restart the gateway process mid-conversation → next turn keeps context
- [ ] 51st turn rejected with zero model calls
- [ ] two concurrent turns do not exceed the allowance
- [ ] proposals survive restart and remain confirmable

Verification: local integration with a Postgres container (Docker needed); offline unit tests for admission. Execution scope: local only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-persistent-sessions-allowance.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
