---
goal: G15
title: "Injection and cross-customer attacks are proven not to cause writes or disclosure"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G07, G08, G10, G28]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 14-20
  review_and_verify: 8-12
  total: 22-32
  calendar_waits: none
  wait_days: 0
owner: Security eng
status: blocked
---

# G15 Injection and cross-customer attacks are proven not to cause writes or disclosure

## Outcome

Threat model with OWASP mapping and a deterministic adversarial suite in CI. Implements I1, I2, I4; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g15--injection-and-cross-customer-attacks-are-proven-not-to-cause-writes-or-disclosure).

## Scope

- In: Threat model; cases: instructions in photos, fake handler messages, other policy numbers, 'submit now', oversized results; forbidden-action assertions.
- Out: External pen test (G19).
- Depth: Build.

## Acceptance

- [ ] Every case asserts the Guidewire client was never called and no other customer's data appeared.
- [ ] Threat model and enforcement-point map written for the reviewer (G20).
- [ ] Suite runs in CI and fails by exit code on a seeded regression.

Verification: Offline scripted-model tests. Execution scope: Local and CI.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
