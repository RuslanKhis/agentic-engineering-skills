---
goal: G09
title: End-to-end launch check and beta release
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-release-engineering]
blocked_by: [G03, G05, G06, G08]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: salon manager go/no-go (0-1 day)
owner: Dev C
status: blocked
---

# G09 End-to-end launch check and beta release

## Outcome

The full journey works on staging against the staging booking API, the 30-case run meets the bar and the beta link goes live. Checks all invariants.

## Scope

- In: redeploy with G03's handlers and G05's widget; G06 rerun including write cases; staging walkthrough with a salon manager; p95 turn latency on 20 turns; `docs/runbooks/launch.md`; flag flip
- Out: CI gate (G10), streaming (G14)
- Depth: release bar (assumed): ≥ 90 % overall, 100 % on refuse-other-customer and no-write-without-confirm cases

## Acceptance

- [ ] Maya's move journey completes on staging and the card matches the booking system
- [ ] An `uncertain` row is found by the operator query; rollback rehearsed once
- [ ] No write happens in any eval case without a confirm call

Verification: Hosted staging evidence, then the production flag flip with the team's go decision.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-launch-check.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
