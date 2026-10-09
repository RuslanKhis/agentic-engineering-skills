---
goal: G14
title: Injected or forged requests cannot change another draft or file a claim
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G07, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 22-38
  review_and_verify: 10-16
  total: 32-54
  calendar_waits: none
  wait_days: 0
owner: Eng E
status: proposed
---

# G14 Injected or forged requests cannot change another draft or file a claim

## Outcome

Implements the design's security posture: capability checks in code and an adversarial suite with deterministic forbidden-effect assertions.

## Scope

- In: `before_tool_callback` checking owner and frozen-draft state; scripted-model adversarial tests (injection photo, foreign policy, forged IDs and hashes, 'file now', payout promises, oversized/polyglot uploads); findings mapped to OWASP IDs; live cases added to G08.
- Out: External pen test (G28).
- Depth: Production depth. Floor: assertions are on effects, not on wording.

## Acceptance

- [ ] Every forbidden action is refused at the trusted boundary with no mutation
- [ ] A frozen draft cannot be changed by any tool
- [ ] The trifecta table in the design matches the tools actually registered
- [ ] Findings are listed with OWASP IDs

Verification: Offline scripted-model tests.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G14-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
