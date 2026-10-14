---
goal: G10
title: Prove the Guidewire contract on the sandbox
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G09, W1]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-22
  review_and_verify: 4-6
  total: 18-28
  calendar_waits: see W1
owner: Eng B
status: blocked
---

# G10 Prove the Guidewire contract on the sandbox

## Outcome

Bounded live tests of G09 against the Guidewire sandbox, closing the O2 items G01 left open. Implements I1, I2 evidence.

## Scope

- In: a live test suite limited to sandbox test policies, a request cap, cleanup of created claims where Guidewire allows it; update to the contract document.
- Out: production credentials.
- Depth: authorised live check on sandbox only.

## Acceptance

- [ ] A test FNOL with two photos is created and found by external reference
- [ ] A forced re-send after a simulated lost reply finds the existing claim and creates none
- [ ] Description text with markup appears escaped in the ClaimCenter UI

Verification: Authorised live, sandbox only, after W1.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G10-guidewire-sandbox.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
