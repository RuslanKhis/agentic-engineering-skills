# HR policy Q&A agent: proof of concept (design and plan)

Status: **draft**. Every decision below is provisional until the builder confirms the assumed answers.
Written 2026-10-09. Nothing implemented yet. This one file holds both the design and the plan.

## 1. Constraints and profile

**Profile: proof of concept.** One builder, about 6 hours, and a demo to HR leadership on Friday. The system only reads. Correct this line if it is wrong.

| Question | Answer (A = assumed) | What depends on it |
| --- | --- | --- |
| Deadline, then? | Demo Fri 2026-10-16 (A: today is Friday, so this means next week). Probably continued if it lands (A) | Phase 1 keeps its code. Phase 2 is written below |
| Who builds | One person, 6 h over two days. Comfortable with Python, new to ADK (A) | Capacity, and a ×1.5 multiplier on every estimate |
| Money | Small: under US$20 of model spend for the POC (A) | Flash-class model, no managed search service |
| Audience | The builder demos by screen share on a laptop. HR leaders suggest questions (A) | `adk web` locally. No login, no hosting |
| Data and effects | About 30 internal policy PDFs. They are text based, contain no personal data and cover one jurisdiction (A). The agent changes nothing | The floor (§4). Data use with Gemini must be confirmed (O1) |

## 2. Journey and shape

An HR leader asks "How many days of parental leave does a secondary carer get, and is it paid?" Today someone searches 30 PDFs or emails HR. In the demo the agent answers in a few sentences, cites the document and page, and says "not covered by these policies, contact HR" when the PDFs are silent.

```
adk web → LlmAgent (pinned model) ─tools→ list_policies()   catalogue: id, title, pages
                                         read_policy(id, pages?)  page-tagged text, bounded
                         offline:  scripts/extract.py  PDFs → data/corpus/*.json + catalogue.json + extraction report
```

**The model decides** which policies to open and how to word the answer. **Code controls** text extraction, the catalogue, page numbers in citations, the size of tool results, the pinned model and the call cap.

## 3. Decisions

| # | Requirement → choice | Tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Correct answers from 30 short PDFs, built in a few hours → document-level routing. The model reads the catalogue, opens one to three whole policies and gets page-tagged text. No embeddings, no vector store | More tokens per question than chunk retrieval, and it does not scale past roughly 100 documents (phase 2 trigger). In return there is no index to tune, and each policy arrives complete with its qualifiers | Gold questions (G03) show the right document opened and the right page cited |
| D2 | Trustworthy answers → the instruction requires an answer only from tool text, with citations in the form *(Policy title, p. N)*, and a fixed "not covered" reply otherwise. No advice on individual cases | Refuses some answerable questions that would need inference | The "not covered" gold cases refuse. The cross-document case cites both policies |
| D3 | Behaviour must match yesterday's dry run → pin **`gemini-3.8-flash`**. Per the lifecycle snapshot `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked 2026-10-08) it is stable, released 2026-09-02, with no shutdown announced. Avoid the 2.5 models (limited) | Not the strongest model. Escalation is a phase 2 measurement | A captured request shows the pinned ID. No alias |
| D4 | One `LlmAgent` with two read-only function tools. No sub-agents, no MCP | — | Offline tool tests. The agent has exactly 2 tools |
| D5 | Bounded tool results → `read_policy` returns at most about 40k characters, with a `truncated` flag and the page range, so the model can ask for more pages | One more tool call on long policies | Unit test on the largest PDF |
| D6 | Kept form → `google-adk==2.8.0` is the working pin, the version the specialists were checked against (`adk-memory-architecture/references/compatibility.md`). Confirm it in G01. Settings go in `config.py`, not in the prompt | — | `pyproject.toml` pins it. G02 confirms the APIs it uses |

## 4. Floor, depth and deferred

| Concern | Now | Trigger to raise |
| --- | --- | --- |
| Secrets | **Floor:** API key in `.env`, git-ignored, never in code or prompts | Any shared deploy → Secret Manager (G05) |
| Spend stop | **Floor:** `RunConfig(max_llm_calls=8)` in the G03 runner. A budget alert on the model project, because `adk web` uses its own Runner | Anyone besides the builder uses it |
| Writes and effects | None. Read-only tools, no egress tools. This removes the injection risk (no write leg) | Any tool that sends or files something |
| Sensitive data | Policies only. No employee records in the corpus or in demo questions | Personal or case data → `protect-adk-sensitive-data` |
| Identity | Deferred. Single local user | HR leaders use it themselves (G05) |
| Retrieval | Build at minimal depth (D1) | More than about 100 docs, or a cost per question above about US$0.05 → G07 |
| Evaluation | About 10 gold questions, judged by hand (G03) | Continued past the demo → G06 |
| Hosting, observability, release | Local, console logs, pinned model | Shared use (G05) |

**Graduation conditions** (before anyone other than the builder uses it): a confirmed data-use approval (O1); identity behind IAP; a named owner and refresh process for the corpus; a labelled set of 30 or more questions with a measured pass rate.

