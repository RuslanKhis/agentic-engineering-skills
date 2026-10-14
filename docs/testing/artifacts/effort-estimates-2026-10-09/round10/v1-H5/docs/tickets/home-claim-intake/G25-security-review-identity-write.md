---
goal: G25
title: The security reviewer has checked who can file what, and that a claim is written once
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [safe-api-tool-calls]
blocked_by: [G04, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 6-10
  review_and_verify: 2-3
  total: 8-13
  calendar_waits: none
owner: Sec
status: blocked
---

# G25 The security reviewer has checked who can file what, and that a claim is written once

## Outcome

The reviewer reads the identity middleware, session ownership, confirm
binding and ledger as soon as they land, and records findings before the
adapter connects them to Guidewire.

## Scope

- In: review against invariants I1–I3; three or more reviewer-authored
  cases (cross-customer, replayed confirm, tampered hash); findings with
  owners; 1 h handoff from Eng E and Eng B.
- Out: injection controls (later review).
- Depth: production.

## Acceptance

- [ ] Each of I1–I3 has a test the reviewer agrees enforces it.
- [ ] No open high-severity finding.
- [ ] Reviewer-authored cases are in the suite and pass.

Verification: the reviewer's offline run; written findings.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G25-security-review-identity-write.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
