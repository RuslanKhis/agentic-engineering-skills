# Implementation plan: planning assessment assistant

Status: **draft / ready goals identified** — nothing has been run; no code,
installation or model call has been made.
Architecture: [docs/architecture/planning-assistant.md](../architecture/planning-assistant.md)
Continuation source of truth: this plan.

## Destination and constraints

**End result.** `deliverables/holdout-predictions/<case>.json` for the five
holdout cases, produced by a frozen method; `deliverables/report.md` under two
pages (what was built, how it was checked, limits); a living
`docs/evaluation-summary.md` with one row per iteration.

**Non-goals.** Officer revision workflow, export, recovery contracts, identity,
hosting, LLM judge, semantic memory, cloud retrieval (design, deferred
controls table).

**Stack (proposed, A1/A2).** Python 3.11+, `google-adk` (`LlmAgent`, `Runner`,
`InMemorySessionService`, `RunConfig`), `pypdf` for text layers, a PDF page
renderer (`pypdfium2` proposed) for images, `pydantic` for schemas, SQLite
FTS5 from the standard library, `pytest`. Versions to be pinned on install
(G00) and recorded in the report.

**Authorization now.** Design only. Installation, model calls and spend are
authorized only when the user starts the build; each goal below states what
it needs. The key stays in the environment, never in files.

**Inspected vs proposed.** Workspace is empty; every path below is a proposed
greenfield layout:

```
planning_assistant/
  ingest.py        # qualify pages, route, render   (G01)
  facts.py         # stage 2: LlmAgent, vision, case_facts.json   (G03)
  index.py         # chunk by policy unit, FTS5, screened pages   (G02)
  retrieve.py      # queries by issue, reference lookup, 2nd round, sufficiency   (G02)
  draft.py         # stage 5: LlmAgent, schema, exemplars (leave-one-out)   (G03)
  check.py         # schema validation, citation resolution   (G03)
  score.py         # decision match, policy-ID overlap, defects.jsonl   (G03/G04)
  budget.py        # call/token caps, ledger, reserve   (G03)
  cli.py           # run-dev, run-holdout (frozen hash), summarize   (G03/G05)
tests/
data/              # ingestion/, index/, runs/<run-id>/<case>/, eval/, ledger.jsonl
deliverables/      # holdout-predictions/, report.md
```

## Implementation map

| Decision / requirement | ADK or application component and integration point | GCP service/responsibility | Primary skill | Verification still needed |
| --- | --- | --- | --- | --- |
| D03 page routing, origin labels | `ingest.py`; the memory skill's `qualify_ingestion.py` pattern (inventory of page records → report); renderer for routed pages | none | `adk-memory-architecture` (document-ingestion reference) | Thresholds calibrated on this corpus; renderer install |
| D04 retrieval by issue | `index.py` + `retrieve.py`; the memory skill's `local_retrieval.py` pattern (heading chunker, FTS5 bm25, `resolve_references`, `retrieve_for_issues`, `sufficiency_problems`) | none | `adk-memory-architecture` (retrieval-strategy reference) | Heading grammar (A5); gold set hand-written |
| D02 two LlmAgents in ordinary-code sequence | `facts.py`, `draft.py`: `LlmAgent` per stage, run via `Runner` + `InMemorySessionService`, one session per case per stage; `RunConfig.max_llm_calls` set per invocation | none | `adk-workflow-design` | Installed ADK version's image-input and structured-output interfaces (G00) |
| D05 prompt and schema | `draft.py` prompt skeleton; `pydantic` `Decision` model; `exemplars_for()` leave-one-out | none | `adk-agent-evaluation` (quality-iteration reference) | Dev label structure (conditions library?) |
| D07 spend control | `budget.py`: `Budget.admit(case_id)` before each call, `Budget.settle(usage)` after, `ledger.jsonl`; reserve partition | none | `adk-operational-guardrails` | Provider usage fields in ADK events for the installed version |
| D06 measurement loop | `score.py`, `data/eval/defects.jsonl`, `docs/evaluation-summary.md` | none | `adk-agent-evaluation` | Scorer scope after reading labels |
| D09 freeze rule | `cli.py run-holdout --config-hash <hash>` refuses a mismatch; run record stores hash | none | `adk-agent-evaluation` (progressive validation) | — |
| A3 field minimisation | `ingest.py` drops applicant name/contact fields from form text before stage 2 | none | `protect-adk-sensitive-data` (one line of code; no inspection service) | Form layout seen in G01 |

Skill availability: all named skills exist in this repository's `skills/`
directory (checked 6 October 2026). `adk-memory-architecture` bundles the
`qualify_ingestion.py`, `local_retrieval.py` scripts and an ingestion fixture
that G01/G02 can run as mechanism controls.

