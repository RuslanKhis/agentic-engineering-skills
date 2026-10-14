---
goal: G10
title: The whole journey works on staging for all five salons
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation]
blocked_by: [G03, G05, G06, G07, G08, G09]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2-3
  review_and_verify: 0.5-1
  total: 2.5-4
  calendar_waits: none
owner: Dev C
status: ready
---

# G10 The whole journey works on staging for all five salons

## Outcome

The integrated system runs on staging through the widget, picking up the other
developers' work (handoff hours in the plan), and the salon chain is given the
staging demo that its approval (W2) follows.

## Scope

- In: integration on staging, end-to-end runs, the demo session and its notes.
- Out: failure drills and the staging evaluation run (G12, in parallel with
  the approval wait); production.
- Depth: Build; staging booking API and test accounts only.

## Acceptance

- [ ] A1 Through the widget on staging, for each of the five salons: book →
  move → cancel for a test customer; the staging booking system shows the
  right final state; logs contain no conversation content.
- [ ] A2 The salon chain has seen the staging demo and has the approval
  request with the list of what was tested and what is deferred.

Verification: authorised staging runs only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-staging-rehearsal.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
