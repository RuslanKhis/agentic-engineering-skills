---
goal: G14
title: An attacker cannot read another customer's data, file without confirmation or steer the agent through photos
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G05, G07, G10]
phase: 1
profile: production
estimate: 60-100 h
status: blocked
---

# G14 An attacker cannot read another customer's data, file without confirmation or steer the agent through photos

## Outcome

A threat model with the trifecta table, tool tiers and enforcement-point map, plus an adversarial suite in CI, reviewed and signed off by the security reviewer. Implements D3, D4, D5, I1, I2, I5, I6 in the design.

## Scope

- In: `docs/security/threat-model.md` mapped to OWASP LLM IDs; adversarial tests (cross-customer IDs in every argument and route, prompt to submit, injected photo text, oversized inputs, prompt-to-promise); review notes.
- Out: External red team (P2-02).
- Depth: Build: threat model and adversarial suite; reviewer time ≤ 36 h (engineers implement).
- Route: Tests use scripted models and the fake Guidewire; `before_tool_callback` assertions.
- Prerequisites: G05, G07, G10.
- Supporting skills:
  - `adk-agent-evaluation`: adversarial cases with deterministic forbidden-action assertions in CI
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] Every row of the design's security-posture table has an enforcement point and a passing test.
- [ ] A scripted model that attempts each forbidden action produces no Guidewire call, no foreign read and no unconfirmed draft change visible only to the model.
- [ ] Forbidden: the suite fails CI if a submit-like tool or a Guidewire credential becomes reachable from the agent process.

Verification: Offline CI suite; security reviewer sign-off recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-threat-model-and-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