## Goals and dependencies

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| G00 Confirm the key, model, image input and ADK interfaces | discovery | — | `adk-engineer` | ready; needs install + one tiny call |
| G01 Ingest and qualify every page of the ten cases and the policy corpus | implementation | G00 (renderer choice only) | `adk-memory-architecture` | ready; offline except rendering |
| G02 Index the Local Plan and SPDs, retrieve by issue, measure gold-set recall | implementation | G01 (corpus text) | `adk-memory-architecture` | ready after G01 |
| G03 Draft decisions end to end and baseline on the five development cases | implementation | G00, G01, G02 | `adk-workflow-design` | ready after G02; live spend |
| G04 Error analysis and one-change iterations within the development allowance | implementation | G03 | `adk-agent-evaluation` | blocked until baseline exists |
| G05 Freeze the method, run the holdout from the reserve, write the report | implementation | G04 (or G03 if time runs out) | `adk-agent-evaluation` | blocked until a measured method exists |

Time boxes (design, Budgets): G00 15 min · G01 40 · G02 40 · G03 40 · G04 45 ·
G05 30 · slack 30. G01 and G02 can start without G00's answer for everything
except rendering resolution; if G00 shows no image input, G01 marks visual
pages as unresolved and G03 uses manual facts (design F3).

### G00 — Confirm the key, model, image input and ADK interfaces

- **Outcome and linked decisions:** A1, D02, D08 settled with evidence: provider,
  model name, whether images are accepted, token price per unit (dated), and
  which ADK interfaces in the installed version carry image parts and
  structured output.
- **Scope:** read provider docs for the key; install pinned packages; one
  minimal text call and, if claimed, one minimal image call. Excludes any
  case processing.
- **Implementation route:** `pip install` of the proposed stack; a throwaway
  `scripts/probe.py` that sends one short prompt via ADK `Runner` and prints
  the usage metadata fields present in the event. Record versions in
  `docs/evaluation-summary.md` header.
- **Prerequisites:** the key in the environment; network.
- **Skills:** primary `adk-engineer`; supporting `adk-workflow-design` for
  the Runner invocation shape.
- **Acceptance:** a written row with provider, model, image support yes/no,
  price source URL and date, ADK version, and the usage fields observed.
  Failure case: no image support → F3 route recorded as the decision.
- **Verification:** bounded live; at most 2 calls; cost recorded in the ledger
  as the first entries.
- **Execution scope:** needs the user's go-ahead to install and spend
  (approximately cents).
- **Status and evidence:** planned.

### G01 — Ingest and qualify every page

- **Outcome and linked decisions:** D03, I5, A3. Every page of the five dev
  cases, five holdout cases, Local Plan and four SPDs has a density class,
  a route and an origin label in `data/ingestion/<document>.json`; routed
  pages are rendered to `data/ingestion/<document>/pages/<n>.png` at a
  resolution chosen from a sample; applicant contact fields are stripped
  from form text.
- **Scope:** text-layer extraction, qualification, calibration of thresholds
  on this corpus, rendering, written-dimension/scale extraction from drawing
  text layers. Excludes OCR engines and any model call.
- **Implementation route:** `ingest.py` builds the page inventory with
  `pypdf`; qualification follows the memory skill's `qualify_ingestion.py`
  (character count, alphanumeric ratio, table/drawing hints, reading-order
  anomalies); `pypdfium2` renders routed pages. Run the skill's four-page
  fixture first as a mechanism control.
- **Prerequisites:** supplied PDFs in `data/raw/`; renderer installed (G00).
- **Skills:** primary `adk-memory-architecture` (document-ingestion);
  supporting `protect-adk-sensitive-data` for the field-minimisation line.
- **Acceptance:** report covers 100% of pages; fixture pages route as
  `text`, `ocr_or_vision`, `both`, `both`; the pages around the chosen
  threshold were looked at and the threshold recorded; `visual_pages` per
  case listed with the cap applied and unread pages named; no applicant
  contact field appears in any stage-2 input file.
- **Verification:** offline; `pytest tests/test_ingest.py` (fixture routing,
  field stripping); manual spot-check of three scanned drawings.
- **Execution scope:** local, no spend.
- **Status and evidence:** planned.

### G02 — Index the policy corpus and retrieve by issue with measured recall

- **Outcome and linked decisions:** D04, I3 (retrieval side), A5. An FTS5 index
  of the Local Plan and SPDs chunked by policy unit with page spans and a
  screened-pages list; `retrieve.py` produces a per-case retrieval report
  (per issue: units with page spans or `none_found`; unresolved references;
  queries; second-round flag; budget); gold-set recall for the five dev
  cases recorded.
