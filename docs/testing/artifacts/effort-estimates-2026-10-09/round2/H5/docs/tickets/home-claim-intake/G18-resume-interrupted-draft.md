---
goal: G18
title: A customer who leaves can resume their draft within 7 days
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-frontend-integration]
blocked_by: [G06, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 22–38
  review_and_verify: 10–18
  total: 32–56
  calendar_waits: none
owner: E2
status: blocked
---

# G18 A customer who leaves can resume their draft within 7 days

## Outcome

A customer who uploads photos later (common after water damage) returns to the same draft and session; abandoned drafts expire per A10.

## Scope

- In: Draft listing for the owner; session resume; expiry; UI entry point.
- Out: Long-term memory across claims (later).
- Depth: Minimal: sessions plus draft, no memory service.
- Route: Owner-scoped draft query; `DatabaseSessionService` resume by session ID owned by the customer.
- Supporting skills: `adk-frontend-integration` ('continue your claim' entry point in the portal)
- Execution scope: Local and dev.

## Acceptance

- [ ] Resume after a restart returns the draft with its photos
- [ ] Another customer cannot list or resume it
- [ ] A draft older than 7 days is offered as 'start again' and is deleted at 30 days

Verification: Offline and local integration tests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-resume-interrupted-draft.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
