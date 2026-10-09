---
goal: G01
title: The 30 HR policy PDFs are searchable by page
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-memory-architecture
supporting_skills: []
blocked_by: [O1]
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK applied
  hands_on: 0.75-1
  review_and_verify: 0.25-0.5
  total: 1-1.5
  calendar_waits: none assumed; O1 (endpoint approval for HR documents) may add one
owner: the builder
status: ready
---

# G01 The 30 HR policy PDFs are searchable by page

## Outcome

The builder runs one script to turn the PDFs in a local folder into a page-level
search index and an ingestion report showing what was extracted. The project
skeleton, pins and model access are confirmed. Implements D1, D4 (access
check), D6.

## Scope

- In: project skeleton (`pyproject.toml` or `requirements.txt` pinning
  `google-adk`, `config.py` with model ID `gemini-3.8-flash`, index path, call
  cap 6); `ingest.py`: per-page text extraction (e.g. `pypdf`), an ingestion
  report (file, pages, characters per page, pages with no text), and a SQLite
  FTS5 table `(doc, page, text)` ranked with `bm25()`, following
  `adk-memory-architecture` `references/retrieval-strategy.md`; a
  `search(query, k)` function the G02 tool will wrap; `.gitignore` for
  `data/pdfs/`, the index and `.env`; one Vertex AI call that confirms model
  access with ADC.
- Out: the agent and tool (G02); heading-based chunks, hybrid ranking and OCR
  (P2-1); document versioning (P2-4).
- Depth: POC. Floor kept: no credentials in code or the repo; HR PDFs and the
  index are never committed. Files with no text layer are listed and excluded,
  not OCR'd.

## Acceptance

- [ ] The confirmed `google-adk` pin is recorded (working assumption 2.8.0;
      keep whatever version is actually installed and note it).
- [ ] The ingestion report lists all ~30 files, with page counts and any pages
      that have no text.
- [ ] `search("<a phrase copied from a known page>")` returns that doc and page in the top 3.
- [ ] A query with no matches returns an empty list, not an error.
- [ ] `git status` shows no PDF, index or credential file.
- [ ] One model call to `gemini-3.8-flash` succeeds through Vertex AI (authorised live, a single call).

Verification: `pytest tests/test_index.py` (offline, against two small
synthetic PDFs or text fixtures); `python ingest.py data/pdfs` locally; one
authorised live model call.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
