# HR policy Q&A agent: proof-of-concept design and plan

Status: **draft** (assumed answers below are unconfirmed; decisions marked *prov.* depend on them)
Profile: **proof of concept**: one builder, a live demo to HR leadership, read-only, internal policy documents. Correct it if this is meant to become a staff tool soon after.
Tickets: [docs/tickets/hr-policy-qa/](../tickets/hr-policy-qa/). This file is the plan and the source of decisions.

## 1. Constraints and assumed answers

The user was not available, so every answer below is assumed.

| Question | Assumed answer | Depends on it |
| --- | --- | --- |
| Demo date, and kept afterwards? | Friday 2026-10-16. Code is kept if the demo lands | Phase 1 cut; kept-form layout (D6) |
| Builder and hours | You, about 6 h in two blocks of roughly 3 h. New to ADK, comfortable with Python 3.12 | Capacity, setup time |
| Spend | Under US$25 of model use before the demo | Model tier, spend cap |
| Model access | Gemini API key on a **paid** billing account. Vertex in an existing project is the alternative | D4 *prov.* |
| May policy text go to Google's model API? | Yes. The documents are internal but contain no personal data | **Blocks live calls in G02**. G01 runs without it |
| PDF format | Text PDFs, possibly with a few scanned pages | G01 reports which pages are scanned and excludes them |
| Restricted policies (manager-only, confidential)? | None. All 30 are for every employee | No entitlement filter (deferred) |
| Who uses it in the demo | You drive `adk web` on your laptop, and leaders call out questions | Local hosting, no login |
| What leadership judges | Correct answers with citations, an honest "not covered", and a quality table | G03 |
| Language | English | Search tokenizer |

## 2. Journey and shape

Today an employee or HR partner searches 30 PDFs or emails HR to ask, for example, "how many days of carry-over leave do I get?". In the demo, a leader asks that question and gets a short answer. The answer quotes the operative section and names the document, section and page, or it says the policies do not cover the question and to contact HR.

```text
PDFs ──build_index.py──▶ index.sqlite + ingestion-report.json   (offline, no model)
question ─▶ adk web ─▶ LlmAgent ──search_hr_policies(query)──▶ SQLite FTS5 (top 5 sections)
                          └── cited answer or "not covered"
```

The model chooses the search terms (one to three searches) and writes the answer. Code owns extraction, chunking, ranking, result size, the call limits and the pinned model.

## 3. Decisions

| ID | Requirement → choice | Tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Interpret free-text questions over one read-only capability → **one `LlmAgent`, one function tool**, no sub-agents | No routing or specialist agents, and none are needed for one corpus | Tool count = 1. The captured request shows one declaration |
| D2 | Find the operative clause in 30 PDFs within 6 h → **local SQLite FTS5 index of heading-to-heading sections with page spans**, built offline, as in `adk-memory-architecture`'s local-retrieval pattern | Lexical only: synonyms ("PTO" vs "annual leave") can miss. The rejected alternatives are putting all 30 PDFs in every prompt (cost and latency per question, citations hard to check) and Vertex AI Search (half a day of GCP setup) | G03 records which document each question retrieved, so a `query_miss` is visible |
| D3 | No invented policy → the **tool returns at most 5 sections and about 6,000 characters, each with `document`, `heading` and `pages`, plus `status` (`ok`, `no_match` or `index_unavailable`)**. The instruction requires citations and a "not covered, contact HR" reply when nothing relevant comes back | Citation discipline comes from the prompt, so it is probabilistic. Code bounds the evidence but cannot force the wording | G03: every answer cites a returned section, and both not-covered questions are declined |
| D4 *prov.* | Demo behaves as rehearsed, cheaply → **`gemini-3.8-flash` pinned** (stable, released 2026-09-02, no shutdown date in the lifecycle snapshot checked 2026-10-08), called through a Gemini API paid key | A Flash model rather than Pro. If data approval requires Vertex, switch with `GOOGLE_GENAI_USE_VERTEXAI`; the code does not change | `agent.py` contains the literal ID, not an alias. Re-read Google's models page before G02 |
| D5 | Spend stops even in `adk web` → **`RunConfig(max_llm_calls=6)` in the question-runner script; an API-key quota or budget alert for `adk web`** | A budget alert only notifies. The key quota is the real stop | G04 shows the quota/alert setting and the runner's limit |
| D6 | Reusable if the demo lands → a **small package** with model ID, index path and limits in one settings module and `.env` | About 15 minutes more than a single script | Phase 2 reuses `hr_index/` unchanged |

