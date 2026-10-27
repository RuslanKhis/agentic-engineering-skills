---
goal: G01
title: I can see exactly what text is in each of the 30 HR PDFs
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-memory-architecture
supporting_skills: []
docs: [adk-memory-architecture/references/document-ingestion.md, adk-memory-architecture/references/local-document-coverage.md]
blocked_by: [none]
touches: [pyproject.toml, hr_policy_agent/ingest.py, data/manifest.json, tests/test_ingest.py]
parallel_safe: no
contracts: [C2, C3]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: [none]
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

# G01 I can see exactly what text is in each of the 30 HR PDFs

## Outcome

An ingestion script reads the PDFs from a local folder and writes a manifest (file, SHA-256, title, page count) and a per-page extraction record. It reports empty or failed pages (D3). It also confirms the ADK pin against 2.8.0.

## Scope

- In: project skeleton with pinned dependencies, `ingest.py`, manifest, report.
- Out: indexing (G02), OCR (phase 2).
- Depth: floor only. The PDFs stay local and git-ignored; no secrets.

## Resources created

none

## Acceptance

- [ ] A1 WHEN ingestion runs on the PDF folder THE script SHALL write one extraction record per page of every PDF and list each empty-text page by document and page (C3)
- [ ] A2 IF a PDF cannot be opened THEN THE script SHALL exit 1 and name the file rather than skip it (C3)
- [ ] A3 THE manifest SHALL list every PDF once by hash, and a re-run SHALL give an identical manifest (C2)

Verification, automated: `python -I -m pytest tests/test_ingest.py -q` exits 0, run on three small synthetic PDFs: text, empty page, corrupt file.
Verification, manual: the builder reads the empty-page list and notes scans for phase 2.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-corpus-ingestion.md. Read its design and plan, use its primary and supporting skills, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent, verified_live after the authorised run, done only when every acceptance item has fresh evidence and the owner accepts). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
