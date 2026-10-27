---
goal: G02
title: Ask a policy question in adk web and get a cited answer
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-engineer
supporting_skills: [adk-memory-architecture (retrieval tool over the page index)]
docs: [adk-memory-architecture/references/local-document-coverage.md]
blocked_by: [G01]
touches: [hr_policy_agent/, tests/test_search.py, tests/test_agent.py]
parallel_safe: no
contracts: [C1, C2, C4, C5]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G01/A1]
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.75-1.25
  review_and_verify: 0.5
  total: 1.25-1.75
  handoff: none
  calendar_waits: none
owner: developer
status: ready
---

# G02 Ask a policy question in adk web and get a cited answer

## Outcome

An `LlmAgent` with one tool, `search_policies`, runs under `adk web` on loopback and answers with document and page citations, or says the policies do not cover it. Implements D2 to D5. Rulings taken here: pinned model ID (check the dated lifecycle table; record if it was unavailable) and the match threshold.

## Scope

- In: BM25 search over `pages.jsonl`, agent instruction, search-count callback.
- Out: gold-set evaluation (G03); embeddings (phase 2 G05).
- Depth: proof of concept; floor kept. The developer sets the key-level spend cap before the first live run.

## Constraints

Loopback only; no tool other than `search_policies`; key from the environment.

## Acceptance

- [ ] A1 WHEN `search_policies` is called THE tool SHALL return up to 5 passages, each with document id, title, page and text (C1)
- [ ] A2 IF no page clears the threshold THEN THE tool SHALL return `status: no_match` and the agent SHALL reply that the policies do not cover it and refer to HR (C2)
- [ ] A3 THE agent SHALL have exactly one tool and no write capability (C4)
- [ ] A4 IF a turn makes a fifth search call THEN THE callback SHALL return an error result without searching (C5)
- [ ] A5 THE agent SHALL use a pinned model ID, and the developer's spend cap SHALL be confirmed before the first live run (floor)

Verification, automated: `python -I -m pytest tests/test_search.py tests/test_agent.py` exits 0, no model call.
Verification, manual: developer asks 3 questions in `adk web` and reads the citations against the PDFs; confirms the cap in the key or project settings.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G02-grounded-search-agent.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
