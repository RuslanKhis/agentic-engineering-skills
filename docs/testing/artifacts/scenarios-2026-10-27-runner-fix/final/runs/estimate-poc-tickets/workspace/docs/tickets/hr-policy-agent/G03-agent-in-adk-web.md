---
goal: G03
title: I ask a policy question in adk web and get a cited answer
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-engineer
supporting_skills: [adk-memory-architecture (tool and retrieval integration)]
docs: [adk-engineer/references/operating-rules.md]
blocked_by: [G02, W1]
touches: [hr_policy_agent/agent.py, hr_policy_agent/guards.py, tests/test_guards.py, .gitignore]
parallel_safe: no
contracts: [C1, C5]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G02/A1, G02/A3]
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.75-1
  review_and_verify: 0.25-0.5
  total: 1-1.5
  handoff: none
  calendar_waits: W1
owner: builder
status: blocked
---

# G03 I ask a policy question in adk web and get a cited answer

## Outcome

One `LlmAgent` with `search_policies` as its only tool runs in `adk web` on loopback (D1, D5). A citation check and a call cap guard it. Ruling taken here: the model ID is pinned from the dated lifecycle table (D4), and the key is read from the environment.

## Scope

- In: agent, instruction, `after_model_callback` citation check, `before_model_callback` cap, key setup.
- Out: measurement (G04), demo script (G05).
- Depth: floor kept. The agent has no tool that writes; the provider quota is set by the builder.

## Resources created

Usage spend only: a provider quota of at most USD 10, set before the first live call.

## Acceptance

- [ ] A1 IF the model cites a document and page that the tool did not return THEN THE agent SHALL replace the answer with the fixed not-found message (C1)
- [ ] A2 WHEN a question's model calls exceed the cap THE agent SHALL stop and say so (C5)
- [ ] A3 THE repository SHALL NOT contain the API key, and the pinned model ID SHALL appear in one config line (C5, floor)

Verification, automated: `python -I -m pytest tests/test_guards.py -q` exits 0 with a fake model response.
Verification, manual: one live question in `adk web` returns a cited answer; the builder confirms the quota exists.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G03-agent-in-adk-web.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent, verified_live after the authorised run, done only when every acceptance item has fresh evidence and the owner accepts). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
