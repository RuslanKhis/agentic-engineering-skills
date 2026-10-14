---
goal: G11
title: Pressing Submit files the claim and shows its number
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-agent-security]
blocked_by: [G06, G07, G08, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 28-42
  review_and_verify: 12-18
  total: 40-60
  calendar_waits: none
owner: Eng A
status: blocked
---

# G11 Pressing Submit files the claim and shows its number

## Outcome

The summary render with version hash, the submit route that inserts the operation and enqueues a named Cloud Task, and the status route reading receipts. Implements D5, I2, I3.

## Scope

- In: `app/api/submit.py`, `/status`, summary rendering from the draft (not model text), Cloud Tasks enqueue, forbidden-submit adversarial cases.
- Out: UI (G12).
- Depth: build; submission is unreachable from any model.

## Acceptance

- [ ] Submit with the current hash returns an operation and status later shows the claim number
- [ ] A stale hash returns 409; a double click returns the same operation
- [ ] A scripted model asked to "submit" produces no operation row and no Guidewire call

Verification: Offline plus local integration with Postgres and a fake task queue.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G11-confirm-and-submit.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
