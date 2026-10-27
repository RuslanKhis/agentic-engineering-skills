# HR policy agent: proof of concept design and plan

Status: **draft**. Every answer in the scope gate below is assumed, not confirmed (nobody was available to ask). Written 2026-10-27. Design only; nothing is built.

## 1. Constraints and profile

Profile: **proof of concept**, kept (phase 1 code is meant to be continued if the demo lands). Reason: one developer, about 6 hours over two days, demo to HR leadership on Friday 2026-10-30.

| Question | Assumed answer | Decisions that depend on it |
| --- | --- | --- |
| Deadline and afterwards | Demo Fri 2026-10-30; continued if HR leadership approves | Kept code layout (D6), phase 2 list |
| Builder | One developer, ~3 h on each of Wed 28 and Thu 29 Oct, new to ADK (estimates x1.5, stated once here) | Capacity, estimates |
| Spend | Small personal or team allowance; a spend cap is set on the model key or project before G02 | Floor item F2, D5 |
| Judge | HR leadership watches the builder drive a live demo; they read answers and citations | Citation format (C1), demo goal G03 |
| Interface | `adk web` on loopback, builder's laptop, screen-shared; no URL, no hand-over | D4; web security baseline n/a (loopback, nobody else connects) |
| Data and effects | About 30 HR policy PDFs, text-based, internal, no employee personal data; the agent is read-only and changes nothing | Floor; no governance goal |
| Model access | Sending the policy text to the chosen hosted model is already approved by the owner of the documents | D5. If wrong, G01 stops before G02 |
| Reviews | Friday demo is the only review; build is already authorised, so no approval deck and no statement of work | No presentation ticket (see section 5) |
| Lock-in | Not a concern | No portability goal |

Open questions written down for the user (no answer was possible):
1. Are all 30 PDFs text-based, or are some scans? Assumed text. Scans are reported by G01, not read.
2. Is sending the policies to a hosted model approved? Assumed yes.
3. Which model and how is it reached (Gemini API key or Vertex)? Not assumed: G01 picks a model ID from Google's current lifecycle page and pins it.
4. Which dates are the two work days? Assumed Wed 28 and Thu 29 Oct.

## 2. Journey and shape

An HR leader asks "How many days of parental leave do we offer, and does it apply to part-time staff?". Today someone opens several PDFs and searches. The agent searches the policy pages, answers from the passages it found and cites document and page, or says it cannot find the answer.

The model decides what to search for and how to phrase an answer from returned passages. Code controls what is searchable, what is returned and the call cap. One `LlmAgent` with one function tool, `search_policies(query)`. A second agent is not justified.

```
PDFs -> G01 extract per page (JSON + ingestion report) -> BM25 index in memory
question -> LlmAgent (pinned model, max_llm_calls) -> search_policies -> passages {doc, page, text}
         -> answer with citations, or "not found in the policy documents"
```

Retrieval is local lexical search (BM25) over page-sized units, not embeddings or a managed RAG service. Reason: nothing to provision, no idle cost, exact page citations, and 30 documents are small. Tradeoff: weaker on paraphrased questions; D2 holds the check and the upgrade trigger.

## 3. Contracts and decisions

| ID | Invariant (scope) | Enforcement | Check |
| --- | --- | --- | --- |
| C1 | Every policy claim in an answer cites a document and page that `search_policies` returned in that turn (all questions) | Tool returns only `{doc, page, text}` units from the corpus; the eval script rejects any cited doc/page not in the returned set. Runtime refusal of uncited answers is deferred (observed, not enforced) | G03 gold run with citation check |
| C2 | The agent reads only the configured corpus folder and has no write, network or code tools (all sessions) | The tool list is exactly `search_policies`; its path is fixed in config, a query is never used as a path | G02 test: tool list and path-traversal query |
| C3 | When no returned passage supports an answer, the agent says the documents do not cover it and points to HR, instead of guessing (out-of-corpus questions) | Tool returns an explicit empty result below a score threshold; the instruction names the refusal text | G02 empty-result test; G03 three out-of-corpus questions |
| C4 | A page that produced no text is never treated as "no provision exists" (all documents) | G01 ingestion report lists every empty page; the tool result flags a document with empty pages so the answer carries the caveat | G01 report test on a PDF with an empty page |
| C5 | Spend stops: calls per question are capped and the model key or project has a spend cap (all runs) | `RunConfig.max_llm_calls` is not available through `adk web`, so the cap goes on the model key or project quota | G02 manual check of the cap setting |

