# HR policy Q&A agent: proof of concept design and plan

Status: **draft**. The user was not available, so every scope answer below is
assumed and every decision that depends on one is provisional (marked *prov.*).
Design and plan share this file (compact form for a POC).

## 1. Constraints and profile

| Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- |
| Deadline, and continued after? | Demo to HR leadership Friday **2026-10-16** (today, 2026-10-09, is itself a Friday). Continued if the demo lands, so phase 1 code is kept. | Phase 1 size; config over hard-coding (D6) |
| Who builds? | One developer, ~6 h over two days in two ~3 h blocks; **new to ADK**, has a Google account and a GCP project. | Capacity, ×1.5 estimate multiplier |
| Money? | Small allowance (≤ ~USD 20 for model calls over the week). | Flash-class model (D4), no managed search service |
| Who judges, reading what? | HR leadership watching a live demo the builder drives, plus a short results table. | `adk web` as the frontend (D5), gold-question table (G03) |
| Data and effects? | ~30 internal HR policy PDFs (internal, not personal data). Read only: the agent changes nothing and sends nothing. | Floor and security depth; model endpoint (D4) |
| Model endpoint approved for internal documents? | Vertex AI in a company GCP project the builder already has access to (ADC login). | D4; blocks G01 if false |

**Profile: proof of concept**: one builder, a demo audience, read-only access
to internal documents, kept code. The data and the effects set the floor; the
label does not lower it.

## 2. Journey and shape

An employee today searches a shared drive or emails HR to learn, for example,
"how many days of parental leave do I get after six months' service?". In the
demo the builder types that question into `adk web`. The agent searches a local
index of the 30 PDFs and answers in two or three sentences, citing document
and page. When the corpus doesn't cover the question, it says so and refers the
user to HR instead of guessing.

The model decides what to search and how to phrase the answer. Code owns PDF
extraction, the index, how many passages come back, the call cap and the model ID.

```
adk web ─► LlmAgent (gemini-3.8-flash) ─► search_policies(query) ─► SQLite FTS5 index ◄─ ingest.py ◄─ 30 PDFs
```

## 3. Decisions

