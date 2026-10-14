---
goal: G24
title: Fix what the pen test found
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-security
supporting_skills: [safe-api-tool-calls]
blocked_by: [G23]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-26
  review_and_verify: 4-8
  total: 18-34
  calendar_waits: none
owner: Eng C
status: blocked
---

# G24 Fix what the pen test found

## Outcome

Remediate critical and high findings from G23 and add a regression test for each.

## Scope

- In: fixes and tests.
- Out: medium and low findings, which get dated follow-ups.
- Depth: build.

## Acceptance

- [ ] Each critical/high finding has a fix and a test that failed before it
- [ ] Security reviewer confirms closure
- [ ] Deferred findings have owners and dates

Verification: Offline tests plus reviewer retest.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G24-security-remediation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
