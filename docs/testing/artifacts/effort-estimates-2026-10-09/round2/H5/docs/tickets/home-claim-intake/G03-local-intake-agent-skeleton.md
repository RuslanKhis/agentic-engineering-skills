---
goal: G03
title: Customer describes an incident and the agent fills a validated draft (local, fakes)
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-agent-instructions, adk-tool-interface-design, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 16–28
  review_and_verify: 8–12
  total: 24–40
  calendar_waits: none
owner: E2
status: ready
---

# G03 Customer describes an incident and the agent fills a validated draft (local, fakes)

## Outcome

Locally, Maria's water-leak account produces a complete `claim_draft` through `update_claim_draft` and a frozen version from `prepare_submission_summary`, using a fake policy adapter. D1, D2, D6.

## Scope

- In: Proposed layout `app/claim_intake/` (agent factory, instruction, tools), `app/drafts/` (draft model + repository), `tests/`; ADK `App` + `Runner` with `DatabaseSessionService` on local Postgres; `RunConfig(max_llm_calls=8)`; scripted-model Runner tests.
- Out: Photos (G07), identity (G06), Guidewire (G08), UI (G09).
- Depth: Production code kept. Floor: pinned model ID, call cap, no secrets. Screening (G11) and budgets beyond the call cap (G12) come later.
- Route: `LlmAgent(name='claim_intake', model='gemini-3.8-flash', tools=[...])`; tools read `customer_id` and policy list from session state set by the caller; draft repository with version + payload hash.
- Supporting skills: `adk-agent-instructions` (intake instruction, versioned prompt, rendered-request test); `adk-tool-interface-design` (the five tool declarations, bounded results, actionable errors); `adk-model-and-output-contracts` (pinned model config and thinking level)
- Execution scope: Local only.

## Acceptance

- [ ] ADK version pinned in the lockfile and confirmed against the installed package; any API differing from 2.8.0 noted
- [ ] Scripted run of the water-leak case produces a draft with all required FNOL fields and a frozen version + hash
- [ ] Tool list of `claim_intake` contains no submit/Guidewire tool (assertion)
- [ ] Restarting the process and resuming the session returns the same draft version
- [ ] Invalid field values return `{status: 'error', errors: [...]}` and leave the draft unchanged

Verification: Offline: `pytest tests/claim_intake` with a scripted model; local integration: Postgres restart test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-local-intake-agent-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
