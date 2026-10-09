---
goal: G10
title: Run the evaluation set and tune to the launch bar
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02, G03, G06]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-4
  review_and_verify: 1-1
  total: 3-5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G10 Run the evaluation set and tune to the launch bar

## Outcome

Measured evidence that the pinned model and `booking_v1` propose the right change and never write without Confirm. This is the I5 gate for G11.

## Scope

- In:
  - A runner over G06's cases: live model, fake API, three repeats, recording cost.
  - A result table in `eval/results/latest.md`.
  - At most two instruction revisions, `booking_v1` then `booking_v2`, each re-run on the full set.
- Out: The CI gate (G13).
- Depth: MVP: an evaluation set run by hand before each release.
- Implementation route: A pytest runner or the ADK evaluation command on the pin. Proposal fields are compared exactly. Forbidden writes are counted from the fake's call log, not from model text.
- Prerequisites: G02, G03 and G06.
- Supporting skills: Adk-agent-instructions, for the instruction revision.
- Execution scope: Dev Vertex AI project.

## Acceptance

- [ ] The full set runs with recorded cost.
- [ ] The launch bar (O6, assumed) is met: at least 27 of 30 cases correct on 2 of 3 repeats, and 0 forbidden writes on any repeat.
- [ ] If the bar is not met after two revisions, the failures are recorded and G11 stays blocked.

Verification: Live model against the fake API in the dev project, spend within the dev budget.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-run-the-evaluation-set-and-tune-to-the-launch-bar.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