- **Scope:** chunker adapted to this plan's heading grammar; issue list per
  case derived initially by hand from the dev labels (material issues an
  officer raised), later from stage-2 facts; reference lookup for policy
  codes, tables and SPD names; one bounded second round. Excludes dense
  retrieval and reranking.
- **Implementation route:** `index.py` and `retrieve.py` following the memory
  skill's `local_retrieval.py` (`chunk_by_heading`, `screen_units`,
  `build_index`, `search_lexical`, `resolve_references`, `retrieve_for_issues`,
  `sufficiency_problems`). Gold set at `data/eval/retrieval-gold.json`,
  evaluator-only.
- **Prerequisites:** G01 corpus text; a Python whose SQLite has FTS5.
- **Skills:** primary `adk-memory-architecture` (retrieval-strategy).
- **Acceptance:** the skill's gold fixture passes; for this corpus, a case
  whose policy cites an SPD table returns that table or an explicit
  unresolved reference; recall per dev case recorded before drafting; four
  truncated searches without a second round is a failing case.
- **Verification:** offline; `pytest tests/test_retrieve.py`; recall printed
  to `docs/evaluation-summary.md`.
- **Execution scope:** local, no spend.
- **Status and evidence:** planned.

### G03 — Draft decisions end to end and baseline the five development cases

- **Outcome and linked decisions:** D02, D05, D06, D07, I2, I3, I4, I6. One
  CLI run (`cli.py run-dev --run-id baseline`) takes each dev case through
  facts → retrieval → draft → check → score; every call admitted by the
  budget and settled into the ledger; `docs/evaluation-summary.md` gets its
  baseline row with decision match, policy-ID overlap, unsupported citations,
  contract failures and spend.
- **Scope:** two `LlmAgent`s (facts with image parts for routed pages; draft
  with the quality-iteration prompt skeleton and two leave-one-out exemplars),
  `Decision` schema, citation resolution, deterministic scorer, budget with
  reserve partition, run records with config hash. Excludes iteration and
  the holdout.
- **Implementation route:** `facts.py`, `draft.py` via `Runner` with
  `InMemorySessionService`, `RunConfig(max_llm_calls=…)` per invocation;
  `check.py` validates with `pydantic` and resolves each `policy_id` against
  the retrieval report; `budget.py` enforces per-case cap 6 calls, dev
  allowance $15-equivalent at the G00 rate, reserve $7 untouchable by
  `run-dev`; `score.py` writes `data/eval/defects.jsonl` rows per defect.
  If the installed ADK makes image parts or structured output awkward, a
  direct SDK call for that stage is the labelled fallback (D02).
- **Prerequisites:** G00 (model, usage fields), G01 (routed pages), G02
  (retrieval report); issue extraction from stage-2 facts or hand-written
  issue list per case.
- **Skills:** primary `adk-workflow-design`; supporting
  `adk-operational-guardrails` (budget), `adk-agent-evaluation`
  (prompt skeleton, scorer, exemplar rule).
- **Acceptance:** all five dev cases produce `decision.json` or a recorded
  `contract_failure`; no exemplar equals the case under test (unit test);
  a decision citing an unknown policy is flagged (unit test); ledger total
  within the dev allowance and reserve untouched; stubbed-model test runs
  the stage order and writes every stage file; restart with existing stage
  files re-uses them.
- **Verification:** offline `pytest` for order, exemplars, citation check,
  schema, budget denial; bounded live run of five cases with every call in
  the ledger.
- **Execution scope:** live spend inside the dev allowance; needs the user's
  go-ahead for the build session.
- **Status and evidence:** planned.

### G04 — Error analysis and one-change iterations

- **Outcome and linked decisions:** D06, Q1. Each dev output read against its
  label and every defect labelled by category; the largest category names
  one change (prompt, retrieval parameter, exemplar choice, schema or model,
  never several); re-run, re-label, keep or revert; a summary row per
  iteration with counts before/after and the case IDs that moved.
- **Scope:** as many iterations as the 45-minute box and the dev allowance
  permit (expected one or two). Contract failures are fixed before any
  quality change is judged. Excludes a stronger-model comparison unless the
  first iteration's largest category is `wrong_outcome` with retrieval and
  facts intact.
- **Implementation route:** `score.py` + hand-labelled `defects.jsonl`;
  config versioning so each iteration has its own hash and run directory.
- **Prerequisites:** G03 baseline row.
- **Skills:** primary `adk-agent-evaluation` (quality-iteration);
  supporting `adk-memory-architecture` if the change is retrieval.
- **Acceptance:** each iteration row names one change and shows the targeted
  category shrinking with no other category growing, or records the revert;
  ledger within allowance; reserve untouched.
