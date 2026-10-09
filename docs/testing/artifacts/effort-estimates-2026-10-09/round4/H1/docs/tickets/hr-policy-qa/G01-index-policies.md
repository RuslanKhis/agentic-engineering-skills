---
goal: G01
title: Index the 30 HR policy PDFs by page and prove the pinned model answers through ADC
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-memory-architecture
supporting_skills: [adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted
  hands_on: 0.5-0.75
  review_and_verify: 0.25
  total: 0.75-1
  calendar_waits: confirm PDFs may be sent to Vertex AI (ask today)
owner: You
status: ready
---

# G01 Index the 30 HR policy PDFs by page and prove model access

## Outcome

Every page of the 30 PDFs is stored as one searchable record with its document
title and page number. One live call shows that `gemini-3.8-flash` answers
through Application Default Credentials. Implements D1, D4 and D5.

## Scope

- In: `scripts/ingest_pdfs.py`, which reads `data/pdfs/*.pdf` with `pypdf`
  (proposed dependency; add it to the project's manifest, do not install it
  silently). It writes `data/index/pages.jsonl` with the fields `doc_id`,
  `title`, `page`, `text`, and a report `data/index/report.md` listing docs,
  pages, empty-text pages, duplicate or near-duplicate titles, and approximate
  tokens (characters ÷ 4). Also `.gitignore` entries for `data/` and `.env`,
  and `.env.example` containing `GOOGLE_GENAI_USE_VERTEXAI`,
  `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` and `MODEL_ID`, without
  values. Pin `google-adk==2.8.0` (working assumption) and confirm the pin
  against the release you install. Make one bounded live call to `MODEL_ID`
  (a single request, no retries in a loop).
- Out: search and the agent (G02); OCR (Later); version manifest (G06).
- Depth: POC. The floor: no key or project ID in source, and PDFs and the
  index stay out of git. The model ID is read from config, defaulting to
  `gemini-3.8-flash`.

## Acceptance

- [ ] The report shows 30 docs and the page count per doc. Every page with
      empty text is listed by name, not dropped silently.
- [ ] A tiny generated fixture PDF of 2 pages gives 2 records, with correct
      page numbers and the title taken from the file name or metadata.
- [ ] `git status` shows no file under `data/` and no `.env`.
- [ ] One live call to `gemini-3.8-flash` succeeds in the configured project
      and region, or the exact error is recorded and D4 falls back to a paid
      Gemini API key.

Verification: run `pytest tests/test_ingest.py` offline (no google.adk import),
then `python scripts/ingest_pdfs.py data/pdfs data/index` locally. The live
model call is authorised once the provider question (open decision 2) is
answered.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
