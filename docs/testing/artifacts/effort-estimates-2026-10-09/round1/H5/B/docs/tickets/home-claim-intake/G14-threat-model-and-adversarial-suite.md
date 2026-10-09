---
goal: G14
title: Threat model and adversarial suite prove the forbidden actions cannot run
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-tool-interface-design]
blocked_by: [G08, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 26-46
  review_and_verify: 14-24
  total: 40-70
  calendar_waits: External pen test booking (3-6 weeks lead); run on staging around week 11-12
owner: Security reviewer (threat model, review) with E3 (tests)
status: blocked
---

# G14 Threat model and adversarial suite prove the forbidden actions cannot run

## Outcome

The security reviewer can sign off that no model output, photo or customer message can create a claim, reach another customer's data or exfiltrate data. Implements D3, I1, I3, I10.

## Scope

- In: Threat model mapped to OWASP LLM/Agentic IDs; tool tiers; `before_tool_callback` capability checks keyed on trusted owner; adversarial suite (cases listed in the design) asserting forbidden calls never run; pen-test scope and findings triage.
- Out: Fixes for pen-test findings beyond triage are new tickets.
- Depth: Production: threat model and adversarial suite.
- Route: Scripted-model pytest suite in CI.
- Supporting skills: `adk-tool-interface-design` (tool tiering in declarations)
- Execution scope: Local suite; pen test needs a contract and a staging target.

## Acceptance

- [ ] Every adversarial case asserts no Guidewire call, no foreign-owner read and no draft change outside the owner
- [ ] Trifecta table re-checked against the code
- [ ] Pen test booked with scope; findings triaged before the pilot
- [ ] Suite runs in CI and fails the build on a forbidden call

Verification: Offline in CI; pen test on staging (authorized external party).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-threat-model-and-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
