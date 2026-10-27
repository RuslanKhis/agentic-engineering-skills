# Planning decision assistant: design and plan (DRAFT, one-pass, unreviewed)

Profile: **time-boxed assignment judged on output.** Judged on five holdout predictions, the method and a short report. Phase 1 is the core judgment end to end, measured on the five labelled development cases; nothing else is built before that measurement exists. Design only: nothing here is built, installed or run.

## 1. Constraints, assumed answers and depth

Nobody can answer in this session, so each scope-gate question has an assumed answer. Decisions that depend on one are provisional.

| Question | Assumed answer | Depends on it |
| --- | --- | --- |
| Deadline, continued afterwards? | 3 to 4 hours, one sitting; not continued | Phase 1 size; no hardening phase |
| Who builds, ADK familiarity? | One developer with a coding agent; comfortable with ADK, so no 1.5x multiplier | Estimates; if new to ADK, G2 rises and the cut order in section 5 applies |
| Money | $25 model allowance; self-imposed stop at about $5 for the whole build | Model tier, repeat runs (C4) |
| Judge and reading | Five holdout predictions, method, short report (about 2 pages) | G4, G5; no UI |
| Interface, handover | Command-line script; `adk web` on loopback only if useful; not handed over | No hosting or identity |
| Data, effects | Synthetic text extracts; read only; writes only to `out/` | Floor items below |
| Presentations, SoW, lock-in | None; the report is the artefact | No presenter, SoW or portability goal |
| Model provider and ID | **Unknown.** Provisional: one pinned ID, chosen at G1. The dated model lifecycle table is not in this workspace, so no ID is chosen from memory | D6 |
| Installing `google-adk` at build time | **Unknown.** Assumed to be authorized in a venv inside this directory when the build starts. If not, the build stops after G1 | G2 onward |

Written-down questions for the user: (a) which model provider and ID is the $25 for; (b) may `google-adk` be installed in a local venv; (c) is there a required report format; (d) how will reasons be judged, by policy cited or by wording; (e) are the standard conditions (see D4) expected on every approval.

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Core judgment, measured | Build: 5 dev cases, leave-one-out | n/a |
| Spend and loop limits | Build: call cap and total stop (C4) | n/a |
| Retrieval over the plan | Defer: whole pack in the prompt (D2) | Real PDFs, or a pack over about 20 pages |
| Identity, hosting, frontend | Defer | Anyone else uses it |
| Observability, CI gate, release engineering | Defer; pinned model ID only | Continued after the assignment |
| Officer revision workflow, export acknowledgement, recovery | Defer | A real officer uses the drafts |
| Governance pack | Defer: synthetic data, drafts for an officer | Real applications or applicant data |

Floor kept: no secrets in source or logs, a spend stop, a pinned model ID, output labelled "draft for officer review", no sending.

## 2. Journey and shape

An officer opens a case (application text plus supporting documents), and the assistant drafts approve or refuse with policy-cited reasons and conditions, which the officer would check against the plan. Today that is a manual read of the application, documents and plan. The label format is `decision`, `reasons[]`, `conditions[]`.

The model reads and applies the policy: thresholds, exceptions, and which documents bear on them. Code does everything else: loads the case, supplies the plan text, validates the output, caps calls, scores and writes files. One `LlmAgent` with an output schema, driven by a plain Python runner. No multi-agent graph: a single read-and-apply step has nothing a second agent could own or measure separately.

## 3. Contracts and decisions

| ID | Invariant (scope: every case run) | Enforced by | Check |
| --- | --- | --- | --- |
| C1 | Each reason cites a policy ID present in the pack (H3, H4, T2, HE1, D5, SPD s4 or Table 2) | Validator after the model, one retry, then flagged "unvalidated" in the output | Unit test with a made-up ID |
| C2 | Output has `decision` in {approve, refuse}; refuse has at least one reason; optional `uncertainty_notes` is never scored | Output schema plus validator | Unit test on malformed output |
| C3 | Output is a draft; nothing leaves the machine except the model call; writes only under `out/` | Runner code, one write path | Directory listing after a run |
| C4 | At most 3 model calls per case and 150 per session; the run stops past either | `RunConfig.max_llm_calls` plus a counter in the runner | Run with the cap set to 1 and see the stop |
| C5 | Dev scoring excludes the scored case from the exemplars; holdout never informs a change; holdout predictions come from the final method, with the config hash recorded | Runner flag, a `holdout` command that refuses to run before G3 closes, hash in the output | Dev score re-run matches; hash in the file |

Decisions (requirement, contract, choice, tradeoff, check):

