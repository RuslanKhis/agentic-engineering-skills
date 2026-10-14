---
goal: G17
title: Injection cannot cause harm
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G06, G07, G08, G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 24-36
  review_and_verify: 8-14
  total: 32-50
  calendar_waits: none
owner: Eng C
status: blocked
---

# G17 Injection cannot cause harm

## Outcome

A threat model mapped to OWASP LLM and agentic IDs and an adversarial suite for the intake agent and photo reader, asserting forbidden actions never run. Implements the security posture table.

## Scope

- In: cases from G16, scripted and live-model variants, CI job for the scripted set.
- Out: submit-route cases (in G11), pen test (G23).
- Depth: build.

## Acceptance

- [ ] Every agreed case passes in CI with deterministic assertions on tool calls and writes
- [ ] Injected text in photos and messages never changes another customer's data or creates an operation
- [ ] Threat model lists residual risks with owners

Verification: Offline scripted; bounded live variant.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G17-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