**Failure paths** that matter for the demo: a scanned PDF yields no text, so the extraction report lists it and the catalogue marks it unreadable rather than silently missing. Two policies conflict, so the agent cites both and says they differ. The model or network fails mid-demo, so the builder plays a recording of the dry run made in G03. A tool loop hits `max_llm_calls` and stops with an error, never a made-up answer.

## 5. Plan

Capacity: 6 h × 0.8 focus = 4.8 h. Keeping a 25% reserve (1.2 h) for demo preparation and the dry run leaves **3.6 h for goals**. Every estimate below already includes the ×1.5 for being new to ADK.

```yaml
- goal: G01
  phase: 1
  hands_on: 0.3-0.5
  review: 0.2-0.3
  total: 0.5-0.8
  owner: Builder
  blocked_by: []
  calendar_waits: none
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 0.5-0.8
  review: 0.5-0.7
  total: 1.0-1.5
  owner: Builder
  blocked_by: [G01]
  calendar_waits: data-use confirmation O1, requested before day 1
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 0.6-1.0
  review: 0.2-0.3
  total: 0.8-1.3
  owner: Builder
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
```

Schedule check (`check_schedule.py`, run 2026-10-09; capacity 3.6 h, 2 days at 1.8 h/day): phase 1 **2.3–3.6 h**, fits (high end exactly); chain G01→G02→G03; finish 1.3–2 working days, fits the calendar **only if O1 is requested before day 1** (with a 1-day O1 wait on G02 the high end becomes 3 days and G03 misses Friday).
**Cut line:** G01–G03 ship by Friday. G04 onward waits. If the work runs high, G03 shrinks to 5 questions typed into `adk web`, and its script moves to G06. Each goal is still demonstrable if time runs out after it.

**G01: Extract the 30 PDFs into a page-tagged corpus.** Total 0.5–0.8 h. The script writes per-document page text, `catalogue.json` and a report of empty or failed pages. It also creates `pyproject.toml` with pins. Primary skill: `adk-memory-architecture`. Acceptance: all 30 PDFs are in the catalogue, the page count matches each PDF, and unreadable pages are listed rather than dropped. Ticket: `docs/tickets/hr-policy-qa/G01-extract-corpus.md`.

**G02: The agent answers a policy question with page citations.** Total 1.0–1.5 h. Builds `LlmAgent` with `list_policies` and `read_policy`, the D2 instruction, the pinned model and `adk web`. Primary skill: `adk-memory-architecture`. Supporting skills: `adk-tool-interface-design`, `adk-agent-instructions`, `adk-model-and-output-contracts`. Acceptance: offline tool tests pass, one live question gets a cited answer, and an off-topic question gets the "not covered" reply. Ticket: `G02-answer-with-citations.md`.

**G03: Gold-question check and demo dry run.** Total 0.8–1.3 h. The builder writes about 10 questions with expected document and page: 7 answerable, 2 not covered and 1 that needs two documents. A runner script writes a results table, the builder judges it by hand, and a dry run is recorded as the demo fallback. Primary skill: `adk-agent-evaluation`. Acceptance: the table exists, the pass count is stated honestly, and both not-covered cases refuse. Ticket: `G03-gold-questions-and-dry-run.md`.

**Phase 2** (coarse, after the demo; ×1.5 included):
- **G04:** Fix the misses found in G03, and decide on model escalation using the gold set. 1.5–3 h. Primary skill: `adk-agent-evaluation`. Check: the gold-set pass count goes up with no new wrong citations.
- **G05:** Cloud Run behind IAP for named HR leaders, with Secret Manager, structured logs and a release manifest. 6–9 h, plus a wait for IAM and data approval. Primary skill: `deploy-adk-on-google-cloud`. Supporting skills: `adk-agent-observability`, `adk-release-engineering`. Check: a non-allowlisted user is refused.
- **G06:** A labelled set of 30 or more questions with a runner, and a pass threshold. 4–8 h, mostly labelling. Primary skill: `adk-agent-evaluation`. Check: a stored run file with the pass rate per category.
- **G07:** Managed retrieval (Vertex AI Search or RAG Engine) with versioned corpus releases. 5–9 h. Primary skill: `adk-memory-architecture`. Check: the gold-set score is no worse than D1, and the cost per question is lower.

**Later:** employee identity and per-entity policies (trigger: policies vary by country or contract); sensitive-data screening (trigger: questions about real cases); CI evaluation gate (trigger: more than one contributor); SLOs and alerts (trigger: daily use).

## 6. Open decisions and next prompt

- **O1:** May internal HR policies be sent to Gemini through the builder's project? Assumed yes, on a billed project or Vertex AI. This must be confirmed before the first live call in G02, and it blocks only G02's live check.
- **O2:** Are any PDFs scanned images? G01's report answers this. If any are, add OCR or exclude them, and say so in the demo.
- **O3:** Should the agent be allowed to interpret policies, or only quote them? D2 assumes it summarises and cites.

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-corpus.md.
```