- **D1** One agent plus ordinary code (C2, C4). Tradeoff: no specialist agents; none is needed at this size. Check: G2 baseline.
- **D2** No retrieval: the whole plan and SPD extracts (about 350 words) go in the instruction (C1). Tradeoff: does not scale to the real PDFs, and the Table 2 extract is known to be damaged, so the measure says nothing about PDF reading. Check: C1 test.
- **D3** The model does the arithmetic (parking, gap, setback) first; a calculator is added only if dev errors show arithmetic faults. ADK structured output may block tools on the same agent, so confirm against the pinned version before choosing. Check: the G3 error table.
- **D4** Conditions: the policy text yields some (D5: tree protection plan when works are in the root protection area). The "begin within three years" and "materials to match" conditions appear only in the dev labels (all 3 approvals carry the first; none of the 2 refusals carry any), not in the pack. They enter as a labelled assumption taught by exemplars, not a policy fact. Check: scored per case.
- **D5** Scoring is deterministic: decision exact match, cited policy-ID set against the label, condition keys against the label; reason wording is read by hand. With 5 cases, one case is 20 points, so the report gives a per-case table and 3 repeats per case, never one percentage. No LLM judge.
- **D6** One pinned model, temperature 0, strongest tier the allowance covers: about 10 cases, 3 repeats and about 10 iterations is a few hundred short calls, so spend is no constraint; time is (C4, C5). Provisional until the ID is chosen.

Leave-one-out matters because the 5 labelled cases are both the only exemplars and the only measure. Reusing them as exemplars on themselves would score memory.

Known coverage gap, derived from the pack alone: the dev cases never exercise the H4 front-slope rule, T2 with no bus reduction, the SPD splay rule on a classified road, or the detached 6.0 m limit with its no-material-loss exception. G3 may add up to five probe cases written from the policy text. They are author-labelled, so they are smoke tests reported separately and never counted in the score.

Disclosure: while scoping I opened the holdout application files to see their shape. I recorded no predictions and will not tune against them; there are no holdout labels to tune against anyway.

## 4. Failure grid

One external system, the model API. Slow or unavailable: the runner retries once, then records the case as "no prediction" rather than guessing (G2 test). Rejects or returns malformed output: C2 validator, one retry, then flagged. Outcome unknown: not applicable, because there are no writes beyond local files.

## 5. Plan (hours by hand, one person, quarter hours)

Phase 1 goals in order; each is end to end and leaves something usable.

- **G1 Scaffold, loader, scorer, caps** (C2, C3, C4). 0.5 to 0.75 h. Primary skill `adk-agent-evaluation`. Acceptance: loader reads all 10 cases; scorer returns per-case decision, policy-ID and condition matches on the labels (given the label as the prediction, it scores 5/5); the cap test stops a run. Run prompt: `/adk-engineer Carry out G1 from docs/architecture/planning-decision-assistant.md.` Status and evidence: empty.
- **G2 Agent v0 and baseline** (C1, C2, D1, D2). 0.5 to 0.75 h. Primary skill `adk-agent-evaluation`; model contracts from `adk-model-and-output-contracts` if installed. Acceptance: leave-one-out run over the 5 dev cases, 3 repeats, per-case table saved as M1; confirm the ADK API against the installed pin; also write a provisional holdout file as a safety net, marked baseline. Status and evidence: empty.
- **G3 Error analysis, time-boxed** (C5). 0.5 h, hard stop. Primary skill `adk-agent-evaluation` (quality iteration). Acceptance: each wrong dev case is classed (misread rule, arithmetic, missed document, condition convention, wording); at most two changes, each re-measured alone against M1; a change that does not move the score is reverted. Status and evidence: empty.
- **G4 Holdout regeneration** (C5). 0.25 h. Acceptance: the five predictions are produced by the final method with the config hash and model ID in the file; the dev score is re-run with the same config and matches. Status and evidence: empty.
- **G5 Report** (all). 0.5 h. Acceptance: two pages max: method and why, dev table with repeats, error classes, the coverage gap, what was and was not measured (PDF reading, wording, real officers), the holdout disclosure, draft-only status, spend. No claim beyond what M1 and the re-run show. Status and evidence: empty.

Capacity: goals sum to 2.25 to 2.75 h. At 4 h with a 25% reserve (3.0 h usable) the high end fits. At 3 h (2.25 h usable) only the low end fits. Cut order if short: probe cases first, then G3 to one change, then G1 polish. G2 baseline, G4 and G5 are never cut; if time runs out early, the ordering above still leaves a measured baseline, safety-net predictions and a report.

Resources created: none that charge while idle, so no teardown goal.

Phase 2 (only if continued): PDF ingestion triage and retrieval (`adk-memory-architecture`, 3 to 6 h, accepts when a Table 2 page is read correctly); an expert-labelled gold set of 20+ cases (`adk-agent-evaluation`, 4 to 8 h); officer review workflow. Later: hosting, identity, CI gate, governance pack, each on the triggers in section 1.

Graduation conditions: real PDFs ingested and checked, a labelled set larger than 5 with an agreement report, an officer reviewing every draft, a governance review before real applicant data.

## 6. Open decisions and next prompt

Open: the five questions in section 1, and the model ID, which blocks G2 only. G1 is independent of them.

```text
/adk-engineer Carry out G1 from docs/architecture/planning-decision-assistant.md.
```
