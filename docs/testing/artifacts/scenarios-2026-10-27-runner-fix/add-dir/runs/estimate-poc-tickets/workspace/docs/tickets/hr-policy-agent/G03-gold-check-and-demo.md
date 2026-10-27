---
goal: G03
title: Know how often the agent is right, and be ready for Friday
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-agent-evaluation
supporting_skills: []
docs: [adk-agent-evaluation/references/evaluation-design.md]
blocked_by: [G02]
touches: [eval/, docs/demo-runbook.md]
parallel_safe: no
contracts: [C1, C2]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G01/A1, G02/A1, G02/A2]
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.75-1.0
  review_and_verify: 0.25
  total: 1.0-1.25
  handoff: none
  calendar_waits: none
owner: developer
status: ready
---

# G03 Know how often the agent is right, and be ready for Friday

## Outcome

A runner replays 10 to 12 gold questions and 3 out-of-scope questions, prints a table of expected against cited document and page, and the developer fixes what it shows. A one-page run-of-show and one rehearsal are done. Implements D6; the demo says whether the gold set is HR-verified.

## Scope

- In: gold file with provenance (who wrote each, which page), runner, citation check, run-of-show.
- Out: HR-verified set (phase 2 G07); a slide deck.
- Depth: proof of concept; include two questions whose answer spans two pages and one paraphrase ("time off").

## Acceptance

- [ ] A1 WHEN the runner finishes THE runner SHALL fail any answer citing a document and page the turn's search did not return (C1)
- [ ] A2 WHEN the runner finishes THE runner SHALL report per question whether the expected page was cited, and the total (C1)
- [ ] A3 WHEN an out-of-scope question is asked THE agent SHALL answer that the policies do not cover it and SHALL NOT state a policy from general knowledge (C2)

Verification, automated: `python -I eval/run_gold.py` exits 0 only when A1 holds for every question; the hit rate is recorded, not gated. It makes live model calls, so the developer runs it after confirming the spend cap.
Verification, manual: developer reads every answer once and rehearses the run-of-show with the demo questions.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G03-gold-check-and-demo.md. Read its design and plan, use its primary skill, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
