---
goal: G01
title: The 30 HR policy PDFs become a page-tagged local corpus with a catalogue
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md
primary_skill: adk-memory-architecture
supporting_skills: []
blocked_by: []
phase: 1
profile: proof of concept
estimate:                # human hours, agent-assisted, x1.5 new-to-ADK included
  hands_on: 0.3-0.5
  review_and_verify: 0.2-0.3
  total: 0.5-0.8
  calendar_waits: none
owner: Builder
status: ready
---

# G01 The 30 HR policy PDFs become a page-tagged local corpus with a catalogue

## Outcome

Every policy PDF is available to the agent as text per page, with a catalogue
of id, title and page count, and the builder can see which pages did not extract.
Implements D1, D5 (data side) and D6 (pins).

## Scope

- In: `pyproject.toml` pinning `google-adk==2.8.0` (confirm the pin) and a PDF
  text library (e.g. `pypdf`, pinned); `scripts/extract.py` reading `data/pdfs/`
  and writing `data/corpus/<doc_id>.json` (pages: number, text, chars),
  `data/corpus/catalogue.json` (doc_id, title from metadata or first heading,
  file name, page count, readable) and `data/corpus/extraction_report.md`
  (empty or failed pages per document); `.gitignore` for `data/pdfs/`, `data/corpus/` and `.env`;
  offline tests on two small generated PDFs.
- Out: the agent and tools (G02), OCR for scanned pages (open decision O2),
  managed retrieval (G07).
- Depth: POC. Floor kept: policy PDFs stay local and are not committed; no
  personal data. Corpus versioning and owners are deferred to G07.

## Acceptance

- [ ] Running the script on the real folder lists 30 documents in the catalogue
      and each page count equals the PDF's page count.
- [ ] A page with no extractable text appears in the report and as an empty
      page, not silently dropped; a document with no text is marked unreadable.
- [ ] No PDF or extracted text is tracked by git (`git status` is clean of `data/`).

Verification: offline, `pytest tests/test_extract.py` on generated fixtures, then
one local run on the real PDFs and a read of `extraction_report.md`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-corpus.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
