# "Evaluation Precedes Evolution" compared with this toolkit — 28 October 2026

Entry 1 of the [engineering-articles reading plan](engineering-articles-reading-plan-2026-10-28.md),
the seed article.

## The article

Pouya Ghiasnezhad Omran and Tanya Dixit, "Evaluation Precedes Evolution:
Rubrics for Agents That Rewrite Themselves", LinkedIn article, 15 June 2026.
The exact URL was not recorded; the register row points at LinkedIn's article
root. The user pasted the article on 28 October 2026, and the pasted text is
kept in the session scratchpad, not in this repository. The skills quote only
short extracts.

The article's claim is that every self-improving loop (GEPA, ReasoningBank,
prompt optimisers, memory accumulation) climbs a rubric. A vague rubric
therefore produces an agent that games it. It gives three axes for shaping a
rubric:

- verifiability;
- horizon;
- stakes.

It gives four rules, each tied to the authors' open-source invoice-processing
agent:

1. Deterministic checks before semantic ones.
2. Name failure modes and score every stage.
3. Asymmetric verification, enforced in code.
4. A business metric instead of a proxy. It names two ways a proxy is gamed:
   escalation as a relief valve, and reasoning-trace theatre.

## Authorship evidence

- **Byline.** "By Pouya Ghiasnezhad Omran & Tanya D.", with Tanya Dixit's
  headline "FDE @ Google".
- **Author note.** Both authors are Forward Deployed Engineers on Google
  Cloud's AI FDE team in Sydney.
- **Confirmation.** The user confirmed on 28 October 2026 that both authors
  work at Google.
- **Related talk.** A web search on 28 October 2026 found a talk with a close
  title by Tanya Dixit at AI Engineer Melbourne 2026. It was not read and is
  not cited.

## Method

1. Read the pasted article in full.
2. Re-read the plan's files:
   - adk-agent-evaluation: `evaluation-design.md`, `expert-review.md`,
     `quality-iteration.md`, `result-auditing.md`;
   - adk-agent-instructions: the Optimisers section of `prompt-as-code.md`.
3. Searched `skills/` for the same ideas: proxy, optimiser, asymmetric,
   re-check, verifiability, horizon, per-stage, keyword, manual intervention,
   rules book, master data, review queue and escalation rate.
4. Read the cited code read-only, from a sparse clone in the session
   scratchpad. Nothing from it was run.
   - **Where the sample went.** google/adk-samples now redirects to
     google/adk-recipes; both report the same HEAD. `python/agents/invoice-processing`
     was deleted from main on 2026-09-09, in commit 3fd76ce ("Deleted the 9
     old/obsolete samples").
   - **Commit read.** a9dc177, the parent of 3fd76ce. Its code is identical to
     9bf35ee (2026-05-11), the last code change before the article was
     published; only an image changed in between.
   - **Files read.** `README.md`, `invoice_processing/agent.py`,
     `shared_libraries/investigation/investigate_agent_reconst.py`,
     `shared_libraries/acting/general_invoice_agent.py`, the header of
     `shared_libraries/alf_engine.py`, and `core/safe_rule_orchestrator.py`;
     also the presence of `invoice_master_data.yaml` and
     `data/reconstructed_rules_book.md`.
5. Checked the ADK optimiser's scoring in the installed google-adk 2.8.0 and
   2.12.0 packages: `optimization/local_eval_sampler.py` and
   `gepa_root_agent_prompt_optimizer.py`.

### What the code shows

| Article claim | At a9dc177 |
| --- | --- |
| ABN checksum in pure Python, before any judge | Verified: `validate_abn_checksum` (weights, `% 89`) in the acting pipeline's phase 3 |
| Numbered stage records `01_classification.json` to `09_audit_log.json` | Verified: the acting pipeline writes them, and the investigation script loads them |
| `PerGroupValidator` gives stage-local verdicts, "never aggregated into one end-scalar" | Partly. The script keeps a `PhaseValidation` verdict per phase, and the per-phase results (`phase1_result`, ...) appear in `CaseProcessingSummary`. It also rolls the phases into a `compliance_score`, and the stop gate in `agent.py` reads that score: `MAJOR_VIOLATION` below 60 stops the pipeline. `PerGroupValidator` validates rule groups (layer 3), not stages |
| `_run_with_triple_check` re-checks violations, trusts compliant after one call, in Python | Verified. A first violation (confidence of at least 0.95) is re-run twice. It is confirmed only when each re-run overlaps the first by 75 per cent of rule IDs; otherwise it is discarded |
| "Only violations confirmed all three times halt the pipeline" | Not found. The class docstring calls layer-3 violations "INFORMATIONAL", and they "do NOT override Layer 1 compliance scores". The stop gate is the score above. Reported by the source, not verified here |
| Rubric in a YAML master data file and a Markdown rules book, versioned in git | Verified: both files are in the repository |
| Business metric: share of invoices needing no manual intervention | Not computed by the sample's `eval/` (field match rates, decision alignment, an optional holistic LLM verdict). Reported by the source, not verified here; so are the 70-to-40 and 85-per-cent figures |
| Correction layer learned from experts as deterministic rules | Verified as described by the sample. ALF rule conditions are matched deterministically, and actions run in three tiers (LLM pipeline continuation, LLM field patch, deterministic `set_field`). Every rule needs expert approval and an impact check against all cases. `safe_rule_orchestrator.py` enforces the safety loop "in code (not prompt instructions)" |

Two details of the triple-check matter for anyone copying it:

- **Temperature 0.** `PerGroupValidator` sets `temperature=0`, so its three
  calls are not independent samples.
- **Failure reads as compliant.** `_call_group_llm` returns
  `"violations": []` when the call raises, so a failed check reads as
  compliant.

Separately, when the whole investigation stage raises, `agent.py` marks it
`INCONCLUSIVE` and continues to the correction stage. The toolkit keeps its
own rules on all three points; see Conflicts.

## Imported

**adk-agent-evaluation.**

- **`evaluation-design.md`, new section "Shape the rubric before writing
  it".**
  - The three axes, as items to record in the plan before a rubric is
    written.
  - Verifiability: code checks run first, a case that fails one fails
    without a judge call, and the judge covers only what is left.
  - Horizon: one sub-rubric per stage, scoped to the stage's contract;
    per-stage verdicts kept beside the end-to-end verdict; a rollup never
    replaces them and never gates.
  - Stakes: decides the gate's error, where re-checks are spent, and the
    headline figure.
  - The work is judged on the outcome measure, not a rubric score.
  - The two gaming patterns:
    - an escalated case counts as manual work, and over-escalation is
      reported beside any score;
    - whether a check ran is read from the trace, never from the agent's
      wording.
  - The calibration set gains "a stated check that the fixed trace shows
    never ran".
- **`expert-review.md`.**
  - "Re-check where the costly error lands": the direction follows the
    downstream gates, and flips when nothing deterministic sits between the
    judge and the effect.
  - The sample's mechanism, cited with its two departures (temperature 0, a
    failure counted as a pass).
  - What to measure: the whole rule's TPR and TNR, the overturn rate, the
    extra calls, and an errored re-run counted as incomplete.
  - A line added to Completion.
