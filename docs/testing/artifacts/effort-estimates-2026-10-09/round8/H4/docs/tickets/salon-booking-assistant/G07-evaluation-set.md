---
goal: G07
title: We know how often the assistant does the right thing, including when misused
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 8-11
  review_and_verify: 2-3
  total: 10-14
  calendar_waits: none
owner: Dev A
status: blocked
---

# G07 We know how often the assistant does the right thing, including when misused

## Outcome

About 30 labelled conversations with expected tool trajectories and a runner, giving the first measured quality on the pinned model.

## Scope

- In: Cases: book, move, cancel, ambiguous dates ("next Friday"), slot unavailable, a policy refusal, out of scope, the salon phone; adversarial cases: another customer's appointment ID, "skip the confirmation", instructions planted in a message. Write-path cases target the tool names frozen in G01 and run once G04 lands. Runner, results file and a one-page summary.
- Out: CI gate (G11); production cases (G15).
- Depth: Build at MVP depth; the evaluation run is manual, not in CI.

## Acceptance

- [ ] Every case has an expected trajectory and a pass or fail; missing runs are reported as missing
- [ ] The adversarial cases assert that no operation is created and no write happens
- [ ] The summary records model ID, prompt version and date

Verification: bounded live run on the pinned model against the fake (paid calls; cap the runs in the summary).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
