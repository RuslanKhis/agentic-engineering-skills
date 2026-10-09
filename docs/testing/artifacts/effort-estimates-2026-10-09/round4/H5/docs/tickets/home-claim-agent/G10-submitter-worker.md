---
goal: G10
title: A confirmed claim reaches Guidewire exactly once, even through crashes and timeouts
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 32-56
  review_and_verify: 12-20
  total: 44-76
  calendar_waits: none
  wait_days: 0
owner: Eng B
status: proposed
---

# G10 A confirmed claim reaches Guidewire exactly once, even through crashes and timeouts

## Outcome

Implements I2 and I4: the worker and Guidewire client that turn an operation into a claim number, with replay or lookup following G01.

## Scope

- In: `app/submission/worker.py`, `app/guidewire/` client and fake; leased state machine `pending → dispatched → created → documents → filed | uncertain | rejected`; per-photo sub-operations; payload escaping; secret only via `submitter-sa`.
- Out: Production client (G23); reconciliation runbook (G26).
- Depth: Production depth. Floor: no fresh create without the replay/lookup check.

## Acceptance

- [ ] Crash after Guidewire commit: one claim, operation ends `filed` after retry
- [ ] Lost response: lookup, no second create
- [ ] Partial document failure: claim kept, photos retried; a stale lease cannot record
- [ ] One end-to-end sandbox filing returns a claim number; HTML in the description is escaped

Verification: Offline against the fake Guidewire; one bounded sandbox filing.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G10-submitter-worker.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
