# HR policy agent: proof-of-concept design and plan

**Status: draft.** Written in a non-interactive session: nobody answered the scope-gate questions, so every answer below is an assumption and every decision resting on one is provisional. Correct the table and the plan follows.

**Profile (one line):** proof of concept, kept (not throwaway) code, judged live by HR leadership on Friday 2026-10-30.

## 1. Constraints and profile

| Question | Assumed answer | What depends on it |
| --- | --- | --- |
| When, and continued after? | First version by Thursday evening for the Friday demo; continued only if HR leadership says go | Phase 1 cut line; phase 2 is written but not scheduled |
| Who builds, hours, familiarity? | One developer, about 6 focused hours over Wed 28 and Thu 29 Oct, new to ADK | ×1.5 on implementation goals; no focus-factor discount (see capacity) |
| Money? | Small allowance; the developer sets a hard spend cap of their own choosing on the model key or project before G02 | Floor spend stop (C5) |
| Who judges, reads what? | HR leadership watching a live session in `adk web`; no slide deck | G03 includes a run-of-show instead of a deck |
| Web interface, reach? | `adk web` on loopback on the developer's machine only; not handed over | No identity, no hosting, no frontend goal |
| Data and effects? | The 30 PDFs are approved, internal, contain no employee personal data and may be sent to the model API. Agent is read-only | Personal data and write controls deferred; floor holds |
| Reviews needing a presentation? | The Friday demo only. A production go/no-go review follows if they say yes | No presentation goal in capacity; `adk-presenter` is not installed here |
| Client contract or lock-in concern? | No / No | No SOW, no portability goal |
| Model and runtime? | Gemini through an API key from the developer's environment, no GCP project. Model ID pinned in G02 from the dated lifecycle table in `adk-model-and-output-contracts`, which is not installed in this workspace, so **unchecked**. ADK version working assumption 2.8.0 (the baseline in `adk-memory-architecture`); G01 confirms against the actual pin | G01 and G02 acceptance |
| Documents? | One current version of each policy, text-based PDFs, a few possibly scanned; folder `data/pdfs/` | G01 coverage report decides how many scans exist |

**Questions I would have asked:** (1) Are any PDFs scanned images, and how many pages in total? (2) May the PDFs go to a hosted model? (3) Can one HR person give 5 to 10 real questions with the policy page that answers each, by Thursday morning? (4) Is Gemini acceptable, or must it be another provider? (5) Are the six hours focused, or interrupted time?

## 2. Journey and shape

An HR leader asks "How many days of bereavement leave do I get for an aunt?" Today they open several PDFs and search by hand. The agent searches the policy pages, answers in plain words with `[Document title, p. N]` citations, and says so plainly when the policies do not cover the question.

One `LlmAgent` with one tool, `search_policies(query)`, over a local page index. No sub-agents: there is no distinct responsibility, tool set or evaluation reason for a second. The model decides what to search for (it may issue up to a few differently worded queries) and how to phrase the answer. Code decides what exists in the corpus, what a "match" is, how many searches a turn may use and which sources are citable.

Ingestion is a separate offline script: PDFs → per-page text → `data/index/pages.jsonl` (doc id, title, page, text) plus a coverage report. Retrieval is lexical (BM25-style, pure Python) over pages. 30 documents do not justify a vector database, a managed RAG service, or anything that charges while idle. Tradeoff: lexical search misses pure paraphrase ("time off" versus "annual leave"); mitigated by the model issuing several wordings, and measured by G03. Embeddings are the phase 2 answer if G03 shows misses.

## 3. Contracts and decisions

| ID | Invariant (scope: every answer, builder and demo audience) | Enforcement | Check |
| --- | --- | --- | --- |
| C1 | A policy claim in an answer cites a document and page that `search_policies` returned in the same turn | Tool returns doc id, title and page with each passage; instruction requires citing them. Runtime check deferred: trigger is any user beyond builder and demo | G03 eval fails any citation not in the turn's returned set |
| C2 | If no passage clears the match threshold the agent says the policies do not cover it and refers to HR; it never answers from general knowledge | Tool returns `status: no_match` computed in code; instruction forbids answering on it | G02 out-of-scope questions; G03 |
| C3 | No PDF is silently dropped: every page's extraction result, including empty ones, is in the index and the coverage report | Ingestion exits non-zero on an unreadable PDF; empty pages recorded with `text=""`; scanned pages are listed, not guessed at | G01 test and report |
| C4 | The agent is read-only and policy-only: one search tool, no employee records; a question about someone's own case gets general policy plus a referral | Tool set is exactly `search_policies`; instruction | G02 test on `tools`; G03 case |
| C5 | Spend is bounded: at most 4 searches per user turn, model ID pinned, a key-level spend cap set by the developer | `before_tool_callback` counts searches in state and returns an error result past the limit; cap is outside the code (`adk web` owns the Runner, so `max_llm_calls` is not ours to set) | G02 callback test; developer confirms the cap |