- **`SKILL.md`.** One routing bullet to the new section.

**adk-workflow-design.**

- **`content-safeguards.md`, new section "Re-check the verdict whose error
  costs most".**
  - The runtime rule, with a small `checked_verdict` function.
  - The loop lives in code, not in an instruction.
  - An incomplete result takes the failed-check path.
  - The check keeps the model's default sampling.
  - Every run and overturned verdict is recorded.
  - Measurement is routed to evaluation.
  - A line added to Completion.
- **`SKILL.md`.** One sentence pointing to the new section.

**adk-agent-instructions.**

- **`prompt-as-code.md`, Optimisers.** "Evaluation precedes evolution",
  restated in ADK terms:
  - `LocalEvalSampler` scores an example 1.0 when its case's
    `final_eval_status` is `PASSED`, else 0.0, so `eval_config` is the
    fitness function;
  - GEPA reflects on the per-invocation metric scores;
  - an unset `validation_eval_set` falls back to the training cases;
  - the preconditions before a run;
  - keep a candidate only when the outcome measure improves on the holdout.
- **`SKILL.md`.** Its table row names the Optimisers section before any
  `adk optimize` run.

**Scenario cases.** Two new cases in `evals/scenarios.json`:
`evaluation-rubric-before-optimiser` and `workflow-recheck-costly-verdict`.

**Source register.**

- **Article row.** The first article row (`"kind": "article"`, `"url"`,
  `pinned` null).
- **Freshness check.** `scripts/check_source_freshness.py` validates article
  rows, never fetches them, and reports them as checked by date only. A rate
  limit does not mark them unchecked. Three tests were added.
- **No new google/adk-samples row.** That repository is google/adk-recipes,
  which already has a row (pinned be63596, used by the evaluation, workflow
  and instructions skills). A second row under the old name would be
  reported as renamed.

**After the trial (same day).**

- **Custom metrics.** `evaluation-design.md` gained the ADK `EvalConfig`
  custom-metric form for code checks, checked against the google-adk
  2.12.0 source:
  - the function signature;
  - the evaluator clears the threshold, so the function sets its own
    status;
  - `NOT_EVALUATED` is skipped, and a case whose metrics are all
    `NOT_EVALUATED` is not `PASSED`.

  It also points to the optimiser's limits.
