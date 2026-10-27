---
goal: G01
title: Index the 30 HR policy PDFs and show what could not be read
design: docs/architecture/hr-policy-agent.md
plan: docs/architecture/hr-policy-agent.md
primary_skill: adk-memory-architecture
supporting_skills: []
docs: [adk-memory-architecture/references/document-ingestion.md]
blocked_by: []
touches: [AGENTS.md, requirements.txt, .gitignore, scripts/ingest.py, data/index/, docs/coverage-report.md, tests/test_ingest.py]
parallel_safe: no
contracts: [C3]
companion_skills: []
security: []
design_system: none
contract_deltas: [none]
pass_to_pass: []
phase: 1
type: implementation
profile: proof of concept
estimate:
  hands_on: 0.75-1.0
  review_and_verify: 0.25-0.5
  total: 1.0-1.5
  handoff: none
  calendar_waits: none
owner: developer
status: ready
---

# G01 Index the 30 HR policy PDFs and show what could not be read

## Outcome

One command turns `data/pdfs/` into `data/index/pages.jsonl` (document id, title, page, text) and a coverage report listing pages with no text. Implements D1. Rulings taken here: the extraction library, the ADK version pin (design assumes 2.8.0; confirm), and the title for each PDF (filename unless the PDF has a title).

## Scope

- In: skeleton, pinned dependencies, `AGENTS.md` with pins, ingestion script, report.
- Out: search, agent (G02); OCR (phase 2 G04).
- Depth: proof of concept; floor kept: key in environment only, `.env` git-ignored.

## Acceptance

- [ ] A1 WHEN the ingest script runs on `data/pdfs/` THE script SHALL write one index record per page of every PDF, empty pages included with empty text (C3)
- [ ] A2 IF a PDF cannot be opened THEN THE script SHALL exit non-zero naming the file and write no partial index (C3)
- [ ] A3 WHEN the report is produced THE report SHALL list per document pages, empty pages and an overall empty-page count, so scans are visible (C3)
- [ ] A4 THE repository SHALL NOT contain an API key in any tracked file, and dependency versions are pinned (floor)

Verification, automated: `python -I -m pytest tests/test_ingest.py` exits 0, using a small generated fixture PDF (no real HR documents committed).
Verification, manual: developer reads the report and confirms the page counts match two PDFs opened by hand.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-ingest-and-coverage.md. Read its design and plan, use its primary skill, keep its constraints, run its verification locally, fill in the Evidence section and set status (verified_local when every acceptance case that can run offline has run here, in_progress with the owed run named when the SDK is absent). If Evidence starts with a Progress block, resume from it. Leave changes uncommitted.
```
