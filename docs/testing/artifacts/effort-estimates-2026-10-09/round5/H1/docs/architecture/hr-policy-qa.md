# HR policy Q&A agent: proof-of-concept design and plan

**Status: draft.** The user was unavailable, so every answer below is assumed and the decisions that depend on them are provisional (marked *prov.*). Design only; nothing is implemented.

## 1. Constraints and profile

| Scope gate | Answer (A = assumed) | What depends on it |
| --- | --- | --- |
| Deadline / afterwards | Demo to HR leadership on Friday (given). Continued if it lands (A) | Phase 1 code is kept, not throwaway |
| Builder | One person, about 6 hours over two days (given); new to ADK, has used Python (A) | 1.5× multiplier on every estimate |
| Budget | Small allowance on a company-billed, paid-tier Gemini API key (A) | Model tier; free-tier key ruled out (D5) |
| Judge | HR leadership watching a live demo, asking their own questions (A) | Citations and honest "not covered" matter more than UI |
| Data / effects | ~30 published HR policy PDFs, internal but not personal; read-only, no writes or messages (A) | Floor is light: no write path, no PII |

**Profile: proof of concept**: one builder, a demo audience, published internal documents, read-only. Correct this line if any row is wrong.

## 2. Journey and shape

An HR leader asks "How many days of parental leave does a part-time employee get?" Today someone opens several PDFs or emails HR. In the demo the agent answers in a few sentences, cites document and page, and says plainly when the policies do not cover the question.

The model decides which policies to read and writes the answer. Code owns PDF extraction, the document catalogue, page bounds, the model ID and the call cap.

```
PDFs ─(offline script)→ corpus.json + catalogue + ingestion report
adk web → LlmAgent(pinned model, catalogue in instruction)
            └─ read_policy(doc_id, first_page, last_page) → bounded page text
```

## 3. Decisions

| ID | Requirement → choice | Tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Answers grounded in ~30 PDFs within hours → **one `LlmAgent` with one read-only tool**; no sub-agents | No routing or reviewer stage | Agent module defines one agent, one tool |
| D2 *prov.* | Find the right policy without building an index → **catalogue in the instruction** (doc ID, title, headings with page numbers, from extraction); `read_policy` returns at most N pages of a named document | Relies on the model choosing documents from titles and headings; weak for cross-document exceptions. Alternative: SQLite FTS5 search (phase 2, G05) | Gold questions (G03) score document hits; misses trigger G05 |
| D3 | Leadership must trust answers → **cite `[doc_id p.N]` for every claim; when nothing relevant is read, say so and point to HR** | Prose contract, not schema-enforced | G03 includes two not-covered questions; a fabricated answer fails |
| D4 | Scanned pages silently missing would give wrong "not covered" → **run the ingestion qualification report** (adk-memory-architecture `qualify_ingestion.py`); `image_only`/`low_density` pages are listed in the catalogue as "not read" | OCR deferred (Later) | Report saved beside the corpus; count of unread pages known before the demo |
| D5 *prov.* | Demo behaves like rehearsal; internal documents not used for training → **pin `gemini-3.8-flash`** (stable, no shutdown announced per lifecycle table checked 2026-10-08) **on a paid-tier key** | Paid key needs company billing; Vertex AI would need a GCP project (≈ a day for a new GCP user) | `model=` literal in code; key in `.env`, which is git-ignored |
| D6 | Spend stop when the demo runs through `adk web`, where we do not own `RunConfig` → **budget alert and quota cap on the key's project**; tool result bounded by page count | Alert observes, the quota enforces | Screenshot of the cap; a test asserts a page-range request beyond N is truncated |

