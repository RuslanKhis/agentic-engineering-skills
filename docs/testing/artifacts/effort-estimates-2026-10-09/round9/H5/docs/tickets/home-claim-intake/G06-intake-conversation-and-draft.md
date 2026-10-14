---
goal: G06
title: The assistant gathers a complete first notice of loss into a saved draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts, adk-agent-evaluation]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 28-46
  review_and_verify: 8-14
  total: 36-60
  calendar_waits: none
owner: Agent
status: blocked
---

# G06 The assistant gathers a complete first notice of loss into a saved draft

## Outcome

Implements D1, D2, D12 and I4: Anna's answers become a versioned, validated `ClaimDraft` whose completeness is computed in code.

## Scope

- In: `ClaimDraft` model and repository (versioned), `update_claim_draft` tool returning `{status, missing_fields, errors}`, DE/EN instruction as versioned files with state templating for the policy list and missing fields, the deterministic emergency rule, the coverage-statement check in `after_model_callback`.
- Out: Photo analysis (G08). Submission (G10). Quality tuning (G19).
- Depth: Build. The tool can touch only the session's own draft (scope from state).

Supporting skills and why:
- adk-tool-interface-design (`update_claim_draft` schema and errors)
- adk-model-and-output-contracts (draft field validation)
- adk-agent-evaluation (Runner tests)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] A scripted conversation for the burst-pipe journey ends with a draft whose completeness = true and whose fields match the expected values.
- [ ] Restarting the process mid-conversation and resuming keeps the draft version and the missing-field list.
- [ ] 'Gas smell' / 'Gasgeruch' shows the emergency message before any other output, whatever the model says.
- [ ] A scripted model reply stating a payout amount is replaced by the neutral adjuster message (I4).
- [ ] The captured model request shows 3 tools, the versioned instruction, and no customer ID or secrets in the instruction text.

Verification: Offline: pytest with scripted model. Bounded live: 5 conversations on Vertex EU under a call cap, only when authorised.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-intake-conversation-and-draft.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
