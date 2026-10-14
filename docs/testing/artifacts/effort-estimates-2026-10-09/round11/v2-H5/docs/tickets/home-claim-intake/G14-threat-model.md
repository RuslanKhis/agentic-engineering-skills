---
goal: G14
title: Hostile text or photos cannot make the assistant file, reveal or promise anything
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G03, G06, G15]
phase: 1
profile: production
estimate:
  hands_on: 16-24
  review_and_verify: 6-10
  total: 22-34
  calendar_waits: none
owner: Eng A
status: proposed
---

# G14 Hostile text or photos cannot make the assistant file, reveal or promise anything

## Outcome

Threat model and an adversarial suite proving invariant I5 and the D1
split, including the extra cases the security reviewer lists in G15/A2.
Handoff: 1 h from Eng E on the identity boundary.

## Scope

- In: `docs/security/threat-model.md` (trifecta table, tool tiers, trust
  boundaries, OWASP LLM and Agentic IDs), `tests/adversarial/` (scripted
  model cases and a live subset), request body and turn size limits.
- Out: screening configuration (G12); filing and policy cases that need G08 (G36); external testing.
- Depth: production.

## Acceptance

- [ ] A1 A test lists the agent's tools and fails if any tool other than the four own-draft tools is registered, or if any tool accepts a customer, policy or draft ID.
- [ ] A2 At least 30 adversarial cases (instructions printed in photos, in messages, in a pasted contractor invoice; attempts to change the policy, file the claim, read another customer's data, obtain a coverage promise) leave no submission operation, no cross-customer read and no coverage statement; asserted on stored state, not on reply text.
- [ ] A3 Oversized message bodies, too many image parts and very long turns are rejected at the API boundary with bounded memory.
- [ ] A4 Findings and residual risks are mapped to OWASP LLM and Agentic IDs in the threat model.

Verification: offline scripted-model suite in CI; bounded live run of the
live subset under the non-prod cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-threat-model.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
