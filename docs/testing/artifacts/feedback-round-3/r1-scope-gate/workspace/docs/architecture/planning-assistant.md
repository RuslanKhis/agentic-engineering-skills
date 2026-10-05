# System design: planning assessment assistant

Status: **draft** — one-pass design with explicit assumptions; the user was not
available for the design conversation, so every material product choice below
is a proposal (P) or a labelled assumption (A), not a user-accepted decision.
Companion plan: [docs/plans/planning-assistant.md](../plans/planning-assistant.md).

## Purpose and constraints

**Users and journey.** A planning case officer receives a householder
application (form, site plan, elevations, optional supporting statement) and
must write a decision: approve or refuse, the reasons, and any conditions,
grounded in the council's Local Plan and its supplementary planning documents
(SPDs). The friction today is the reading: finding the operative policies for
each material issue in ~300 pages of plan plus four SPDs, reading drawings
that are sometimes scans, and writing reasons that cite the right provision.
The useful result is a draft decision an officer could sign with light edits,
where every cited policy resolves to a real passage and every stated fact
traces to a page of the application.

**Running example.** A rear extension on a semi-detached house: the drawings
show the extension depth and height, the Local Plan's residential-extensions
policy sets a depth limit and an amenity test, an SPD gives the 45-degree
rule; the officer must say whether the depth criterion is met, by which
drawing, and attach a materials condition if approving.

**What is judged.** Five holdout predictions (scored), the method, and a
report under two pages describing what was built, how it was checked and its
limits (brief, `../brief.md`).

**Observed facts (from the brief).** Five labelled development cases with the
officer's decision, reasons and conditions. Five unlabelled holdout cases.
Local Plan ~300 pages PDF; four SPD PDFs; some application drawings are
scans. One model API key with a $25 allowance. Three to four hours.

