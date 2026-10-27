# HR policy Q&A agent: proof of concept design and plan

Status: **draft**. Every answer in the assumed-answers table is an assumption, not a user decision. Nothing is built yet.
Profile: **proof of concept**, one developer, about 6 hours over two days, live demo to HR leadership on Friday 30 Oct 2026. Phase 1 code is meant to be kept (D6).

## Summary (for the person who decides)

- Phase 1 delivers a local ADK agent that answers HR policy questions from about 30 PDFs, cites document and page for every claim, says "not found" instead of guessing, and runs in `adk web` on the builder's laptop for the demo.
- Phase 1 estimate is 3.5 to 5.5 hours (G01 to G05) against 4.5 usable hours (6 hours minus a 25% reserve). **The low end fits; the high end does not.** The cut line is in the Plan section; please confirm or move it.
- Largest risks: (1) permission to send policy text to the model provider is unconfirmed (W1); (2) some PDFs may be scans with no extractable text, which G01 will reveal; (3) answers that sound right but cite the wrong clause, which G04 measures on a small hand-labelled set.
- Decisions needed from you: confirm W1, the cut line, and who may be named as an HR reviewer of the gold questions (Open decisions).

## 1. Constraints and profile

The session is non-interactive, so each scope-gate question is answered with an assumption. Decisions that depend on an assumption are provisional.

| Question | Assumed answer | Depends on it |
| --- | --- | --- |
| Deadline and afterwards | Demo Fri 30 Oct 2026; continued if HR leadership likes it | Phase 1 cut line; kept-code choice D6 |
| Builder and hours | One developer, 6 focused hours on Wed 28 and Thu 29 Oct, new to ADK and GCP (1.5x on ADK work, folded into the estimates) | All estimates; no GCP project work is planned |
| Money | Small allowance, taken as at most USD 10 of model spend, enforced by a provider quota the builder sets (C5) | Model tier; number of eval runs |
| Judge and what they read | HR leadership watching a screen share; non-technical | Demo script (G05); citations visible in answers |
| Interface | `adk web` on loopback, builder drives; no URL for others; not handed over | No auth, no hosting; Cloud Run is phase 2 |
| Data and effects | About 30 internal HR policy PDFs, current approved versions only, no employee records; read only | Data handling W1; no write-side contracts |
| Reviews | Friday demo is the go/no-go review for phase 2; no pre-build deck | G05 is the only presentation goal |
| Contract, lock-in | No statement of work; no lock-in concern | No SOW or portability goal |
| PDF quality | Unknown: text, scans or tables | G01 reports it per page; OCR is deferred |

Waits: **W1** approval to send the HR policy text to the model provider, requested today (Tue 27 Oct). It is an outside approval, runs in parallel and blocks G03 only. If refused, the agent cannot call a hosted model and the plan is replanned (Open decisions).

## 2. Journey and shape

An HR leader asks "how many days of parental leave, and can they be taken in blocks?". The agent searches the policy corpus, reads the returned passages, and answers with citations such as `[Parental Leave Policy, p.3]`. When nothing relevant is found it says so and suggests contacting HR. Today the answer means finding the right PDF and reading it.

The model decides which queries to run and how to phrase the answer. Code controls the corpus, retrieval, the citation check and the call cap. One `LlmAgent` with one function tool, `search_policies(query)`, which returns passages with document, page and text. There is no sub-agent, vector database or hosted service.

## 3. Contracts and decisions

| ID | Invariant and scope | Enforcement | Evidence |
| --- | --- | --- | --- |
| C1 | Every citation in an answer names a (document, page) that the search tool returned in the same invocation; an answer with an uncited or unreturned citation is replaced by the fixed not-found message | `after_model_callback` checks citations against the invocation's retrieved set | offline test with forged citation (G03); gold run (G04) |
| C2 | The agent answers only from the approved corpus manifest (the about 30 PDFs, by file hash); its only tool is `search_policies` | Tool list in code; manifest built by G01 and read by the index | offline test: index doc set equals manifest (G02) |
| C3 | Every page of every PDF has an extraction record; pages with empty or failed extraction are listed, never silently skipped | Ingestion script exits 1 while any page lacks a record; the report lists empty pages | G01 report; known gaps shown in the demo |
| C4 | A question about a named person's case, legal advice or an eligibility decision gets general policy with a referral to HR, not a determination | Instruction plus a small refusal case set. **Gap:** no deterministic screen; accepted for the POC (owner: builder), deferred until real users | 3 labelled cases in G04 |
| C5 | At most N model calls per question (N fixed in G03) and a provider spend quota; no API key in source, prompts or logs | `before_model_callback` counter; quota set on the model project by the builder | offline test of the cap; manual quota check (G03, G05) |

Decisions (requirement, contract, choice, tradeoff, check):