Decisions (requirement, contract, choice, tradeoff, check):
- D1 Page-level extraction with `pypdf`, per-page JSON. Contracts C1, C4. Tradeoff: tables and scans extract badly; reported by G01, not fixed.
- D2 BM25 over pages, top 5, threshold for empty. C1, C3. Tradeoff: lexical only. Upgrade to embeddings when the gold set shows `query_miss` failures (see `adk-memory-architecture` local-document-coverage).
- D3 One agent, one tool, instruction in a file, answers concise with a citation list. C1, C3.
- D4 `adk web` on loopback only. Not reachable by anyone else. Tradeoff: no one else can try it.
- D5 Pinned model ID (chosen in G01), cap on key or project. C5.
- D6 Layout: `hr_agent/` package (agent, tools, config), `data/policies/` for PDFs (git-ignored, not committed), `data/pages/` for extracted JSON, `tests/`, `eval/`. Paths come from config so phase 2 can change them.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Secrets (F1) | Minimal: key in environment, never in code, prompts or logs | Any shared deployment: Secret Manager |
| Spend stop (F2) | Minimal: C5 | More users: per-user allowance |
| Model pin (F3) | Minimal: pinned ID | Model retirement date inside the plan horizon |
| Identity | Deferred: loopback, builder only | Anyone else connects or a URL exists: managed sign-in |
| Sensitive data | Deferred: no personal data assumed | Case-specific questions or employee records |
| Injection and agency | Minimal: no write or network tools, so the injection-plus-write combination cannot occur | Any write tool |
| Observability, CI gate, hosting | Deferred: console logs, local | HR wants daily use: Cloud Run behind IAP, traces |
| Runtime citation enforcement | Deferred | Used by people who do not check citations |

Graduation conditions (phase 2): an owner for the policy corpus and a refresh process; identity and hosting; larger labelled set reviewed by HR; runtime citation check; scans handled.

Resources that charge while idle: none. All local. So there is no teardown goal; the only cleanup is deleting `data/` copies of the PDFs if HR asks.

## 5. Plan

Capacity: 6 h x 0.75 focus; hold 25% (1.5 h) in reserve for setup surprises and the demo run, leaving 4.5 h for goals. Summed by hand (one person):

| Goal | Hands-on | Review | Total |
| --- | --- | --- | --- |
| G01 Ingest PDFs and search them | 0.75-1.0 | 0.5-0.75 | 1.25-1.75 |
| G02 Agent answers with citations in `adk web` | 0.5-0.75 | 0.25-0.5 | 0.75-1.25 |
| G03 Gold questions and demo dry run (journey) | 0.75-1.0 | 0.25-0.5 | 1.0-1.5 |
| **Phase 1 total** | | | **3.0-4.5 h** |

The high end exactly uses the 4.5 h after reserve; there is no slack beyond the reserve. These are tighter than the usual 3-6 h for retrieval with gold questions, so the risk is real. Cut line, in order if G01 or G02 runs high: (1) gold set 10 -> 6 questions; (2) drop the cross-document question; (3) demo uses G02 as built with a scripted fallback transcript. Never cut the floor or C3. If time runs out early, the order that stays useful is G01, G02, G03.

Schedule: Day 1 (Wed 28): G01, G02. Day 2 (Thu 29): G03, then buffer. Demo Fri 30. No calendar waits.

Presentation: `adk-presenter` is not installed here, so there is no presentation ticket. Demo preparation (script, fallback transcript) is inside G03. Friday's review is the user's.

Tickets: `docs/tickets/hr-policy-agent/G01.md`, `G02.md`, `G03.md`. Each holds its outcome and acceptance.

**Phase 2 (graduate, not ticketed):**
- P2-1 Hosting and sign-in: Cloud Run behind IAP, `deploy-adk-on-google-cloud`, 4-8 h, check: unauthenticated request is refused.
- P2-2 Larger labelled set reviewed by HR, `adk-agent-evaluation`, 4-8 h, check: agreement report plus coverage score.
- P2-3 Embeddings or hybrid retrieval if G03 shows query misses, `adk-memory-architecture`, 3-6 h, check: gold-set recall improves.
- P2-4 Scans and tables: OCR route per page, `adk-memory-architecture`, 3-6 h, check: per-page route report has no unrouted page.

**Later:** observability and traces (trigger: daily use); evaluation gate in CI (trigger: second developer); policy refresh and versioning (trigger: a document changes); runtime citation enforcement (trigger: unattended use).

## 6. Open decisions and next prompt

Open: questions 1-4 in section 1; the model ID (settled in G01).

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01.md.
```
