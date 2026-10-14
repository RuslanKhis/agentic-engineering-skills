---
goal: G15
title: The DPO has everything needed to sign the DPIA for the pilot and GA
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [protect-adk-sensitive-data]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 24-36
  review_and_verify: 4-6
  total: 28-42
  calendar_waits: none
owner: Sec
mentions_only: [W4, wait]
status: ready
---

# G15 The DPO has everything needed to sign the DPIA for the pilot and GA

## Outcome

A DPIA draft and AI-transparency pack prepared from the design, so that the
DPO review (W6) runs while the build continues. Covers purposes, lawful
basis, data map, retention (A15), residency (A7), processors (Google,
Guidewire), risks to customers and mitigations by design decision, and the
EU AI Act transparency notice.

## Scope

- In: `docs/compliance/dpia-home-claim-intake.md`; processor list with
  regions; risk register referencing D2, D4, D9, D12; answers needed from
  product on A9 and A15; updated evidence links once the data-boundary and
  adversarial work lands.
- Out: legal approval of customer wording (W4).
- Depth: production; written from the design, not from finished code.

## Acceptance

- [ ] The DPO accepts the pack for review (the clock on W6 starts).
- [ ] Every data class in the design's data table appears with purpose, basis and retention.
- [ ] Each high risk names its mitigating decision and the goal that builds it.

Verification: document review by the DPO; no code.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G15-dpia-pack.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
