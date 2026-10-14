---
goal: G06
title: Maria can describe her water damage and the agent builds a complete claim draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts, adk-agent-evaluation]
blocked_by: [G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 30-45
  review_and_verify: 10-15
  total: 40-60
  calendar_waits: none
owner: Eng A
mentions_only: [G08]
status: blocked
---

# G06 Maria can describe her water damage and the agent builds a complete claim draft

## Outcome

Implements D1, D5, D10 and invariants I4 and I5: the intake instruction, the
`update_claim_draft` tool, the versioned `claim_drafts` record, the
deterministic release check and emergency signposting, in two languages (A1).

## Scope

- In: instruction files under `app/agent/instructions/` (versioned);
  `update_claim_draft(fields)` with per-field validation and a `missing`
  list in its result (≤ 2 KB); required-field rules in code; `claim_drafts`
  table with versions and 7-day resume; `after_model_callback` release
  check with per-language rules; emergency keywords and fixed text from
  configuration; 15 scripted conversation cases as the goal's own tests;
  rendered-request test showing instruction, two tool declarations and
  injected state.
- Out: photos in the draft (G08); full evaluation set (G24); confirm (G09).
- Depth: production; measured on the goal's scripted cases now and the
  conversation set later.

## Acceptance

- [ ] Maria's journey (kitchen ceiling leak) produces a draft with every required field and no question asked twice.
- [ ] A scripted model reply promising cover or an amount is replaced before release.
- [ ] "Gas smell" or "water still pouring" shows the emergency text even when the model call fails.
- [ ] Draft survives a process restart and is resumed in a new session by its owner only.
- [ ] Captured request contains no customer identifier in the instruction text and exactly two tool declarations.

Verification: offline Runner tests with a scripted model; a bounded live run
of the 15 cases (≤ 200 model calls) recorded.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-intake-conversation-and-draft.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