**Assumptions (A).** Each is revisited in [Open decisions](#open-decisions).

| ID | Assumption | Why it is needed now |
| --- | --- | --- |
| A1 | The API key is for a Gemini-family model with image input (ADK's native backend). If it is another provider, ADK's LiteLLM route or a direct SDK call replaces the model binding; the pipeline is unchanged. | Decides the ADK model binding and whether scans can be read without a separate OCR install. |
| A2 | The builder runs everything locally on their own machine; no hosting, no end users, no login. | Removes identity, delivery and deployment work from the slice. |
| A3 | The supplied materials may be sent to the model under the key's terms. Applicant contact fields on the form are not needed for the decision and are dropped in code before any model call (cheap, kept). | Sensitive-data boundary at the only ingress. |
| A4 | Model prices are unknown at design time; spend is controlled by call and token counts with a configurable rate, and the actual rate is recorded on the day. | The $25 allowance must be enforced by the application, not observed after the fact. |
| A5 | The Local Plan has a heading grammar (policy codes such as "Policy H3") usable for chunking. If not, page-window chunking is the fallback and recall is expected to be worse. | Chunking strategy for retrieval. |

**What the model contributes vs ordinary code.** The model reads drawings and
forms into structured case facts, and weighs policy against facts to draft the
decision. Ordinary code owns everything it can already know: page routing,
chunking, policy-reference lookup, citation resolution, exemplar selection
(leave-one-out), schema validation, scoring against labels, spend accounting
and the stop.

## Scope, evaluator and deferred controls

| Scope-gate answer | Value |
| --- | --- |
| Time and money available | 3 to 4 hours wall-clock, one builder. $25 API allowance, of which a **reserve for the final holdout run** is set aside before any experiment (P: $7 reserve, $3 contingency, $15 for development runs; symbolic until the rate is known, see [Budgets](#budgets-and-capacity)). |
| Who judges the result and what they read | Assignment reviewers. They read: five holdout predictions, the method, a report under two pages. They do not run the system. |
| Artifact type | **Assignment.** Not a pilot or production service. |

Under the proportionality rule, the first and only slice is the core judgment
end to end on the real supplied inputs, measured on the five development
cases, with only the controls that keep spend safe. Everything else waits:

| Deferred control | Why it waits | What would bring it forward |
| --- | --- | --- |
| Officer revision workflow (edit, re-draft, accept) | No officer uses this; the reviewer reads predictions. | A pilot with real officers. |
| Export / acknowledgement of a decision record | No downstream system consumes the decision. | Integration with a case-management system. |
| Saved-stage recovery and checkpoint freezes | Stage outputs are plain files on disk for inspection; a formal resume contract costs time the slice does not have. | More than ~20 cases, or runs long enough that a crash loses more than a few minutes. |
| Identity, session ownership, multi-user state | Single builder, local run (A2). | Any hosted or shared use. |
| Cloud hosting (Cloud Run / Agent Runtime / GKE) | Nothing is served; the deliverable is files. | A demo or service requirement. |
| LLM judge for reason quality | Spends budget and time; five dev cases can be read by a person in minutes. | A development set too large to read by hand. |
| Semantic memory / cross-session recall | Each case is independent; nothing needs to persist across cases. | An officer workload with recurring applicants or sites. |
| Dense/hybrid retrieval, reranking | Lexical FTS with deterministic reference lookup first; measured on the gold set. | Gold-set recall below target after the one bounded second round. |
| Sensitive-data inspection service (SDP / Model Armor) | Field minimisation in code (A3) is the proportionate boundary for supplied assignment materials. | Real applicant data under a data-protection obligation. |
| Parallel case processing | Five plus five cases run sequentially within the time box; parallelism complicates spend accounting. | Case volume that does not fit the time box sequentially. |

## Guarantees and acceptance

| Invariant or target | Enforcing component and authoritative evidence | Failure outcome | Planned verification |
| --- | --- | --- | --- |
| I1 **Deliverable integrity.** The five holdout predictions submitted are produced by the frozen final method the report describes. | `run_holdout` entrypoint runs only with a frozen config hash; `data/runs/holdout-final/` records config hash, prompt version, model, timestamps. | If the method changes after the holdout run and budget or time forbid regeneration, the report states this explicitly. | Compare config hash in holdout run record with the hash the report names. |
| I2 **No label leakage.** Holdout cases have no label anywhere in the system; a development case never sees its own label (leave-one-out exemplars). | `exemplars_for(case_id, labelled)` in ordinary code; holdout label files do not exist. | Any exemplar whose ID equals the case under test fails the run before the model call. | Unit test: for every dev case, the exemplar set excludes its own ID; for every holdout case, the exemplar set is drawn only from the five labelled cases. |
| I3 **Citations resolve.** Every `policy_id` in a reason resolves in code to a retrieved unit with document and page span, or the reason is marked `unsupported`. | `resolve_citations` after drafting, against the retrieval report for that case. | Unsupported citation stays in the output, flagged; it counts in error analysis as `unsupported_fact` or `wrong_attribution`. | Unit test with a drafted output citing a policy not in the retrieval report → flagged. On the dev set: count of unsupported citations per case recorded. |
| I4 **Spend stays within allowance.** Per-case call cap and a total stop, with the final-run reserve excluded from the development allowance. | `Budget` object checked before each model call; usage ledger appended after each call; `RunConfig.max_llm_calls` as a second bound per invocation (version check needed). | When the development allowance is exhausted, the run stops cleanly, outputs so far are retained, and the reserve remains for the holdout run. | Unit test: ledger at the cap denies the next call. Live: the dev-set run record shows calls and estimated spend per case. |
| I5 **Every page has a route.** Each page of each case and of the policy corpus has a density class, a route (`text`, `ocr_or_vision`, `both`) and its text carries an origin label; low-density pages are never passed as text. | Ingestion report per case (`data/ingestion/<case>.json`) from the qualification step. | A page without a route blocks that case from drafting. | Offline: run qualification on the corpus; check that every page appears in the report; spot-check the pages around the threshold. |
| I6 **Structured output or contract failure.** The drafting output validates against the decision schema; a failed validation is retried once and then recorded as `contract_failure`, excluded from the quality denominator. | Pydantic schema validation in ordinary code after the model call. | Case output is marked `contract_failure` with the raw response retained. | Unit test with malformed JSON; dev-run record shows contract failures separately from decision defects. |
| Q1 **Quality target (provisional).** Decision (approve/refuse) matches the officer on at least 4 of 5 development cases, and cited policy IDs overlap the officer's reasons. | Deterministic scorer against labels; manual category labels. | Below target after the time-boxed iterations: report the score and the largest remaining defect category. | Living evaluation summary, one row per iteration. **Provisional:** 4/5 is a labelled assumption, not a brief requirement; five cases cannot establish generalisation. |

## Architecture and decisions

```
supplied files ──► [1] Ingest & qualify ──► ingestion report (per case, per corpus doc)
   (PDFs, scans)        (pypdf + render)          │ routes: text / vision / both
                                                  ▼
                                    [2] Case facts (model, vision on routed pages)
                                        → case_facts.json  {fact, source page, origin}
                                                  │
 Local Plan + SPDs ──► [3] Index (FTS5 by policy unit, page spans)
                                                  │
                                    [4] Retrieve by issue + resolve references
                                        → retrieval_report.json {issue → units | none_found}
                                                  │
                                    [5] Draft decision (model) with 2 leave-one-out exemplars
                                        → decision.json  {decision, reasons[], conditions[], uncertainties[]}
                                                  │
                                    [6] Validate schema, resolve citations, score vs label (dev only)
                                        → scored.json, defects.jsonl, evaluation-summary.md
                                                  │
                              Budget ledger (checked before 2 and 5; total stop; reserve)
```

All stages are ordinary Python code run sequentially per case from one CLI
entrypoint. Stages 2 and 5 are the only model calls. There is no gateway,
session store, approval or external write.

| ID | Requirement | Design choice | Reason | Tradeoff / alternative | Verification and expected result |
| --- | --- | --- | --- | --- | --- |
| D01 (P) | Judged on holdout predictions, method and a short report in 3–4 h | First slice = core judgment end to end on the real inputs, scored on the dev set, holdout regenerated with the frozen method; nothing else. | Proportionality rule: output quality is what is scored; infrastructure that does not change a prediction is wasted time. | Forgoes a demo UI or hosted service that could impress but is not judged. | The plan has no goal that is not on the path to a prediction or the report. |
| D02 (P) | Known fixed ordering of stages; two language steps | Ordinary code orchestration; two ADK `LlmAgent`s (fact extraction, drafting) run through `Runner` with `InMemorySessionService`; no workflow agent, no reviewer agent, no loop. | The ordering is known; a sequential workflow agent adds nothing. Two agents are justified by distinct inputs (images vs retrieved text) and distinct output schemas. | Direct model-SDK calls would be marginally simpler; ADK gives `RunConfig.max_llm_calls`, event traces and a path to later specialists. If ADK's current version complicates image input or structured output, fall back to direct SDK calls for that stage and say so in the report. | Offline: stage order test with stubbed model. Live: one dev case produces a `decision.json` with traces retained. |
| D03 (P) | Some drawings are scans; facts must trace to a page | Ingestion qualification per page (density class, route, origin label) before any model call; scans and drawings are rendered and sent as images to the model's vision input; text pages sent as text. | A scan's empty text layer silently yields "no facts"; routing makes unread pages visible as unresolved evidence rather than absence. | A separate OCR engine (e.g. Tesseract) avoids image tokens but needs an install and gives no drawing understanding; vision spends budget per page. Visual pages are capped per case (see Budgets). | Ingestion report for every case; pages left unread listed. Fixture: the skill's four-page ingestion fixture routes as expected. |
| D04 (P) | Reasons must cite the operative policy among ~300 pages + 4 SPDs | Local SQLite FTS5 index chunked by policy unit (heading to next heading, page spans kept); one query per material issue; every named reference (policy code, table, SPD) resolved by exact lookup in code; one bounded second round; retrieval sufficiency report to the drafter. | Exact policy codes and numbers are what lexical search finds well; deterministic lookup removes the model's need to remember policy numbers; sufficiency report lets the drafter decline rather than invent. | A cloud RAG service costs setup time and adds nothing at this corpus size. Dense/hybrid retrieval deferred until gold-set recall shows a miss. | Gold set: for each dev case the units a reviewer would cite; recall recorded before drafting and after any retrieval change. |
| D05 (P) | Draft an officer-quality decision with reasons and conditions | Prompt in the quality-iteration skeleton: role, the judgment owned, labelled inputs (facts with source IDs, policy text per issue or `none_found`), schema sized to the decision, two leave-one-out exemplars trimmed to reasons and conditions. | Exemplars carry structure and tone; code supplies IDs, quotes and coverage so the prompt stays about the judgment. | A longer rule-laden prompt would be faster to write but harder to debug; standard-conditions library would help but none is supplied (see Open decisions). | Schema validation; citation resolution; dev-set score. |
| D06 (P) | Measure quality within the time box | Deterministic scorer (decision match; policy-ID overlap; condition count) plus manual defect labels by category (`missed_policy`, `wrong_attribution`, `unsupported_fact`, `weak_condition`, `wrong_outcome`, `contract_failure`); one change per iteration; living summary. | Five cases are readable by hand; an LLM judge would spend budget and need its own calibration. | Manual labelling is subjective; mitigated by fixed categories and recording the detail per defect. | `data/eval/defects.jsonl` and `docs/evaluation-summary.md` with a row per iteration. |
| D07 (P) | $25 allowance; must not be exceeded; final run must be affordable | Application-enforced `Budget`: per-case call cap (P: 6), per-case token cap, total development allowance, separate holdout reserve; checked before each call; ledger on disk; operator stop = delete the key from the environment. | Billing alerts are observations, not caps; the application must refuse admission itself. | Counting calls and tokens with an assumed rate is approximate; the ledger records tokens so the actual spend can be reconciled from the provider console. | Unit test: cap denial. Dev run: ledger totals under allowance. |
| D08 (A1) | One model key, provider unstated | Bind ADK to the key's provider; prefer a model with image input for stage 2. Record model name, settings and prompt version with every run. | Vision input removes the need for an OCR install. | If the key's model lacks vision, stage 2 falls back to text-layer only and scans become manual-transcription tasks (see failure F3). | First discovery goal (G00) confirms provider, model and image support from the provider's documentation and one tiny call inside the budget. |
| D09 (P) | Report must describe the method that produced the predictions | Freeze rule: the holdout run uses a frozen config hash; any later method change either regenerates the holdout (from reserve) or is stated as not applied. | Keeps deliverable and method together for the reviewer. | Regeneration costs reserve budget; the reserve is sized for exactly one holdout run. | Run record carries the hash; report cites it. |
| D10 (A2) | No users, no hosting | No identity, session persistence, streaming or deployment. | Nothing is served. | A later pilot restarts those decisions from the deferred-controls table. | None needed. |

**Runtime, model backend, data services.** Application runtime: a local Python
process (CLI). Model backend: the supplied key's provider (A1). Data services:
the local filesystem (`data/`) and an SQLite FTS5 file. No GCP services are
used in the slice; the GCP decisions reference applies only if hosting is
later brought forward. ADK interface names (`LlmAgent`, `Runner`,
`InMemorySessionService`, `RunConfig.max_llm_calls`) were checked against the
skill's handoff reference dated 25 September 2026 and still need checking
against the ADK version actually installed on the day.

## Data and authority

| Data / operation | Owner and authorized scope | Writers / readers | Source and freshness | Lifetime / erasure |
| --- | --- | --- | --- | --- |
| Supplied case PDFs (dev + holdout) | Builder, local disk; read-only | Read by ingestion only | As supplied; never modified | Kept for the assignment; deleted with the workspace |
| Labels (dev only) | Builder; evaluator-only | Read by scorer and exemplar selector (leave-one-out); never by the case under test | As supplied | Same |
| Ingestion reports | Pipeline | Written once per document; read by stages 2–6 and the report | Derived from supplied PDFs; regenerated if thresholds change | Same |
| Case facts | Pipeline (model output, labelled by origin) | Written by stage 2; read by 4–6 | Per run; tied to run ID and config hash | Same |
| Policy index + gold set | Pipeline / builder | Index built once; gold set written by the builder by hand, read by the evaluator only | Local Plan + SPDs as supplied | Same |
| Retrieval reports | Pipeline | Written by stage 4; read by 5–6 | Per run | Same |
| Decisions, scores, defects, ledger | Pipeline / builder | Written per run; read by the evaluation summary and report | Per run, run ID + config hash | Same |
| API key | Builder | Read from environment by the model client only; never logged or written to `data/` | — | Removed from the environment to stop all spend |

Identities: one builder, one local process, one provider key. No end-user
identity, delegated OAuth or approval exists. Public output is a file; nothing
streams. Applicant contact fields are dropped in code before any model call
(A3); drawings and site addresses are sent because the decision depends on
them.

## Budgets and capacity

Workload: ten cases total, processed sequentially; development runs repeat the
five dev cases per iteration. No concurrency, no latency target beyond the
time box.

**Calls per case (bounded).** Stage 2: `ceil(visual_pages / images_per_call)`
calls, with `visual_pages` capped (P: 6 pages per case, drawings first, then
tables, then scanned form pages; pages over the cap are listed as unread).
Stage 5: one drafting call, one retry on schema failure. Per-case cap: 6
calls. Expected: 2–4 calls per case.

**Symbolic spend model (illustrative, not a bill).**

```
dev_iteration_cost   = 5 cases × calls_per_case × (prompt_tokens + image_tokens + output_tokens) × rate
holdout_run_cost     = 5 cases × same
allowance            = $25 = dev_allowance ($15) + contingency ($3) + holdout_reserve ($7)
iterations_affordable = floor(dev_allowance / dev_iteration_cost)
```

Fill with the key's published rate and the measured token counts from the
first dev case (G00/G03) and record the date. If one iteration costs more than
a third of the development allowance, reduce `visual_pages` cap or trim
exemplars before trying a stronger model. The reserve is never drawn on by a
development run; the budget object enforces that separation.

**Time budget (3–4 h).** G00 15 min · G01 40 min · G02 40 min · G03 40 min ·
G04 45 min · G05 30 min · slack 30 min. If G01+G02 overrun by more than
30 minutes, the fallback is text-layer-only facts plus a hand-transcribed
facts file for scanned drawings, stated in the report.

**Exhaustion and restart.** When the development allowance is spent, the run
stops after the current call; per-case outputs so far remain on disk; the
holdout reserve remains. A process restart re-runs a case from its last
written stage file (plain file reuse, not a recovery contract).

## Failure and recovery

| Failure window | User-visible outcome | Retained state / possible effects | Safe next action and recovery owner |
| --- | --- | --- | --- |
| F1 Successful case | `decision.json` with reasons, conditions, uncertainties; citation check passed; ledger updated | All stage files for the case under the run ID | Score (dev) or collect (holdout); builder |
| F2 Scanned page not legible to the model / vision returns nothing usable | Facts for that page absent; page listed as `unresolved_evidence` in the ingestion report; drafter's `uncertainties[]` names the missing fact | Rendered page, model response retained | Builder transcribes the needed dimensions by hand into a labelled `manual_facts.json` (origin `manual`) and re-runs stage 5 only; report states the manual step |
| F3 Key's model has no image input (A1 false) | Stage 2 runs on text layers only; every routed visual page becomes unresolved evidence | Same | Same as F2 for all scanned drawings, or install an OCR engine if time allows; this is a G00 decision, not a mid-run surprise |
| F4 Malformed or truncated drafting output | One retry; then `contract_failure` recorded for the case | Raw response retained | Fix the schema/prompt contract before any quality change; excluded from quality denominator |
| F5 Retrieval finds nothing for an issue after the second round | `none_found` reaches the drafter; the decision may still be drafted with the issue in `uncertainties[]` | Retrieval report with queries run and budget used | Error analysis labels `missed_policy`; next iteration changes one retrieval parameter or the query vocabulary, measured on the gold set |
| F6 Development allowance exhausted mid-iteration | Run stops; summary row marks the iteration partial | Completed cases retained; reserve intact | Builder decides: trim the per-case cost and rerun remaining cases, or freeze the previous iteration's method |
| F7 Time box ends before the planned iterations | Freeze the best measured method; run holdout from the reserve; report the shortfall | All run records | Builder; the report names the largest remaining defect category |
| F8 Method changed after the holdout run | Reviewer would otherwise read predictions from an undescribed method | Holdout run record with config hash | Regenerate from reserve if affordable; otherwise the report states that the predictions came from the earlier hash and what changed after |
| F9 Provider outage or rate limit | Bounded retry (P: 2 attempts, short backoff) then stop the run | Ledger counts attempted calls | Builder resumes later from the last stage file |

Not applicable, with reason: denied user or cross-tenant access (no users);
provider commits but reply lost (no external writes); approval or entitlement
changes (no approvals); forget/revoke races (no memory, no credentials beyond
the key); rollout/rollback (nothing deployed); cleanup of cloud resources
(none created; delete the workspace and the key).

## Verification and implementation handoff

**Offline deterministic checks** (no model calls): page routing on the
skill's ingestion fixture and on sampled corpus pages; chunking yields units
with page spans and screened contents pages; reference lookup resolves a known
policy code; leave-one-out exemplar selection; citation resolution flags an
unknown policy ID; schema validation rejects malformed output; budget denial at
the cap; stage ordering with a stubbed model.

**Local integration evidence:** one full dev case through all stages with a
stubbed model produces every stage file; restart re-uses existing stage files.

**Bounded live checks** (inside the development allowance): G00 tiny call to
confirm provider/model/vision; G03 baseline run over the five dev cases with
every call logged in the ledger; one or two iterations in G04.

**Final deliverable run:** G05 holdout run from the reserve with the frozen
config hash, regenerated if the method changes.

**Model quality vs product usefulness.** Decision-match and policy-ID overlap
on five dev cases is a quality measurement, not evidence that an officer would
sign the draft; the report says so. Generalisation is a hypothesis until the
holdout is scored by the reviewer.

**Deliverable rule.** The reviewer judges `deliverables/holdout-predictions/`
and `deliverables/report.md`. Both are produced by the method the report
describes (I1, D09); the holdout reserve is set aside before the first
experiment.

**Implementation map and goals:** see the
[implementation plan](../plans/planning-assistant.md). All modules are
proposed (greenfield); no path has been inspected because the workspace is
empty.

## Open decisions

| Question or assumption | Why it changes the design | Owner / evidence needed | What it blocks |
| --- | --- | --- | --- |
| A1 Which provider and model does the key unlock, and does it accept images? | Vision vs OCR route for scans; ADK binding vs LiteLLM/direct SDK | Builder; provider docs for the key + one tiny call (G00) | G01's render decision, G03 |
| A4 Actual model price per token | Number of affordable iterations; visual page cap | Builder; provider price page, dated | Sizing in G03/G04 (not G01/G02) |
| A5 Does the Local Plan have a usable heading grammar? | Unit chunking vs page-window fallback; expected recall | Builder; inspect the extracted text of ~10 pages (G02) | G02 chunker choice |
| Is there a standard-conditions library in the SPDs or dev labels? | Conditions are the weakest category in first runs; a library as data improves them cheaply | Builder; read the dev labels' conditions (G03) | Prompt design in G03 |
| Q1 Is 4/5 decision match the right provisional target? | Decides when to stop iterating and freeze | Builder's judgment; no brief requirement exists | Freeze decision in G05 |
| What does the ADK version installed on the day expose for image input and structured output? | Whether stage 2/5 use `LlmAgent` or direct SDK calls | Builder; ADK docs for the installed version (G00) | D02 fallback choice |
| Are the dev labels' reasons structured enough to score policy-ID overlap automatically? | Deterministic scorer vs manual-only labelling | Builder; read the five labels (G03) | Scorer scope in G03 |

No decision in this document has been accepted by the user. Design review is
complete when each invariant above has an owner/mechanism/test or an explicit
gap; it is not evidence that anything has been implemented or tested.
