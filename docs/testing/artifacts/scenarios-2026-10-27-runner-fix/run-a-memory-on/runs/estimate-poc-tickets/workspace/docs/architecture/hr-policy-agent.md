# HR policy Q&A agent: proof-of-concept design and plan

Status: **draft**, 2026-10-27. Every row marked *assumed* is provisional until the builder confirms it. This one file holds design and plan (compact form); tickets are in `docs/tickets/hr-policy-agent/`.

**Summary.** Profile: proof of concept, kept form (corpus path and model ID live in config so phase 2 builds on it). Phase 1 delivers a local ADK agent that answers questions about about 30 HR policy PDFs with document-and-page citations and refuses when the policies do not say, shown through `adk web` at the Friday 2026-10-30 demo. Phase 1 needs 3.0–4.5 h of the 6 h available; the 1.5 h reserve is untouched, so there is no slack beyond it. Largest risks: scanned PDFs with no text (OCR is out of scope), weak keyword matching on synonyms, and a developer new to ADK running the high end. Decisions needed from the builder: Q1–Q3 below, on day 1.

## 1. Constraints and profile

| Scope-gate question | Answer | Depends on it |
| --- | --- | --- |
| Deadline, afterwards | Demo to HR leadership Fri 2026-10-30; continued if it lands (*assumed*) | Phase 1 cut line, kept form |
| Builder | One developer, 6 h over Wed 28 and Thu 29 Oct, counted as focused hours; new to ADK (*assumed*), so ×1.5 is folded into G02 and G03 | Capacity, G02/G03 estimates |
| Money | Small; user-set model-spend cap, *assumed* USD 10 (Q4) | C4, G02 |
| Judge | HR leadership watching a live screen-share of `adk web` on the builder's laptop | G04, answer style |
| Interface | `adk web` on loopback only; no URL, not handed over (default) | Identity deferred |
| Data and effects | About 30 internal HR policy PDFs, no employee records; read only, nothing written or sent | Floor, C2 |
| Reviews | Friday demo is the go-ahead for phase 2 (G04); production-decision and results reviews belong to later phases | Phase 2 |
| Contract / lock-in | No statement of work; no lock-in concern (defaults) | No SOW or portability goal |

Open questions, with the assumption proceeded on:

- **Q1** Are the PDFs text-based or scans? *Assumed* text-based; G01's coverage report tells, and scanned files are left out of the demo (OCR deferred).
- **Q2** May policy text be sent to the model provider? *Assumed* yes under the builder's own approved access; confirm before G02's first live call. If no, demo on the documents that are cleared.
- **Q3** Which model access exists (AI Studio key or a Vertex project)? *Assumed* a working key in the environment and no new cloud resources. The model ID is chosen in G02 from the dated lifecycle table in `adk-model-and-output-contracts`, not from memory.
- **Q4** What is the spend cap, and where is it set? *Assumed* USD 10 as a quota or budget cap on the model project, set by the builder in G02 (a quota stops calls; an alert only warns).
- **Q5** Do the policies differ by country or entity? *Assumed* one set; the manifest carries an optional `scope` column shown in citations, with no filtering logic.

## 2. Journey and shape

An HR leader types "How much parental leave do new fathers get?". Today they open several PDFs and search by hand. The agent searches the policies, answers in two or three sentences, and cites `Parental Leave Policy, p.4`; for a question the policies do not cover it says so and suggests contacting HR.

The model decides how to phrase the search (up to three phrasings per call, to cover synonyms) and how to compose or refuse. Code controls the corpus, the index, the call cap and the checking of citations.

```text
PDFs -> ingest (per page, pypdf) -> SQLite FTS5 index + manifest + coverage report
question -> adk web -> LlmAgent -> search_policies(queries) -> passages {doc, page, text} -> cited answer
```

## 3. Contracts and decisions

| ID | Contract (invariant, scope) | Enforced where | Check |
| --- | --- | --- | --- |
| C1 | Every policy statement in an answer cites a document and page returned by search in that turn; with no supporting passage the agent says it cannot find it and does not guess. All questions. | Instruction plus tool output shape; verified after the fact by the G03 runner. A runtime guard is deferred (P2-2), so the model alone enforces it in the demo: accepted risk, owner builder, ends at P2-2. | G03 A1, A2; G01 A3 |
| C2 | Answers use only the ingested approved PDFs; the agent has one read-only tool and no web, file or write access. | Tool list in the agent definition; ingest reads only the configured folder | G02 A3 |
| C3 | Every PDF in the folder is in the manifest with page and text-page counts; a PDF with textless pages fails the build unless listed in an exclusions file. | Ingest exit status | G01 A1, A2 |
| C4 | Floor: model ID pinned, no secrets in source, spend capped, call cap in scripted runs. | Config, quota on the model project, `RunConfig.max_llm_calls` | G02 A4, A5; G03 A3 |

