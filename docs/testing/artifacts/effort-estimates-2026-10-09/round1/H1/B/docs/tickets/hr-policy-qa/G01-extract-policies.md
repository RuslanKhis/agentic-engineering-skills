---
goal: G01
title: The 30 HR policy PDFs are extracted to page-level text with a catalogue
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-memory-architecture
supporting_skills: []
blocked_by: []
phase: 1
profile: proof of concept
estimate:
  hands_on: 0.25-0.5
  review_and_verify: 0.25-0.5
  total: 0.5-1.0
  calendar_waits: none
owner: builder
status: ready
---

# G01 The 30 HR policy PDFs are extracted to page-level text with a catalogue

## Outcome

The extracted text of every policy is stored locally with page numbers, along with
a catalogue that the agent can read. The report shows which pages cannot be read.
Implements D2 and D3.

## Scope

- In: proposed `hr_policy_agent/ingest.py`, a CLI that reads `data/pdfs/*.pdf`
  and uses `pypdf` (the user installs it). It writes the following:
  - `data/pages/<doc_id>.json`: a list of `{page, text}` entries. `doc_id` is a slug
    of the file name.
  - `data/catalogue.json`: entries of `{doc_id, title, pages, chars,
    est_tokens}`. The title comes from the PDF metadata or the first heading,
    and falls back to the file name.
  - `data/extraction_report.md`: per-document counts, pages with no text, and
    the total estimated tokens.
- In: offline tests in `tests/test_ingest.py`. They use two small PDFs generated
  in the test or fixture text pages, not the real policies.
- Out: OCR of scanned pages (P2-4), chunking and search index (P2-1).
- Depth: POC. Output is deterministic. A broken PDF is listed in the report and
  does not stop the run. Floor: the real PDFs stay in `data/`, which is
  git-ignored. Do not commit them.

## Acceptance

- [ ] Running it on the real folder lists all 30 documents in the catalogue,
  with page counts that match a PDF viewer for 3 documents the user spot-checks.
- [ ] A PDF with an image-only page has that page in the report's "no text"
  list, with an empty `text`. It is not silently dropped.
- [ ] A corrupt PDF is reported as failed, and the other documents are still
  written.
- [ ] Running it a second time gives byte-identical output files.
- [ ] `data/` is in `.gitignore`. `git status` shows no PDF or extracted text.

Verification: offline `pytest tests/test_ingest.py`, then a local run on the real
folder: `python -m hr_policy_agent.ingest data/pdfs data/`. The user reads
the report and records the total estimated tokens and any empty pages (O3).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
