---
goal: G01
title: Triage draft from a de-identified notification
design: docs/architecture/claims.md
plan: docs/plans/claims.md
primary_skill: protect-adk-sensitive-data
supporting_skills: [adk-model-and-output-contracts (draft schema)]
docs: []
blocked_by: []
touches: [app/deidentify.py, app/agent.py, app/schemas.py, tests/test_draft.py]
parallel_safe: yes
contracts: [C4]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: []
phase: 1
type: implementation
profile: MVP or pilot
estimate:
  hands_on: 3-4
  review_and_verify: 1-1.5
  total: 4-5.5
  handoff: none
  calendar_waits: none
owner: Dev A (Tom Reid)
status: ready
---

# G01 Triage draft from a de-identified notification

## Outcome

A handler sees a draft type and urgency for a new home claim, produced from a notification whose personal details were removed before the model saw it (D1: a draft for a person to accept). Implements R1.

## Scope

- In: notification parsing, de-identification step (Sensitive Data Protection de-identify template) before the model call, `draft_triage` LlmAgent with an output schema for type and urgency.
- Out: the cover position and clause citation (G02); the queue view (G03).
- Depth: pilot depth; floor kept (no secrets in code, model pinned as `gemini-3.5-flash-001` per D2, a person accepts every draft).

## Constraints

Stack and pins as in the design (D2, D5); identity comes from IAP (AGENTS.md); module paths are proposed, not inspected, since no repository exists yet.

## Resources created

none. Model calls in tests use a recorded double, so no usage spend.

## Acceptance

- [ ] A1 WHEN a notification arrives THE app SHALL return a draft with type and urgency (C4)
- [ ] A2 IF a note contains a name, phone or email THEN THE model request SHALL NOT contain it (C4)
- [ ] A3 IF de-identification fails THEN THE app SHALL withhold the draft and send nothing to the model (C4)
- [ ] A4 THE agent SHALL use the model pinned in D2 and hold no secret in code (floor)

Verification, automated: `python -m unittest tests.test_draft` on Python 3.12 with a recorded model double; offline; expected exit code 0. A3 and A4 are added to this module; the plan's A1 and A2 are kept as written.
Verification, manual: none.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/claims/G01-triage-draft.md. Read its design and plan,
use its primary and supporting skills and its companion skills at the pins
in AGENTS.md, keep its constraints and security rules, run its
verification locally, fill in the Evidence section and set status
(verified_local when every
acceptance case that can run offline has run here, in_progress with the owed
run named when the SDK is absent, verified_live after the authorised run,
done only when every acceptance item has fresh evidence and the owner
accepts). If Evidence starts with a Progress block, resume from it. Leave
changes uncommitted.
```
