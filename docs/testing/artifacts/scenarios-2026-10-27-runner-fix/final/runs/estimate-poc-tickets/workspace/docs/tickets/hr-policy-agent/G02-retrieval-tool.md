---
goal: G02
title: A search tool returns the right policy pages for a question
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-memory-architecture
supporting_skills: []
docs: [adk-memory-architecture/references/retrieval-strategy.md, adk-memory-architecture/references/local-document-coverage.md]
blocked_by: [G01]
touches: [hr_policy_agent/index.py, hr_policy_agent/tools.py, data/gold.json, tests/test_retrieval.py]
parallel_safe: no
contracts: [C2, C3]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [G01/A1, G01/A3]
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.5-1
  review_and_verify: 0.25
  total: 0.75-1.25
  handoff: none
  calendar_waits: none
owner: builder
status: ready
---

# G02 A search tool returns the right policy pages for a question

## Outcome

`search_policies(query)` ranks page-level passages by BM25 and returns document, page and text (D2). The builder writes 10 gold questions, each with its expected document and page, before looking at results.

## Scope

- In: index built from G01 records, the tool, gold file, retrieval check.
- Out: embeddings and hybrid search (P2-3), the agent (G03).
- Depth: build the retrieval hit check; the gold file records its author.

## Resources created

none

## Acceptance

- [ ] A1 WHEN a gold question is searched THE tool SHALL return its expected document and page within the top 5, and the run SHALL print the hit rate (C2)
- [ ] A2 THE index SHALL contain only documents in the manifest and SHALL expose the empty-text pages so the tool can say they were not searchable (C2, C3)
- [ ] A3 IF no passage scores above zero THEN THE tool SHALL return an explicit empty result, not nearby text (C3)

Verification, automated: `python -I -m pytest tests/test_retrieval.py -q` exits 0 on a synthetic corpus; the gold hit rate is run against the real PDFs.
Verification, manual: the builder checks that each gold expected page is correct.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G02-retrieval-tool.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent, verified_live after the authorised run, done only when every acceptance item has fresh evidence and the owner accepts). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
