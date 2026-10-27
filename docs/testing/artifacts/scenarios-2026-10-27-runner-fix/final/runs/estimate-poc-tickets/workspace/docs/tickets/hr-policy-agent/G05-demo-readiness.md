---
goal: G05
title: The Friday demo runs smoothly and survives a model outage
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-engineer
supporting_skills: []
docs: [adk-engineer/references/operating-rules.md]
blocked_by: [G03]
touches: [docs/demo/script.md, docs/demo/fallback-transcript.md]
parallel_safe: no
contracts: [C5]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G03/A2]
phase: 1
type: presentation
profile: proof of concept
estimate:
  hands_on: 0.5
  review_and_verify: 0-0.25
  total: 0.5-0.75
  handoff: none
  calendar_waits: none
owner: builder
status: blocked
---

# G05 The Friday demo runs smoothly and survives a model outage

## Outcome

A one-page demo script (5 questions HR leaders ask, one not-found, one referral case), one full dry run, and a saved transcript to show if the model API is slow or down (D5). The deck skill is not installed here, so this is demo readiness, not a presentation deck. G04's measured result, or its absence, is stated on the script.

## Scope

- In: script, dry run, fallback transcript, spend check, key revoked after the demo.
- Out: slides; hosting for anyone else.
- Depth: floor kept.

## Resources created

none. Usage spend only, inside the C5 quota.

## Acceptance

- [ ] A1 WHEN the dry run completes THE script SHALL list each demo question with its cited page and the fallback transcript SHALL hold the same answers (C5, floor)
- [ ] A2 THE quota SHALL be confirmed in place before the demo, and the demo key SHALL be revoked afterwards (C5)

Verification, automated: none beyond G03's tests, which keep passing.
Verification, manual: the builder confirms the dry run and the quota; the Evidence line reads `manual: ... confirmed by the builder, date`, or `owed`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G05-demo-readiness.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent, verified_live after the authorised run, done only when every acceptance item has fresh evidence and the owner accepts). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
