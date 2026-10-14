---
goal: G26
title: An independent reviewer has checked the identity, filing and adversarial code before external testing
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-tool-auth-and-secrets, safe-api-tool-calls]
blocked_by: [G03, G08, G14, G15, G36]
phase: 1
profile: production
estimate:
  hands_on: 5-7
  review_and_verify: 1-1
  total: 6-8
  calendar_waits: none
owner: SecRev
status: proposed
---

# G26 An independent reviewer has checked the identity, filing and adversarial code before external testing

## Outcome

The security reviewer reads the identity middleware, the filing operation
and the adversarial suites of G14 and G36, and states whether staging is ready for the
external test. Handoff: 1 h from Eng A, Eng B and Eng E.

## Scope

- In: code review findings with severity; readiness statement.
- Out: fixes (G38).
- Depth: production.

## Acceptance

- [ ] A1 Findings on the identity, filing and adversarial code are recorded; critical and high ones are fixed in G38 before the external test starts.
- [ ] A2 The reviewer records that staging is ready for external testing, or lists what blocks it.

Verification: code review; no new code.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G26-security-code-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
