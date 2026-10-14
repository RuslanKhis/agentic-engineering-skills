---
goal: G06
title: The customer describes the loss and the assistant asks only for what is missing
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-agent-evaluation]
blocked_by: [G02, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 26-40
  review_and_verify: 8-14
  total: 34-54
  calendar_waits: none
owner: Eng C
status: blocked
---

# G06 The customer describes the loss and the assistant asks only for what is missing

## Outcome

The intake `LlmAgent` with the three tools from the design's model-facing contracts, a German and English instruction, and the emergency flag. Implements D1, D11.

## Scope

- In: `list_my_policies`, `update_claim_draft`, `get_draft_checklist`; scope from trusted state; `before_tool_callback` owner check; instruction `intake-v1`; rendered-request snapshot test.
- Out: photo reader (G08), submit (G11), eval set (G13).
- Depth: build; no submit tool exists.

## Acceptance

- [ ] A scripted conversation for Maria's burst pipe fills the checklist
- [ ] A tool call naming another customer's policy is refused by the callback and no write occurs
- [ ] The rendered request shows three tool declarations, no customer IDs in the instruction, and stays within the agreed byte size

Verification: Offline: scripted-model Runner tests; a small live smoke on Vertex in G14.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G06-intake-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
