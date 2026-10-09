---
goal: G12
title: Runaway and abusive use stops safely and emergencies reach a human
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: [adk-agent-instructions]
blocked_by: [G03, G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 26–42
  review_and_verify: 14–22
  total: 40–64
  calendar_waits: none
owner: E3
status: blocked
---

# G12 Runaway and abusive use stops safely and emergencies reach a human

## Outcome

Per-invocation, per-session and per-customer limits, a Cloud Armor rate limit, one retry policy owner, an operator kill switch to the classic form, and `escalate_to_human` with a code-driven emergency banner. D11, D13, I8.

## Scope

- In: Admission table in Postgres; session caps; retry policy for Vertex calls (SDK retries configured once); kill switch flag read per request; emergency keyword banner; escalation reason codes.
- Out: Load measurement (G17).
- Depth: Production. Floor: spend stop and kill switch outside agent authority.
- Route: Admission check in the `/turns` handler before `Runner`; `RunConfig.max_llm_calls`; flag in a config table or Secret/Parameter.
- Supporting skills: `adk-agent-instructions` (escalation guidance and reason codes in the instruction)
- Execution scope: Dev project.

## Acceptance

- [ ] A scripted looping model stops at 8 calls with the designed message
- [ ] Fourth claim session in a day for one customer is refused with the phone and form options
- [ ] Kill switch on: new sessions get the form with prefill; in-flight submissions still complete
- [ ] 'Water is near the fuse box' shows the emergency banner without a model call and escalation is offered

Verification: Offline tests; dev check of the kill switch.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-budgets-limits-and-handoff.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
