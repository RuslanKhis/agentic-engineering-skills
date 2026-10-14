---
goal: G25
title: The filing path behaves against real Guidewire non-prod as it does against the fake
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G08, W1]
phase: 1
profile: production
estimate:
  hands_on: 8-12
  review_and_verify: 3-4
  total: 11-16
  calendar_waits: none
owner: Eng B
status: blocked
---

# G25 The filing path behaves against real Guidewire non-prod as it does against the fake

## Outcome

Live verification of the contract G01 took from documentation, once
non-prod access (W1) is granted; differences are fixed in the fake and the
adapter. Settles the open decision on dedup semantics behind I3. Owned by
Eng B; handoff: 1 h from Eng D on the adapter.

## Scope

- In: contract tests run against both the fake and Guidewire non-prod;
  fake and adapter fixes; update of the contract note.
- Out: production credentials (W7, used in G22).
- Assumption: live calls run over the integration team's existing non-prod
  network path; staging's own allowlist (W15) is needed for G20 and G24.
- Depth: production; non-prod tenant only.

## Acceptance

- [ ] A1 Every endpoint in the contract note is exercised against non-prod; recorded request and response shapes (redacted) match the fake or the fake is changed.
- [ ] A2 The same create sent twice with the same dedup key, and a lookup by our reference after a create, behave as G08 assumes; if not, G08's reconciliation is changed and its A3, A4 rerun.
- [ ] A3 Validation, 401, 403, 429, 5xx and timeout responses observed or confirmed with the integration team, and the error mapping updated.
- [ ] A4 The adapter contract test suite passes against both the fake and non-prod.
- [ ] A5 Rate and payload limits are recorded with their source.

Verification: authorised live calls to Guidewire non-prod with declared
request limits.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G25-guidewire-live-verification.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
