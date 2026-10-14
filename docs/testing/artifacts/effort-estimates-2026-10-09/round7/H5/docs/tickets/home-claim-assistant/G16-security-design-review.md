---
goal: G16
title: Security reviewer agrees the design's structure
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 2-4
  total: 10-16
  calendar_waits: none
owner: Sec Reviewer
status: ready
---

# G16 Security reviewer agrees the design's structure

## Outcome

The part-time security reviewer reviews D1, D3, D5, D6, D9 and the security posture table before code hardens, and records findings for G17.

## Scope

- In: written findings with severity, agreed adversarial cases, decision on O5 (upload scanning).
- Out: code review (G23).
- Depth: design review only.

## Acceptance

- [ ] Findings are recorded against decision IDs with an owner
- [ ] O5 has a decision or a dated follow-up
- [ ] The adversarial case list for G17 is agreed

Verification: Document review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G16-security-design-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
