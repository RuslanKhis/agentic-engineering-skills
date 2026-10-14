---
goal: G13
title: Threat model and an adversarial suite that proves forbidden actions never run
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G06, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 20-32
  review_and_verify: 8-14
  total: 28-46
  calendar_waits: none
owner: Lead
status: blocked
---

# G13 Threat model and an adversarial suite that proves forbidden actions never run

## Outcome

Implements and evidences I5, I1 and the security posture table in the design.

## Scope

- In: Threat model (OWASP LLM01/02/06/08 mapping), enforcement-point map, trifecta table per agent, `before_tool_callback` capability checks, an adversarial suite: text-in-image injection, a hostile loss description, cross-draft tool arguments, coverage bait, 'submit for me', prompt-leak attempts, an oversized-input loop.
- Out: Submission-path forbidden effects (owned by G10). External pen test (W3).
- Depth: Production depth: the suite runs in CI with deterministic assertions.

Supporting skills and why:
- adk-agent-evaluation (suite runner)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Every adversarial case asserts on tool-call logs and stored state, not on model prose. All pass.
- [ ] Each threat in the model maps to an enforcing component and a test, or to an accepted risk with an owner.
- [ ] The suite runs in CI and fails the build on a forbidden call.

Verification: Offline: scripted-model and recorded-model cases in CI.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G13-threat-model-and-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
