---
goal: G04
title: I know how often the agent cites the right policy
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-agent-evaluation
supporting_skills: []
docs: [adk-agent-evaluation/references/live-evaluations.md, adk-agent-evaluation/references/deterministic-tests.md]
blocked_by: [G03]
touches: [evals/run_gold.py, data/gold.json, data/refusal_cases.json, evals/results/]
parallel_safe: no
contracts: [C1, C4]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G03/A1]
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.25-0.5
  review_and_verify: 0.25
  total: 0.5-0.75
  handoff: none
  calendar_waits: none
owner: builder
status: blocked
---

# G04 I know how often the agent cites the right policy

## Outcome

The 10 gold questions and 3 refusal cases run through the agent. The result table shows, per question, the expected and cited pages and the answer, and the builder marks each correct or not. If G03 closed late, the cut line in the design applies (5 questions, or a hand read).

## Scope

- In: runner, results table, up to three prompt or retrieval fixes for the worst failures.
- Out: HR reviewer labels, 30+ questions (P2-1).
- Depth: small hand-labelled set; results are labelled as builder-reviewed, not HR-reviewed.

## Resources created

Usage spend only: at most 40 model calls, inside the C5 quota.

## Acceptance

- [ ] A1 WHEN the gold set runs THE runner SHALL write a table of question, expected page, cited pages and verdict, and print the share of answers whose citation matches (C1)
- [ ] A2 WHEN a refusal case names a person or asks for a legal or eligibility decision THE agent SHALL answer with general policy and an HR referral, not a determination (C4)
- [ ] A3 IF a question has no answer in the corpus THEN THE agent SHALL say it was not found (C1)

Verification, automated: `python -I evals/run_gold.py data/gold.json` exits 0 and writes `evals/results/`; exit 1 only when the runner itself fails.
Verification, manual: the builder reads every answer and records the verdict.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G04-answer-quality-check.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent, verified_live after the authorised run, done only when every acceptance item has fresh evidence and the owner accepts). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
