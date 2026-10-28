# "Evaluation Precedes Evolution" alignment — 28 October 2026

Source note: [comparison](../research/omran-dixit-evaluation-precedes-evolution-comparison-2026-10-28.md).

## Changed journeys

- **adk-agent-evaluation.** A rubric for a multi-stage pipeline, or one that
  an optimiser will climb (`evaluation-design.md`, "Shape the rubric before
  writing it"); the re-checked judge (`expert-review.md`).
- **adk-agent-instructions.** The preconditions before an `adk optimize`
  run (`prompt-as-code.md`, Optimisers).
- **adk-workflow-design.** Re-checking a model check's costly verdict in
  code (`content-safeguards.md`).

New scenario cases: `evaluation-rubric-before-optimiser` and
`workflow-recheck-costly-verdict`. Neither has a fixture in
`evals/scenario-fixtures.json`, so the scenario runner reports them as
`fixture-missing`.

## Fresh-agent trial

**Set-up.** One trial, run on 28 October 2026.

- **Agent.** A general-purpose subagent with a fresh context, on the same
  model as the coordinator (Claude Opus 5.5). It loaded the installed skills,
  which link to this working tree. It was not shown the scenario
  assertions, and it was told not to open `evals/` or `docs/`.
- **Fixture.** A synthetic project in the session scratchpad, not kept in
  this repository:
  - an ADK 2.12-style `SequentialAgent` (extract, `policy_check`, decide);
  - a one-rubric "helpfulness 1 to 10" judge config;
  - a 12-case eval set whose invoice fixtures were missing;
  - `routing.py`, which treated an unreadable policy result as compliant;
  - a discovery brief naming the outcome measure;
  - 60 pilot labels in which the old LLM policy check over-flagged.
- **Prompt.** Set up an evaluation to trust before `adk optimize` rewrites
  the prompt, and cut the policy check's false alarms without letting real
  problems through.
- **Limits.** No ADK install, no model, no network. Bounded to about 40 tool
  calls; it used 27 (about 8 minutes).

**What it did.**

- **Skills read.**
  - adk-agent-evaluation: `SKILL.md`, all of `evaluation-design.md`, the
    calibration section of `expert-review.md`, and two sections of
    `quality-iteration.md`.
  - adk-workflow-design: `content-safeguards.md`, including the new
    section.
  - adk-agent-instructions: the Optimisers section of `prompt-as-code.md`.
- **Policy rules.** All four moved out of the LLM check into Python with
  pass, fail or unknown per rule. Unknown never counts as pass.
- **Routing.** It fails closed, and a code guard stops any payment that the
  checks did not pass.
- **Evaluation.**
  - The judge was replaced by two code metrics in `custom_metrics`.
  - 18 synthetic cases were written, with false-alarm controls, split
    dev 8, validation 5 and holdout 5.
  - A pure-Python grader gives stage verdicts and reports the outcome
    measure (an escalated case counts as manual work), wrong payments, and
    missed and over-escalation.
- **Optimiser checklist.** Pin `optimizer_model`, set `validation_eval_set`,
  never give the optimiser the holdout, and keep a candidate only if the
  outcome measure improves on the holdout.
- **Pilot labels.** It ran `label_agreement.py` on them. The result was NOT
  REPORTED, with 12 violations against a minimum of 30 per class.
- **Tests.** 44 offline tests passed, re-run by the coordinator, including a
  do-nothing control, a review-everything control and an always-pay decide
  stage. Nothing that calls ADK or a model ran. The agent's ease rating: 4
  of 5.

**Against the scenario assertions** (`evaluation-rubric-before-optimiser`,
graded by the coordinator from the files):

| Assertion | Result |
| --- | --- |
| Axes recorded; code-checkable properties as assertions before any judge | Partial. The rules moved to code and run first, but the three axes were not written down as such |
| One sub-rubric per stage; stage verdicts kept | Pass (stage verdicts in `eval/grading.py`) |
| Outcome measure as headline; escalation counted as manual; over-escalation reported | Pass |
| A claimed-check case; whether a check ran read from the trace | Not exercised: no model judge remained to be gamed |
| Separate validation set, holdout outside, `optimizer_model` pinned, keep only on holdout gain; model runs not run | Pass (checklist in README; nothing model-dependent ran) |

The workflow journey (`workflow-recheck-costly-verdict`) was touched but not
exercised. The agent chose to move every rule into code, which leaves no
model verdict to re-check. That choice matches the guidance, but the
mechanism itself was not tried.

## Frictions and fixes (same day)

1. **`adk optimize` cannot rewrite a `SequentialAgent` root.** The skills
   did not say what to do. Fixed in the `prompt-as-code.md` Optimisers
   section: GEPA seeds from the root agent's static string `instruction`
   and raises on an instruction provider (`_gepa_utils.require_static_instruction`,
   google-adk 2.12.0). A workflow root has nothing to rewrite, so expose the
   stage's `LlmAgent` as the root of its own module.
2. **No 2.12 form for a code-based metric.** The agent wrote it from memory.
   Fixed in `evaluation-design.md`, checked against the 2.12.0 source:
   - the `custom_metrics.<name>.code_config.name` path and the function
     signature;
   - the evaluator clears the threshold, so the function sets
     `overall_eval_status` itself;
   - a case whose metrics are all `NOT_EVALUATED` is not `PASSED`.

   The agent's adapter happened to default the missing threshold to 1.0.
3. **The optimiser's limits sat only in the instructions skill.** Fixed:
   the new evaluation section points to the Optimisers section of
   `prompt-as-code.md`.
4. **When every rule moves to code, no model verdict is left.** Neither
   reference said so plainly. Fixed: `content-safeguards.md` now says to
   move code-decidable rules out of the model check first, and that the
   re-check is for what stays a model judgement.
5. **No guidance on what to report below the per-class minimum.** Fixed:
   `expert-review.md` says to give the raw counts, labelled indicative.
6. **Labels without their inputs cannot measure new checks.** Not changed:
   the fixture's own gap. The skill already requires traces shown whole.
7. **`__pycache__` folders in skill directories.** Not changed: they are
   local build leftovers, out of this article's scope.

## Checks

- `.venv/bin/python scripts/check_repo.py`: passed. 28 offline suites,
  1,215 tests; 26 skill packages with 0 errors and the 3 existing
  word-budget warnings.
- `git diff --check`: clean.
- `tests/test_check_source_freshness.py`: 17 tests, including the three
  article-row tests.

## Limits

- **One trial.** One trial on one synthetic fixture; it is not a paired
  comparison with the skills before this change.
- **Same model family.** The trial agent used the same model family as the
  author of the change.
- **No live runs.** No ADK Runner, `adk eval` or `adk optimize` run, and no
  model call.
- **Not exercised.** The re-check mechanism and the claimed-check control.