ADK version: none installed. Working assumption **google-adk 2.8.0** (specialists' `references/compatibility.md`); G02 confirms it against the chosen pin.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core answer, measured | Build: 10 gold questions checked by hand | Any wider audience → evaluation set (G04) |
| Secrets | Minimal: key in `.env`, never in code, prompts or the repo | Hosting → Secret Manager (G06) |
| Writes / effects | None exist | Any tool that writes or sends → `adk-agent-security` review |
| Prompt injection | Minimal: agent reads company-authored PDFs and has no write or egress tool, so the trifecta is broken | User-uploaded documents or a write tool |
| Sensitive data | Defer: policies only, no employee records | Any employee-specific data |
| Identity / access | Defer: single local user | Anyone else uses it → Cloud Run behind IAP (G06) |
| Budgets | Minimal: quota cap + bounded tool result | Shared use → app-owned `max_llm_calls` |
| Frontend | `adk web` | Employees use it |
| Observability, release, tuning | Defer: console logs, pinned model | Shared deployment |

**Graduation conditions** (become phase 2): measured accuracy on a larger set; employees signing in with their own identity; a hosted service with secrets in Secret Manager; an owner who approves which policy versions are loaded.

## 5. Plan

Estimates are human hours (hands-on + review/verify) with a coding agent, already multiplied by 1.5 for a first ADK project. No calendar waits, provided a paid key exists (Q4).

**G01: Extract and qualify the policy corpus.** 0.5–0.75 h. Script turns `data/policies/*.pdf` into page records, the ingestion report and a catalogue. Primary `adk-memory-architecture`. Acceptance: 30 documents in the catalogue; unread pages listed; re-run gives identical output. *Ticket:* `docs/tickets/hr-policy-qa/G01.md`.

**G02: Agent answers with citations in `adk web`.** 1.75–3.25 h (includes ~0.5–1 h first-time key and environment setup). D1–D3, D5, D6. Primary `adk-tool-interface-design`; supporting `adk-agent-instructions`, `adk-model-and-output-contracts`. Acceptance: three sample questions answered with valid citations; not-covered question declined; offline tests for `read_policy` bounds and unknown IDs; ADK pin confirmed. Needs G01. *Ticket:* `G02.md`.

**G03: Check ten gold questions and rehearse the demo.** 0.75–1.25 h. Builder writes 10 questions with answers from the PDFs (incl. 2 not-covered, 1 cross-document exception), records results in a table, sets the quota cap, picks 5 demo questions, does one dry run. Primary `adk-agent-evaluation`. Needs G02. *Ticket:* `G03.md`.

**Capacity.** 6 h × 0.8 (two dedicated blocks) = 4.8 h; 25 % reserve leaves 3.6 h for goals. Phase 1 sums (by hand) to **3.0–5.25 h**. **Only the low end fits.** If G02 runs high, G03 shrinks to the five demo questions plus the dry run, and the other five gold questions move to G04. Useful order if time runs out: G01 → G02 → dry run.

**Cut line:** ships Friday: G01–G03. Phase 2 (if the demo lands):

- **G04** Evaluation set of 30–50 HR-labelled questions with a runner. `adk-agent-evaluation`, 6–12 h. Accept: scored table, failures diagnosed (query miss, empty extraction).
- **G05** Local FTS5 search tool replacing catalogue selection when G03/G04 show document misses. `adk-memory-architecture`, 4.5–9 h. Accept: document-hit rate on G04 ≥ catalogue baseline.
- **G06** Cloud Run behind IAP with Secret Manager for named HR staff. `deploy-adk-on-google-cloud`, 4.5–9 h + a GCP project day. Accept: unauthenticated request rejected.

**Later:** OCR of scanned pages (trigger: report shows relevant unread pages); policy-version publication workflow (trigger: policies change monthly); CI evaluation gate (trigger: second contributor); traces and cost dashboard (trigger: shared use).

## 6. Open decisions and next prompt

1. Paid-tier Gemini API key vs. Vertex AI in a company project (D5); confirm internal documents may be sent to the chosen service.
2. Model `gemini-3.8-flash`; confirm against the live models page on the day.
3. Accept the cut line above, or move G03's gold questions to phase 2.
4. Do any PDFs contain employee personal data? If yes, remove them or raise sensitive-data depth.

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