| # | Requirement → choice → reason | Tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Grounded answers on 30 PDFs in about 1 h of build time → **local SQLite FTS5 (BM25) index of page-level passages**, built by a script, reusing `adk-memory-architecture`'s local retrieval approach | Lexical search misses synonyms that embeddings would catch; page chunks can split a clause. Rejected alternatives: Vertex AI Search/RAG Engine (setup and IAM time) and putting the whole corpus in context (cost and latency per question at an unknown corpus size) | G03: expected document in the top 5 for ≥ 5 of 6 gold questions |
| D2 | Citable, refusable answers → **one agent, one read-only tool** returning ≤ 5 passages `{doc, page, text ≤ 1,500 chars}` and a `status`; the instruction requires a doc+page citation per claim and a fixed "not found, contact HR" reply | A prompt rule, not a code check, enforces citations during the demo | G03 code check: every cited (doc, page) was among the retrieved passages |
| D3 | Prompt injection and agency → **no write or egress tools**, so the agent never holds untrusted content and a write path together | No follow-up actions (e.g. raising a ticket) | Tool list in G02 test equals `[search_policies]` |
| D4 | Internal documents go only to an approved endpoint; behaviour stable all week → **Vertex AI, `gemini-3.8-flash` pinned** (stable, no shutdown or Vertex retirement listed in `model-lifecycle-2026-10-01.json`, checked 2026-10-08) *prov.* | Newest stable rather than longest-proven; Flash rather than Pro | G01 confirms access with one call; G02 test asserts the model ID |
| D5 | Demo with minimal UI work → **`adk web`, run locally** by the builder | Not shareable; no login (single user) | Rehearsal on day 2 |
| D6 | Kept code → model ID, index path and call cap in one `config.py`; ADK pinned at **google-adk 2.8.0** *prov.* (the specialists' checked baseline) | A few minutes more than hard-coding | G01 acceptance: pin confirmed |

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Secrets | Minimal: ADC credentials, nothing in code, prompts or the repo; PDFs and index git-ignored | Any shared deployment |
| Spend stop | Minimal: a `before_model_callback` ends a turn after 6 model calls (works under `adk web`, which owns the Runner), plus `RunConfig(max_llm_calls=6)` in the G03 script and a USD 20 budget alert on the project (an alert, not a cap) | Anyone other than the builder uses it |
| External effects | None exist (D3) | Any write tool |
| Sensitive data | Defer: policy text only; demo questions are invented, never about real employees | Real employee questions |
| Identity | Defer: single local user | More users (phase 2) |
| Core judgment, measured | Build: 6 gold questions (G03) | — |
| Observability, release, tuning | Defer: console logs; pinned model and ADK only | Shared deployment |

Accepted risk (owner: the builder, ends at phase 2): an answer can be wrong
despite citing a page. The demo says "POC, check the cited page" and is
rehearsed on the gold questions.

**Graduation conditions** (become phase 2): employee SSO before anyone else
uses it; HR owns which document versions are published; ≥ 30 labelled
questions with a measured score; no question text in logs.

Failure paths worth naming: a question outside the corpus gets the fixed
"not found" reply, not a broadened guess. A scanned PDF with no text layer is
listed by G01's ingestion report and excluded, and the demo says so. Model
unavailable or 429 on demo day: `adk web` shows the error, and the builder
falls back to G03's recorded results table.

## 5. Plan

Estimates are human hours (hands-on + review/verify), agent-assisted, with a
**×1.5 new-to-ADK multiplier already applied** to every figure. The goal entries
below are the only source of the numbers.

**G01 Index the HR PDFs.** Project skeleton (google-adk pin confirmed, config,
`.gitignore`); `ingest.py` extracts text per page, writes an ingestion report
(pages, characters, no-text pages) and builds the FTS5 index; one Vertex call
confirms model access. Estimate 0.75–1 + 0.25–0.5 = **1–1.5 h**; waits: none
assumed (see O1). Primary `adk-memory-architecture`. Acceptance: report lists all
30 files; a known phrase query returns its page; no PDF or index is tracked by git.
Run: `/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md.`

**G02 Ask a question in adk web and get a cited answer.** `LlmAgent` + `search_policies`
+ instruction + call-cap callback (D2–D6). Estimate 0.5–0.75 + 0.5–0.75 = **1–1.5 h**.
Primary `adk-memory-architecture`; supporting `adk-tool-interface-design`,
`adk-agent-instructions`, `adk-model-and-output-contracts`, `adk-operational-guardrails`.
Needs G01. Acceptance: offline tests for the tool (hit, empty, oversize) and the
cap; a live question in `adk web` returns a doc+page citation, and an
off-corpus question gets the "not found" reply.
Run: `/adk-engineer Carry out docs/tickets/hr-policy-qa/G02-cited-answer-in-adk-web.md.`

**G03 Measure six gold questions and prepare the demo.** The builder writes 6
questions with expected doc/page (5 answerable, 1 off-corpus); a script runs
them through `Runner` and writes a Markdown table (retrieval hit, citations
valid, answer by eye); a demo script. Estimate 0.5–0.75 + 0.25 = **0.75–1 h**.
Primary `adk-agent-evaluation`. Needs G02. Acceptance: table generated; ≥ 5/6
retrieval hits, or the misses written up as known limits.
Run: `/adk-engineer Carry out docs/tickets/hr-policy-qa/G03-gold-questions-and-demo.md.`

**Capacity and cut line.** 6 h × 0.8 focus = 4.8 h, less a 25 % reserve (1.2 h
for setup surprises and rehearsal) = **3.6 h for goals**. Phase 1 = G01–G03 =
**2.75–4.0 h**. The low end fits with 0.85 h spare; the high end is 0.4 h over.
**If G01 + G02 take more than 2.75 h, G03 shrinks to 4 questions checked by
eye in `adk web`, and the scripted table moves to phase 2.** If time runs out,
the useful order is G01 → G02 (a demonstrable agent), then G03 (evidence). Path: G01 → G02 → G03,
one person, all sequential: day 1 G01 + G02, day 2 G03 + rehearsal.

**Phase 2: graduate to an internal tool (if the demo lands).**
- P2-1 Heading-based chunks and hybrid ranking; OCR route for scanned PDFs. `adk-memory-architecture`, 3–6 h. Check: recall on the gold set does not drop.
- P2-2 30–50 HR-labelled questions with a scored runner. `adk-agent-evaluation`, 4–8 h (mostly HR's labelling). Check: score reported per release.
- P2-3 Cloud Run behind IAP with Workspace SSO. `deploy-adk-on-google-cloud`, supporting `adk-agent-observability` and `adk-release-engineering`, 5–9 h plus an IAM wait. Check: a non-allowlisted account is denied.
- P2-4 HR-owned document release (versions, superseded policies). `adk-memory-architecture`, 2–4 h. Check: a withdrawn policy is never cited.

**Later:** a per-user budget (trigger: more than about 20 users); content-free
structured logs and traces (trigger: first shared deployment); a managed search
service (trigger: corpus over about 500 documents or measured recall too low);
an employee-specific answer path (trigger: questions needing personal records,
which brings a full identity and data-protection design).

## 6. Open decisions

- **O1** Is Vertex AI in the builder's project approved for HR documents? If not,
  find out which endpoint is before G01 (this may be a calendar wait).
- **O2** Do any of the PDFs need OCR? G01's report settles it; affected files are excluded in phase 1.
- **O3** Are superseded policy versions among the 30? The builder removes them by hand for the POC.
- **O4** Confirm the cut line above, or move it.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
