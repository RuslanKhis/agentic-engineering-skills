---
goal: G15
title: Personal data stays where the design says and can be erased
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G06, G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 28-42
  review_and_verify: 10-16
  total: 38-58
  calendar_waits: none
owner: Eng E
status: blocked
---

# G15 Personal data stays where the design says and can be erased

## Outcome

The data map made real: telemetry content gates off, logs with IDs only, screening on customer text failing closed, retention jobs and an erasure job with tombstones. Implements D9, I6, I7, I10.

## Scope

- In: screening callback (Model Armor or SDP per regional availability), retention and erasure jobs, sink inventory.
- Out: final retention values (O4, set after W2).
- Depth: build.

## Acceptance

- [ ] A full test conversation leaves no message text or image bytes in logs or traces
- [ ] Screening unavailable → the message is not sent to the model and the customer sees the defined message
- [ ] Erasure during a queued submission lets the claim complete, then removes local data; a late write is blocked by the tombstone

Verification: Offline plus staging log scan.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G15-sensitive-data.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
