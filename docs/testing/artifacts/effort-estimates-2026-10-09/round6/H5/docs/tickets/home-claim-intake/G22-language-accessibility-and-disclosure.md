---
goal: G22
title: Use the agent in either language, accessibly, knowing it is AI
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-agent-instructions]
blocked_by: [G14]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-21
  review_and_verify: 3-6
  total: 15-27
  calendar_waits: translation vendor turnaround
  wait_days: 5-10
owner: Dev C
status: blocked
---

# G22 Use the agent in either language, accessibly, knowing it is AI

## Outcome

Both GA languages, WCAG 2.1 AA, the AI notice and the handoff view are in place. Implements D9; Q6, Q17; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: UI strings, language-aware instruction, AI notice from G04, handoff view with phone and draft reference.
- Out: Second market (phase 2).
- Depth: Production.

## Acceptance

- [ ] The agent answers in the customer's language on the eval language subset.
- [ ] AI notice shown before the first message.
- [ ] Automated and manual WCAG 2.1 AA checks pass; handoff shows phone and draft reference.

Verification: Local browser tests plus manual accessibility review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G22-language-accessibility-and-disclosure.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