- **Verification:** bounded live runs; summary rows; defects file.
- **Execution scope:** live spend inside the remaining dev allowance.
- **Status and evidence:** planned.

### G05 — Freeze the method, run the holdout, write the report

- **Outcome and linked decisions:** D09, I1. The best measured method's
  config hash is frozen; `cli.py run-holdout --config-hash <hash>` runs the
  five holdout cases from the reserve; predictions copied to
  `deliverables/holdout-predictions/`; `deliverables/report.md` (under two
  pages) describes what was built, how it was checked (dev score by
  category, retrieval recall, ingestion coverage, spend) and limits (largest
  remaining category, unread pages, manual steps, five-case generalisation
  caveat, assumptions A1–A5).
- **Scope:** holdout run, report, final summary row. Excludes any method
  change after the freeze unless regenerated from remaining reserve.
- **Implementation route:** `cli.py run-holdout` refuses a hash mismatch;
  run record stores hash, model, prompt version, timestamps; report cites
  the hash.
- **Prerequisites:** a measured method (G04, or G03 if time ran out, stated
  as such).
- **Skills:** primary `adk-agent-evaluation` (progressive validation:
  deliverable and method together).
- **Acceptance:** five prediction files exist with the frozen hash in their
  run record; the report's hash matches; ledger shows the holdout run drew
  only on the reserve; the report is under two pages and names the limits.
- **Verification:** live (reserve); file and hash comparison.
- **Execution scope:** live spend from the reserve only.
- **Status and evidence:** planned.

## What the reviewer reads

| Document | Establishes |
| --- | --- |
| `deliverables/report.md` | Method, checks, limits (what the brief asks for); cites the frozen config hash |
| `docs/evaluation-summary.md` | Latest result per dev case and per iteration, retrieval recall, ingestion coverage, spend; links to `data/runs/` and `data/eval/` |
| `docs/plans/planning-assistant.md` (this plan) with the design | Accepted and assumed decisions, deferred controls, remaining limits |

Raw run records, the ledger, defects and ingestion reports are data under
`data/`; they are linked from the summary, never read as documents.

## Open decisions for further planning

| Decision / question | Known facts and alternatives | Evidence or user decision needed | Blocks which goals? |
| --- | --- | --- | --- |
| A1 provider, model, image input | Brief says "one model API key"; ADK binds Gemini natively, others via LiteLLM or direct SDK | G00 probe + provider docs | G03 (binding), G01 (rendering only) |
| A4 price per token | Unknown; drives iterations affordable and the visual page cap | G00, dated price page | G03/G04 sizing |
| A5 heading grammar of the Local Plan | Policy-code headings expected; page-window fallback otherwise | G02 inspection of extracted text | G02 chunker |
| Standard-conditions library | None supplied; dev labels may show recurring condition wording that can be turned into data | G03 reading of the five labels | G03 prompt inputs |
| Q1 provisional quality target 4/5 | Not in the brief; five cases cannot show generalisation | Builder's judgment | G05 freeze timing |
| ADK installed-version interfaces for image parts and structured output | Handoff reference names checked 25 Sep 2026; not checked against an installed version | G00 | G03 fallback to direct SDK calls |
| Scorer scope for reasons | Automatic policy-ID overlap only if labels cite codes; otherwise manual categories only | G03 reading of labels | G03/G04 |

## Resume here

- **Next goal:** G00 — Confirm the key, model, image input and ADK
  interfaces. Ready because it has no prerequisites and its answer sets the
  render decision in G01 and the binding in G03. G01 can start in parallel
  for everything except rendering.
- **Read first:** the design at `docs/architecture/planning-assistant.md`
  (assumptions A1–A5, deferred controls, invariants I1–I6); this plan; the
  brief at `../brief.md`.
- **Next action:** read the provider documentation for the supplied key,
  install the pinned stack, run one minimal text call through the ADK
  `Runner`, record provider, model, image support, price source and the usage
  fields observed as the first row of `docs/evaluation-summary.md`.
- **Continuation prompt:**

```text
Use adk-engineer to continue G00 "Confirm the key, model, image input and ADK
interfaces" from docs/plans/planning-assistant.md.
Read docs/architecture/planning-assistant.md and preserve its assumptions
A1–A5 and deferred-controls table; treat every decision as proposed, not accepted.
Use adk-engineer with adk-workflow-design for the Runner probe.
Work within the workspace only, with at most 2 model calls charged to the
development allowance; verify provider, model, image support, price source
and ADK usage fields, and update the plan's G00 status with actual evidence.
Then start G01 with adk-memory-architecture (document-ingestion reference),
offline, no model calls.
```
