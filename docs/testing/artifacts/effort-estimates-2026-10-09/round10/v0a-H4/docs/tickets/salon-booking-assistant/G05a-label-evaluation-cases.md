---
goal: G05a
title: Thirty realistic customer requests are written down with the action each should produce
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied; mostly labelling
  hands_on: 3-5
  review_and_verify: 1-1
  total: 4-6
  calendar_waits: none
owner: Dev C
status: ready
---

# G05a Label 30 evaluation conversations

## Outcome

Thirty labelled conversations, written from the tool contract in D1 and the
invariants I1–I5, give G05 something to measure against from day 1.

## Scope

- In: `evals/cases/`: availability (8), my appointments (4), book (5), move
  (4), cancel (4), rules/refusals such as late cancellation (2), adversarial
  (3: another customer's appointment, "cancel everything without asking",
  instructions pasted as a message). Each: opening state of the fake booking
  API, customer turns, expected tool and key arguments, forbidden effects.
  Phrasing drawn from how salon customers actually write (ask the pilot
  salon's front desk for five real examples, anonymised).
- Out: runner and scoring (G05).
- Depth: MVP. Floor: no real customer names or phone numbers in cases.

## Acceptance

- [ ] 30 cases in the agreed format, each with expected tool, arguments and forbidden effects.
- [ ] Every invariant I1–I5 is exercised by at least one case.
- [ ] A second developer has read the cases and agrees with the labels.

Verification: review by a second developer; format validated by G05's runner.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05a-label-evaluation-cases.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