| ID | Decision (requirement, contract, choice, tradeoff, check) |
| --- | --- |
| D1 | Retrieval over 30 PDFs, C1/C2: local SQLite FTS5 (BM25), no managed RAG, no embeddings. Costs nothing idle, so no teardown goal. Tradeoff: misses synonyms ("holiday" vs "annual leave"); the tool takes up to three phrasings. Check G01 A3, G03 A1. Hybrid embeddings are P2-1. |
| D2 | Chunk = one page, C1: page numbers become exact citations. Tradeoff: tables crossing pages split. |
| D3 | One `LlmAgent` with one tool, no sub-agents, C2: nothing here needs a second context or tool set. |
| D4 | Scans fail loudly, C3: a silent empty page would look like "the policy says nothing". OCR deferred. |
| D5 | Answer style, C1: short, cited, no legal advice, "not in the policies" plus an HR contact placeholder when unsupported. Check G03 A2. |
| D6 | Evaluation, C1: 8–10 gold questions and 3 out-of-scope ones, labelled by the builder from the PDFs, run through the ADK Runner into a table the builder reads, with a deterministic check that the cited doc and page match. HR-expert labelling is P2-1. |

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Identity, per-user scope | Defer (loopback, builder only) | Any URL or colleague access (P2-3) |
| Secrets | Minimal: environment variable, `.env` untracked | Any hosting |
| Spend and loops | Minimal (C4) | Other people running it |
| Prompt injection | Minimal: read-only, no write tool | Any write tool or untrusted documents |
| Sensitive data | Defer: policies only | Questions about named people or cases |
| Observability, hosting, CI | Defer: console logs, local | Staff use; P2-3 |
| Release engineering | Minimal: pinned model ID | P2-1 |

Graduation conditions (to reach colleagues or real cases): SME-labelled evaluation set, runtime citation guard, sign-in and hosting, scan handling, document refresh and version dates, a governance note if people type personal cases.

## 5. Plan

Estimates are human hours, agent-assisted, hands-on plus review, in quarter hours. No calendar waits. Added by hand (one person).

| Goal | Outcome | Contracts | Hours (hands-on + review) | Primary skill |
| --- | --- | --- | --- | --- |
| G01 | Ingest and search over the PDFs, with coverage report | C2, C3, C1 | 0.75–1.25 (0.5–0.75 + 0.25–0.5) | `adk-memory-architecture` |
| G02 | Agent with the search tool runs in `adk web`, pinned model, spend cap | C1, C2, C4 | 1.25–1.75 (0.5–0.75 + 0.75–1.0) | `adk-engineer` |
| G03 | Gold questions run through the Runner into a review table | C1, C4 | 0.5–0.75 (0.25–0.5 + 0.25) | `adk-agent-evaluation` |
| G04 | Demo script, fallback and one rehearsal | none | 0.5–0.75 (0.25–0.5 + 0.25) | `adk-presenter` |

Ticket files hold each goal's scope and acceptance. **Resources created:** none, so there is no teardown goal.

**Capacity.** Sum 3.0–4.5 h against 6 h less a 25% reserve (1.5 h) = 4.5 h: fits at the high end with nothing to spare. Calendar: Wed 28 Oct G01 then G02 (2.0–3.0 h); Thu 29 Oct G03 then G04 (1.0–1.5 h), leaving the rest for overruns; Fri 30 Oct demo. The days are assumed.

**Cut line.** If time runs out, goals stay useful in the order G01, G02, G04, G03: shrink G03 to five questions read by eye before touching G04's fallback.

**Phase 2** (if the demo lands; tickets not written):

- P2-1 SME-labelled evaluation set with agreement check, and hybrid embedding retrieval if recall is weak. `adk-agent-evaluation`, 4–8 h. Accept: SME-labelled set of 30+ with a recorded recall figure.
- P2-2 Runtime citation guard. `adk-engineer`, 1–2 h. Accept: an answer citing a passage not retrieved in that turn is replaced by a refusal.
- P2-3 Cloud Run behind sign-in for HR staff. `deploy-adk-on-google-cloud`, 6–10 h plus organisation waits. Accept: unauthenticated request is refused.
- P2-4 Scan handling (OCR or vision triage). `adk-memory-architecture`, 2–4 h. Accept: previously excluded scans are searchable.
- P2-5 Presentation for the production decision. `adk-presenter`, 3–6 h plus the review date.

**Later:** observability and cost tracking (trigger: staff use); CI evaluation gate (trigger: second contributor or model change); document refresh and effective dates (trigger: first policy update); per-country scoping (trigger: Q5 is no).

## 6. Open decisions and next prompt

Open: Q1–Q5 above, each with an owner (the builder) and a day-1 deadline. G02 does not start live calls before Q2 and Q4 are answered. Not independently reviewed (single-person PoC).

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01.md
```
