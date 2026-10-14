---
goal: G08
title: Labelled evaluation set and runner
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-7
  review_and_verify: 1-2
  total: 6-9
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 Labelled evaluation set and runner

## Outcome

Gives the measured result the MVP needs: about 30 labelled conversations. Policy-edge labels compute their expected outcome from `app/policy.yaml`, so the W1 sign-off changes config, not labels.

## Scope

- In and out: In: `evals/cases/` covering book, move and cancel, ambiguous dates, two appointments on the same day, out-of-policy requests, unavailable slots, another customer's ID, "cancel everything", and instructions in notes; a runner over the fake API reporting tool calls and the proposed operation per case. Out: the final measured run (G09) and the CI gate (G12).
- Depth: Build. Labels are checked by a second person (Dev C, 1 h, inside review).

## Acceptance

- [ ] The runner executes the read-only cases on the G02 agent and writes a results table
- [ ] Every case states an expected tool sequence or operation and a forbidden effect
- [ ] The runner records a failed or missing result as a failure, never as a skip

Verification: Live model against the fake API, capped at 30 cases × 1 repeat.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