- D1 Ground answers: R1, C1, C2. Retrieval tool plus a code-level citation check. Tradeoff: stricter than prompt-only, rejects some good answers. Check: G03 forged-citation test.
- D2 Retrieval is in-process keyword ranking (BM25) over page-level passages with their headings and neighbours, no embeddings. Tradeoff: misses synonyms ("maternity" vs "parental"), but costs nothing idle and is debuggable. Check: G02 gold queries; hybrid is a phase 2 trigger if recall is under 80%.
- D3 Ingest first: C3. Per-page report before any model work, following the ingestion reference. Tradeoff: spends 1 hour before the agent exists; avoids demoing over silent gaps.
- D4 Model: a pinned Gemini Flash-class model ID chosen from the dated model lifecycle table in G03 (provisional: that table is not in this workspace). ADK 2.8.0 is the working assumption; G01 confirms the pin.
- D5 `adk web` for the demo, with a recorded fallback transcript (G05) because the model API is the only external system: if it is slow or down the live demo has no other path.
- D6 Code kept in a normal package (`hr_policy_agent/`) with config in one file, so phase 2 changes values, not structure.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Core judgment, measured | Build: 10 hand-labelled questions plus 3 C4 cases | Real users; HR reviewer labels |
| Secrets | Minimal: key in environment, `.env` git-ignored | Any shared host |
| Spend stop | Minimal: C5 | More users |
| Sensitive data | Minimal: no employee data; questions not logged beyond the console | Real case questions from staff |
| Prompt injection | Minimal: corpus is the only untrusted input and the agent has no write tool | Any write tool |
| Identity, hosting, release, observability, performance | Deferred | URL for anyone but the builder |
| Teardown | None: nothing charges while idle; the demo key is revoked in G05 | Cloud resources created |

Resource ledger: no resource that charges while provisioned is created. Model spend is usage only, capped by C5.

Graduation conditions (become phase 2): HR reviewer labels the gold set; scanned pages handled; policy versions and effective dates tracked; sign-in before anyone else can reach it; data-handling approval for real usage.

## 5. Plan

Estimates are human hours, hands-on plus review and verify, agent-assisted, quarter-hour rounding. The 1.5x new-to-ADK multiplier is already applied to G03.

Phase 1 (order is dependency order; `G01 > G02 > G03 > G04 > G05`):

| Goal | Outcome | Contracts | Hands-on | Review | Total | Primary skill |
| --- | --- | --- | --- | --- | --- | --- |
| G01 | Corpus manifest and per-page ingestion report | C2, C3 | 0.5-1 | 0.25 | 0.75-1.25 | adk-memory-architecture |
| G02 | Page-level index and `search_policies` tool, 10 gold queries | C2, C3 | 0.5-1 | 0.25 | 0.75-1.25 | adk-memory-architecture |
| G03 | Agent in `adk web` with citation check and call cap (needs W1) | C1, C5 | 0.75-1 | 0.25-0.5 | 1-1.5 | adk-engineer |
| G04 | Gold questions through the agent, hand review, fix top failures | C1, C4 | 0.25-0.5 | 0.25 | 0.5-0.75 | adk-agent-evaluation |
| G05 | Demo script, dry run, fallback transcript, key revoked after | C5 | 0.5 | 0-0.25 | 0.5-0.75 | adk-engineer |

Tickets: `docs/tickets/hr-policy-agent/`. Each ticket holds the goal's acceptance and run prompt; this table holds its estimate. The G05 presentation is owned by `adk-presenter` in the full method; that skill is not installed here, so G05 is a demo-readiness goal carried by `adk-engineer`.

Sum by hand (one person): low 3.5 h, high 5.5 h. Capacity: 6 h minus 25% reserve is 4.5 h. **The high end exceeds it by 1.0 h; only the low end fits.**

Cut line (please confirm or move): G01 to G03 and G05 are fixed. At their high ends they total 4.75 h, already 0.25 h over 4.5 h, so G04 is the flexible goal and the only one that moves:
- Cumulative time after G03 of 3.0 h or less: G04 runs as written.
- Between 3.0 h and 4.0 h: G04 runs on 5 of the 10 gold questions plus the 3 C4 cases; the other 5 move to phase 2.
- Over 4.0 h: G04 is dropped to a hand read of answers during the G05 rehearsal, and the demo says answer quality is not yet measured (C1 keeps its offline evidence only).

The order that stays useful if time runs out: G01, G02 (a searchable corpus), G03 (an answering agent), G05, then G04.

Day split: Wed, G01, G02 and the start of G03 (about 3 h); Thu, finish G03, G04, G05.

Phase 2 (after the demo, not ticketed):
- P2-1 Gold set labelled with an HR reviewer and expanded to 30+ questions, with a runner (adk-agent-evaluation), 4-8 h, check: agreement report on the labels.
- P2-2 Scanned and table pages routed through OCR or vision review (adk-memory-architecture), 3-6 h, check: no empty-extraction pages in the report.
- P2-3 Hybrid retrieval if gold recall is under 80% (adk-memory-architecture), 3-6 h.
- P2-4 Cloud Run behind sign-in for HR leaders to try it (deploy-adk-on-google-cloud), 3-6 h plus a project wait; adds a teardown goal.

Later: version and effective-date tracking when a policy is revised; observability when others use it; evaluation gate in CI when the prompt changes weekly.

## 6. Open decisions and next prompt

| Question (assumed answer used) | Impact if wrong | Who settles |
| --- | --- | --- |
| May the policy text go to the model provider? (assumed yes, W1) | G03 blocked; local model route needed | Builder with HR or security owner |
| Are the 30 PDFs the current versions, text-based? (assumed yes) | G01 may show scans; coverage gaps shown in the demo | G01 report |
| Is 6 hours focused time? (assumed yes) | Plan loses its reserve | Builder |
| Which model and credential (AI Studio key or Vertex)? | G03 setup time | Builder, in G03 |

Failure paths reviewed: the model API is the only external system and nothing is written, so there is one row: unavailable or slow produces an error in `adk web`, and the demo uses the fallback transcript from G05. Unknown writes and rejected requests do not apply.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01-corpus-ingestion.md
```