Decisions (all provisional on section 1):

- **D1 (C3):** Per-page extraction with a library chosen in G01 (`pypdf` first; swap only if the report shows poor text). *Tradeoff:* no OCR, so scans are reported rather than read; OCR waits for the trigger below. Check: coverage report.
- **D2 (C1, C2):** Local BM25 over pages, not embeddings or a hosted index. *Tradeoff:* paraphrase misses. Check: G03 recall on gold questions.
- **D3 (C1):** Page is the evidence unit; the tool returns top 5 pages with a trimmed snippet and the full page text. *Tradeoff:* a clause continued on the next page can be cut; G03 includes two such questions.
- **D4 (C5):** Searches per turn capped in a callback, not in the prompt. Check: callback test.
- **D5 (C4):** One agent, one tool, in-memory sessions. Check: tool-list test.
- **D6:** Gold set is developer-written, HR-verified only if question (3) is answered; the demo says which.

## 4. Floor, depth and deferred

Floor, kept: no secrets in source, prompts or logs (key from environment, `.env` ignored); spend stop (C5); model ID pinned; nothing reachable by URL (`adk web` on loopback only); nothing written or sent; no personal data.

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Core judgment, measured | Build: 10–12 gold questions + 3 out-of-scope | HR supplies real questions |
| Identity, per-user scope | Defer (builder-only) | Anyone but the builder reaches it |
| Runtime citation check | Defer (eval only) | Any user beyond the demo |
| OCR for scanned pages | Defer | G01 report shows scans in more than a few documents |
| Embeddings / hybrid retrieval | Defer | G03 shows paraphrase misses |
| Hosting, observability, CI gates | Defer | Colleagues use it daily |
| Document versions and effective dates | Defer | Policies are revised or superseded copies exist |

**Graduation conditions** (before more users or real HR cases): sign-in and allowlist, hosting, OCR where needed, HR-verified gold set, runtime citation check, document update process.

## 5. Plan

All estimates are human hours, agent-assisted, hands-on plus review, quarter hours, with ×1.5 for new-to-ADK applied. No calendar waits. No schedule block or helper run (one person; added by hand). **No resources that charge while idle are created, so there is no teardown goal.**

| Goal | Outcome | Contracts | Hands-on | Review | Total |
| --- | --- | --- | --- | --- | --- |
| G01 | Project skeleton, pinned deps, 30 PDFs → page index and coverage report | C3 | 0.75–1.0 | 0.25–0.5 | 1.0–1.5 |
| G02 | Agent plus search tool answering with citations in `adk web` | C1, C2, C4, C5 | 0.75–1.25 | 0.5 | 1.25–1.75 |
| G03 | Gold-question run, fixes, demo run-of-show and one rehearsal | C1, C2 | 0.75–1.0 | 0.25 | 1.0–1.25 |

Tickets: `docs/tickets/hr-policy-agent/G01-ingest-and-coverage.md`, `G02-grounded-search-agent.md`, `G03-gold-check-and-demo.md`. Each ticket holds its goal's scope and acceptance; **Status and evidence** lives in its Evidence section.

**Capacity (by hand):** sum 3.25–4.5 h. Six hours, taken as focused, minus a 25% reserve (1.5 h) leaves 4.5 h; the high end fits with no slack and the reserve is the only cushion. If the six hours are interrupted time (focus 0.6–0.8, so 3.6–4.8 h, 2.7–3.6 after reserve), only G01 plus G02 at their low ends fit.

**Suggested days:** Wednesday G01 then G02 (2.25–3.25 h). Thursday G03 and the rehearsal (1.0–1.25 h), the rest as reserve.

**Cut line if time runs short, in the order work stays useful:** G01 (corpus is indexed and its gaps known) → G02 (demoable agent) → G03. Shrink G03 first: keep 6 gold questions, 2 out-of-scope, and the rehearsal; drop the expanded question set. Never cut the floor.

**Phase 2 (graduate, only if HR says go; no tickets written):**
- G04 OCR for scanned pages: `adk-memory-architecture`, 1–3 h; acceptance: coverage report shows zero unreviewed scanned pages.
- G05 Embeddings or hybrid retrieval: `adk-memory-architecture`, 2–4 h; acceptance: gold-set recall at least matches G03 and improves its paraphrase misses.
- G06 Sign-in, Cloud Run, runtime citation check: `deploy-adk-on-google-cloud`, `adk-agent-security`, 6–12 h; acceptance: unauthenticated request refused.
- G07 HR-verified gold set (`adk-agent-evaluation` expert review), 4–8 h plus HR session date as a wait.

**Later:** see section 4.

## 6. Open decisions and next prompt

Open: questions 1–5 in section 1; the model ID and ADK pin (checked in G01 and G02); who sets the spend cap (the developer, before G02); whether leadership needs a deck beyond the live demo.

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-ingest-and-coverage.md. Read its design and plan, keep its constraints, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```
