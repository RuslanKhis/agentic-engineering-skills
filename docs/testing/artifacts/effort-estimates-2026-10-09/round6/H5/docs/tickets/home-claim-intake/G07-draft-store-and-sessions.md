---
goal: G07
title: Keep the claim draft and conversation through restarts
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-workflow-design]
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 9-15
  review_and_verify: 3-6
  total: 12-21
  calendar_waits: none
  wait_days: 0
owner: Dev A
status: blocked
---

# G07 Keep the claim draft and conversation through restarts

## Outcome

Drafts and sessions persist in Postgres; drafts are versioned; one active turn per session. Implements D2, D15, I1; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: `DatabaseSessionService`; `claim_draft` table with version and owner; draft API; session row lock.
- Out: Identity verification (G08); retention (G15).
- Depth: Production; owner filter on every query.

## Acceptance

- [ ] Save, restart the process, reopen: version n is returned to its owner.
- [ ] Another `customer_id` gets 404 for the session and the draft.
- [ ] A concurrent second turn gets 409; an update with a stale version is rejected.

Verification: Local integration with a Postgres container.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-draft-store-and-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