Proposed layout (greenfield, unverified): `hr_index/{ingest,search}.py`, `hr_policy_agent/{agent,tools}.py`, `scripts/{build_index,run_questions}.py`, `evals/questions.json`, `data/policies/` and `build/` (both git-ignored), `tests/`. Working ADK assumption: `google-adk==2.8.0`, the version the specialists were read against. G01 pins it and G02 confirms the interfaces against that pin.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Answer quality | **Build**: 12 checked questions | Before any wider use (G07) |
| Retrieval | **Build**: local FTS5, scanned pages reported | `query_miss` above 2 of 12 → hybrid search (later) |
| Secrets | Minimal: key in `.env` (git-ignored), never in code or prompts | Shared host → Secret Manager (G05) |
| Writes and effects | None: the agent has no write or egress tool, which breaks the untrusted-content-plus-action combination | Any tool that sends or changes something |
| Sensitive data | Minimal: policy documents only; demo questions are generic, with no named employee | Employees type their own situations (G08) |
| Identity, per-user scope | Defer: single local user | Anyone besides you uses it (G05) |
| Budgets | Minimal: D5 | Shared use → per-user allowance |
| Frontend and hosting | `adk web` on your laptop | Staff pilot (G05) |
| Observability | Defer: console | Shared deployment (G09) |
| Release | Minimal: pinned model and ADK | Eval in CI (G07) |

**Graduation conditions** (before any user beyond you): data-processing approval confirmed, sign-in through company SSO, an HR-reviewed evaluation set, a named HR owner who approves document versions, and question content kept out of logs.

**Failure paths** (the only ones this journey has):

| Failure | User sees | Recovery |
| --- | --- | --- |
| No relevant section | "Not covered in the policies provided; contact HR" | None needed. This is the correct result |
| Page had no extractable text | The answer cannot use that page. The ingestion report lists it | Name the excluded pages in the demo. OCR comes later |
| Two policies conflict | Both cited, and the conflict stated | HR owner decides (phase 2 release process) |
| Model error or quota hit | `adk web` error, and nothing is stored | Retry once. If that fails, show the G04 results table |

## 5. Plan

**Capacity:** 6 h × 0.8 (dedicated blocks) = 4.8 focused hours. A 25 % reserve leaves **3.6 h for goals**.
**Cut line:** phase 1 = G01 to G04, **3.0 to 4.25 h**. Only the low end fits inside the reserve. If G02 runs long (first ADK setup), G03 drops to 6 questions and G04 shrinks to setting the spend cap. The spend cap and the pinned model are never cut. Order of usefulness: G01 → G02 gives a demo, G03 makes it credible, and G04 makes it safe to rerun.

| ID | Outcome | Est. | Primary skill | Depends on |
| --- | --- | --- | --- | --- |
| G01 | 30 PDFs become a searchable section index with an ingestion report | 0.75–1.25 h | `adk-memory-architecture` | none |
| G02 | Ask a question in `adk web` and get a cited answer or "not covered" | 1.25–1.75 h | `adk-tool-interface-design` | G01, data approval |
| G03 | 12 checked questions produce a reviewable results table | 0.75–1.0 h | `adk-agent-evaluation` | G02 |
| G04 | Spend cap, version record and rehearsal for Friday | 0.25 h | `adk-operational-guardrails` | G03 |

Acceptance, depth and the run prompt for each goal are in its ticket. Run the next one with:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-section-index.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

**Phase 2: graduate to an HR-staff pilot** (coarse; demo feedback may change it)
- **G05** Cloud Run behind IAP with Workspace sign-in, Vertex in a company project, key in Secret Manager. `deploy-adk-on-google-cloud`, 4–8 h. Check: a signed-out request gets 401/redirect, and a signed-in HR user gets a cited answer.
- **G06** Document release: an HR owner approves versions, the index records version and date, and removed documents disappear. `adk-memory-architecture`, 2–4 h. Check: replacing a PDF changes the cited version.
- **G07** 40+ HR-reviewed questions run in CI with a pass threshold. `adk-agent-evaluation` (supporting `adk-release-engineering`), 4–6 h. Check: CI fails on a seeded regression.
- **G08** Question content kept out of logs, with retention defined. `protect-adk-sensitive-data`, 2–4 h. Check: logs from a test question contain no question text.
- **G09** Structured logs and token cost per question. `adk-agent-observability`, 1–2 h. Check: one log line per question with its token count.

**Later**, each with the trigger that brings it forward and the risk accepted meanwhile:
- Hybrid embeddings: when `query_miss` exceeds 15 % on G07. Meanwhile, synonym misses are visible in results.
- Managed retrieval such as Vertex AI Search: when the corpus passes about 300 documents or needs a scheduled sync.
- Audience entitlements: when the first restricted policy appears. Until then, all documents are assumed public to staff.
- OCR for scanned pages: when G01 reports pages that matter.
- Multilingual support: when a non-English office joins.
- SLOs and alerts: at production launch.

## 6. Open decisions

1. **Data approval** for sending policy text to the Gemini API, or a move to Vertex. Blocks live calls in G02. Owner: you or IT security.
2. **Model ID re-check:** `gemini-3.8-flash` comes from a snapshot dated 2026-10-08. Confirm on ai.google.dev before G02.
3. **Profile:** if HR wants staff using it within weeks, phase 2 becomes the main plan and identity moves up.
4. **Spend cap value:** US$25 is assumed.
