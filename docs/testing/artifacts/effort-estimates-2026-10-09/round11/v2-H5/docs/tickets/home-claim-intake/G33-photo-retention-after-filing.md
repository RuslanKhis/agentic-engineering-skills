---
goal: G33
title: Photos already sent to ClaimCenter are removed from our storage on time and on request
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-memory-architecture]
blocked_by: [G09, G12]
phase: 1
profile: production
estimate:
  hands_on: 7-9
  review_and_verify: 2-3
  total: 9-12
  calendar_waits: none
owner: Eng E
status: proposed
---

# G33 Photos already sent to ClaimCenter are removed from our storage on time and on request

## Outcome

Retention and erasure for filed claims, using G09's per-photo transfer
states and G08's operation states, so deletion never races the worker.
Implements the filed-claim part of D9. Handoff: 1 h from Eng B on transfer
states.

## Scope

- In: retention job for originals after confirmed transfer, erasure path
  for customers with filed or pending claims, operation payload deletion.
- Out: data held in ClaimCenter (insurer retention, outside this service).
- Depth: production.

## Acceptance

- [ ] A1 Originals are deleted 30 days after their `attached` state; photos still `rejected` or retrying are kept until the operation is terminal plus 30 days; the job is read back from staging.
- [ ] A2 An erasure request during a pending submission waits until the operation is terminal, then erases; a late or repeated worker step cannot recreate deleted photos; a second erasure request is a no-op.
- [ ] A3 Erasure after filing deletes sessions, drafts, photos and operation payloads, keeping only operation IDs and claim numbers; an absence query confirms it and touches no other customer.
- [ ] A4 An erasure job that crashes or whose delete times out resumes and completes; the absence query runs again after completion.
- [ ] A5 The erasure section of the on-call runbook is written and walked through once.

Verification: offline with the G01 fake and a storage fake; authorised
staging readback for A1.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G33-photo-retention-after-filing.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
