---
goal: G23
title: Independent testers find no open high-severity issue
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G10, G11, G15, G17, W3]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-20
  review_and_verify: 2-4
  total: 14-24
  calendar_waits: pen-test window
  wait_days: 10-15
owner: Sec Reviewer
status: blocked
---

# G23 Independent testers find no open high-severity issue

## Outcome

External pen test of staging (API, upload, agent) coordinated by the security reviewer, followed by sign-off or a list of blockers for G24.

## Scope

- In: scope letter, test window, findings triage.
- Out: fixing (G24).
- Depth: review.

## Acceptance

- [ ] Findings are triaged with severity and owner
- [ ] Sign-off states the conditions for real customers
- [ ] Testers received no production data

Verification: External test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G23-pen-test-sign-off.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
