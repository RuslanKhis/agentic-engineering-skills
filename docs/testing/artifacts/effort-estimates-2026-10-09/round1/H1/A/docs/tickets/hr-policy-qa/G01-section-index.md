---
goal: G01
title: Our 30 HR policy PDFs become a searchable section index, with a report of what could not be read
design: ../../architecture/hr-policy-qa.md
plan: ../../architecture/hr-policy-qa.md#5-plan
primary_skill: adk-memory-architecture
supporting_skills: []
blocked_by: []
phase: 1
profile: proof of concept
estimate: 0.75–1.25 h
status: ready
---

# G01 Our 30 HR policy PDFs become a searchable section index, with a report of what could not be read

## Outcome

Running `python scripts/build_index.py data/policies` produces `build/index.sqlite` and `build/ingestion-report.json`. The index holds heading-to-heading sections from all 30 PDFs, with document name and page span, searchable by BM25. The report lists each page's extraction status, so an unreadable page is never mistaken for "no policy". Implements D2 and the kept layout of D6.

## Scope

- In: project skeleton (`pyproject.toml` pinning Python ≥3.12, `pypdf` and `google-adk==2.8.0` as the working ADK assumption, `.gitignore` for `.env`, `data/` and `build/`); `hr_index/ingest.py` (PDF → page records → sections via a heading regex adapted to these documents → skip contents and cover pages); `hr_index/search.py` (`search(conn, query, k)` → sections with `document`, `heading`, `pages`, `text`); `scripts/build_index.py`; offline tests on a two-document synthetic fixture. Adapt `chunk_by_heading`, `screen_units`, `build_index` and `search_lexical` from the specialist's `scripts/local_retrieval.py`. That script needs Python 3.12+.
- Out: the agent and tool wrapper (G02), embeddings or hybrid search (later), OCR of scanned pages (later), versioned document releases (G06).
- Depth: build at POC depth. Keep the floor: no policy PDFs or index committed to git. Left for later: document version approval (G06), audience entitlements (later list).

## Acceptance

- [ ] All 30 PDFs are indexed. The report shows per-document page counts and lists every `image_only` or `low_density` page.
- [ ] A test query for a known heading in the synthetic fixture returns that section first, with the correct page span. A query with no matching terms returns an empty list, not the nearest unrelated section.
- [ ] Contents-page entries are screened out: a query matching only a table-of-contents line does not return the contents page as a hit.
- [ ] `git status` shows no file under `data/` or `build/`.
- [ ] The `google-adk` pin is recorded in `pyproject.toml`. Whether 2.8.0 or a newer release was chosen is recorded in Evidence.

Verification: offline. `pytest tests/test_index.py` (no ADK import), then `python scripts/build_index.py data/policies` on the real PDFs, plus a manual look at the report summary.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-section-index.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
