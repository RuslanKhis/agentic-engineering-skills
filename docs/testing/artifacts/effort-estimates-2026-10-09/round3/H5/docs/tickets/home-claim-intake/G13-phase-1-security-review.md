---
goal: G13
title: An independent reviewer confirms the agent cannot be turned against customers or the claim system
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 10-16
  review_and_verify: 2-4
  total: 12-20
  calendar_waits: none
owner: Sec
status: blocked
---

# G13 An independent reviewer confirms the agent cannot be turned against customers or the claim system

## Outcome

Reviews D2, D5, D6 and invariants I1 to I4.

## Scope

- In:
  - Threat model, adversarial suite and service-account grant plan
  - Submission ledger design from the G01 contract and G06 work in progress
  - Findings with severity and OWASP LLM IDs
- Out: Penetration test (G23); re-check of G06's finished code (moved to G14 by the schedule check)
- Depth: Build.

## Acceptance

- [ ] Findings list with severity and owner
- [ ] No open critical finding before the pilot
- [ ] Each finding names the invariant it threatens

Verification: Reviewer sign-off; read-only review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-phase-1-security-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
