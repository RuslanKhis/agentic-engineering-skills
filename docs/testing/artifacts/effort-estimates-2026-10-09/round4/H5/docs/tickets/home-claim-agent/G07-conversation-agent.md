---
goal: G07
title: The assistant gathers a complete home-claim FNOL safely in the customer's language
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-agent-evaluation]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 30-50
  review_and_verify: 10-16
  total: 40-66
  calendar_waits: none
  wait_days: 0
owner: Eng D
status: proposed
---

# G07 The assistant gathers a complete home-claim FNOL safely in the customer's language

## Outcome

Implements D2, I5 and I6: the instruction, three bounded tools, emergency flag and the forbidden-commitment check.

## Scope

- In: `app/agent/instructions/` (versioned), tools `list_my_policies`, `update_claim_draft`, `show_summary_for_confirmation` with bounded results and actionable errors; post-response commitment check.
- Out: Submission (G09, G10), UI (G11, G12), launch-language tuning (G30).
- Depth: Production depth. Floor: no submission tool; identity only from trusted state.

## Acceptance

- [ ] The rendered request shows the versioned instruction, exactly 3 tools and no identity parameter
- [ ] On the G08 development set, field completeness and no-commitment results are reported
- [ ] An emergency message produces the emergency flag and fixed guidance in the same turn
- [ ] 'Just file it now' produces the confirmation card, never a submission

Verification: Offline scripted Runner tests plus G08 development-set run within its cost ceiling.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G07-conversation-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