- **Workflow root.** `prompt-as-code.md` says that GEPA needs a static
  string `instruction` on the root agent, so a workflow root has nothing to
  rewrite.
- **Code first.** `content-safeguards.md` says to move code-decidable rules
  out of the model check first.
- **Small samples.** `expert-review.md` says to give raw counts, labelled
  indicative, when a class is below the minimum.

## Linked only

None. The article is cited at the decisions it serves, not as further
reading.

## Not imported, with reasons

- **Deterministic checks before the judge.** Already covered:
  `evaluation-design.md` "Use programmatic assertions for exact facts and
  business invariants. Add a judge when …". The new section points to it and
  adds only the order (a failed check fails the case without a judge call).
- **One judge per failure mode, and binary criteria.** Already covered:
  `expert-review.md`, "Calibrate one judge per failure mode" and "Label per
  criterion".
- **The TPR or TNR choice for a review queue.** Already covered:
  `expert-review.md` ("favour TPR when a missed failure is costly and TNR
  when false alarms would flood a human review queue"). The re-check builds
  on it.
- **Missed- and over-escalation rates.** Already covered:
  `evaluation-design.md`, "Curate cases with a reason to exist", step 1. The
  guardrails skill already forbids prompt changes "tuned to move the
  dashboard number" (`human-review.md`). Only the rule that an escalated case
  counts as manual work in the headline was added.
- **Rubric versioned in git as YAML master data and a Markdown rules book.**
  Already covered: criteria files versioned and dated (`expert-review.md`,
  "Write the criteria"); the rubric version recorded with every judge run
  (`evaluation-design.md`); judge pins in the release skill. File formats are
  the project's choice.
- **The correction layer learned from experts as deterministic rules (ALF).**
  The article defers it ("Evolution is the other half … different
  problem"). It changes no evaluation decision here. Procedural knowledge
  written by code and promoted by review is entry 37 (ReasoningBank), for
  adk-memory-architecture; record this sample there as a worked example when
  that entry runs.
- **Outcome measure, baseline and counter-metric in discovery, and the value
  report in presenter.** Already covered: `opportunity-portfolio.md`, "Define
  the measure before the build"; `value-report.md`. Nothing changes there.
- **GEPA, ReasoningBank and OpenAI's optimiser as named products.** Mentioned
  by the article only as examples of loops. The ADK form (`adk optimize`) is
  what the skills describe.
- **"Nine teams out of ten" and similar figures.** Opinion, with no data.

## Conflicts

- **Temperature 0 for repeated checks.** The sample's validator runs at
  temperature 0. The repository keeps Gemini 3 at its default temperature
  of 1.0 (adk-model-and-output-contracts, `reasoning-and-sampling.md`,
  "Keep temperature at 1.0 on Gemini 3"), and re-runs only help when they
  can disagree. Kept the repository's rule and said why in both new sections.
- **A failed check reads as compliant.** In the sample, an LLM call error in
  the validator returns no violations, and a failed investigation stage
  continues to correction. The repository fails closed (a judge exception is
  incomplete evaluation; an approval rule fails closed on unreadable input).
  Kept the repository's rule: an errored re-run is `incomplete` and takes the
  failed-check path.
- **Scalar gate.** The article says stage verdicts are never collapsed into
  one scalar, but the sample's stop gate reads a compliance percentage. The
  toolkit follows the article's rule (a gate reads the verdicts, not an
  average) and records the sample's behaviour beside it.

## Left for later entries

- **Entry 3 (receipt inspection).** Pricing each error type, and which input
  a stage grader is fed. The new horizon item says only that each stage is
  scored and kept, so that entry can add both.
- **Entry 4 (agent quality flywheel).** The proposer never grades its own
  fix; a categorical rubric with a not-applicable class. The Optimisers
  paragraph names the metric and leaves grader independence to it.
- **Entry 8 (harness design).** An in-loop critic calibrated like a judge.
  The re-check went into `content-safeguards.md`, leaving
  `orchestration.md`'s loop section untouched.
- **Entry 34 (CoT faithfulness).** A `reason` field is not evidence. The
  evaluation-side rule ("a claimed check is not a check") is in place; the
  output-contract rule stays with adk-model-and-output-contracts.

## Limits

- **The article.** Read from the user's paste. Its URL was not recorded.
- **The sample.** Read at a commit that is no longer on main; nothing was
  run.
- **Figures.** The article's numbers are the authors' and were not
  reproduced.
- **Model behaviour.** The re-check's benefit (overturn rate, TPR and TNR) is
  a measurement a project must make on its own labels. No model was called.
- **Trial.** One fresh-agent trial was run on a synthetic project, recorded
  in the [testing record](../testing/omran-dixit-evaluation-precedes-evolution-alignment-2026-10-28.md).
