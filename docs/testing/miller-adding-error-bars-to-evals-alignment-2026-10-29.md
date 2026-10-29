# "Adding Error Bars to Evals" alignment — 29 October 2026

Source note: [comparison](../research/miller-adding-error-bars-to-evals-comparison-2026-10-29.md).

## Changed journeys

- **adk-agent-evaluation.** Saying whether a prompt, exemplar, model or
  workflow change helped, and sizing a holdout or CI set
  (`quality-iteration.md`, "Tell a change from noise"). The new helper is
  `scripts/paired_difference.py`, with 17 tests.
- **adk-release-engineering.** Reading a nightly drop against the noise, and
  the "not worse" question in a model migration (`ci-eval-gates.md`,
  `model-migration.md`).
- **adk-presenter.** The margin of a lift between two periods
  (`storyline.md`, `value-report.md`).
- **adk-discovery.** Sizing a pilot from the smallest lift the sponsor would
  act on (`opportunity-portfolio.md`).
- **adk-agent-instructions.** One clause in the Optimisers section:
  "improves by more than its noise".

**New scenario cases.**

| Case | Status in `evals/scenario-fixtures.json` |
| --- | --- |
| `evaluation-paired-difference-and-holdout-size` | repo-fixture: overlay under `evals/fixtures/`, judge-only material under `evals/graders/` |
| `release-nightly-drop-against-noise` | runnable |
| `presenter-lift-within-margin` | runnable |
| `discovery-pilot-sample-size` | runnable |

## Fresh-agent trial

**Set-up.** One trial, run on 29 October 2026.

- **Agent.** A general-purpose subagent with a fresh context, on the same
  model as the coordinator (Claude Opus 5.5). It was told to work only
  inside the workspace and to read the installed skills' `SKILL.md` first.
  It did not see the scenario assertions or the judge material.
- **Workspace.** In the session scratchpad. It was the
  `evaluation-paired-difference-and-holdout-size` overlay, plus copies of
  adk-agent-evaluation, adk-agent-instructions, adk-release-engineering and
  adk-presenter under `.claude/skills/` (without `tests/`). The copies were
  taken before the step-7 clustering clause was added.
- **Data.** Synthetic trial records generated with a seeded script:
  - 20 development cases in 8 scenarios;
  - 3 runs per case for each prompt version;
  - one `infra_error` run.
- **Prompt.** The scenario's prompt and context. It was asked to write
  `docs/v4-comparison.md` and report frictions.
- **Limits.** No model, no network, no ADK. It used 12 tool calls in about
  2.5 minutes.

**What it did.**

- **Skills read.**
  - `SKILL.md`;
  - all of `quality-iteration.md`;
  - `paired_difference.py --help`;
  - `result-auditing.md`, lines 1 to 36;
  - the holdout and evidence-label lines of `evaluation-design.md` and
    `operating-rules.md`.
- **Helper.** It ran `paired_difference.py` (exit 0) and checked the
  figures by hand in Python. Its hand-computed clustered SE was 0.0678,
  matching the helper; the unclustered SE was 0.0824. It also ran
  `--require improved`, which exited 1 as expected.
- **Answer.**
  - +6.7 points, 95% interval −9.4 to +22.7: within noise.
  - Minimum detectable difference about 22 points.
  - Do not tell the sponsor "6 to 7 points".
  - About 295 cases (118 claim types) at three runs to detect 5 points,
    against about 430 unclustered.
  - The 600-run budget detects only about 9 to 10 points.
  - The 12-case holdout is unlabelled and far too small.
  - Read the per-case losses (dev-003, 006, 008, 009, 013) before saying
    anything about v4.
- **Evidence labels.** `offline`; the claim "v4 improved" `fail`; the
  holdout `not run`.
- **Ease.** 5 of 5 for finding the method, 3 of 5 for applying it.

**Against the scenario assertions** (graded by the coordinator from the
report and the helper output):

| Assertion | Result |
| --- | --- |
| Runs averaged per case, difference per case, not pooled run rates; infra_error left out and reported | Pass |
| SE clustered on scenario; interval includes zero; "within noise" | Pass (it reported both the clustered and unclustered figures) |
| Minimum detectable difference about 22 points; no "it helped" claim | Pass |
| Holdout sized from the 5-point lift with the dev variance; 12-case holdout insufficient; budget trade-off | Pass (295 to 430 cases; budget detects about 9 to 10 points) |
| Helper used; no model run | Pass |

The release, presenter and discovery journeys were not trialled. Their
scenario cases are runnable from the context, but no session ran them.

## Frictions and fixes (same day)

1. **The noise split was confusing.** The helper printed "100% run noise"
   when the run-noise estimate exceeded the observed variance. It then
   projected runs from that, which contradicted the reference's "add cases,
   not runs".
   - **Helper fix.** It now reports the split as not estimable in that
     case, and it does not project other run counts.
   - **Reference fix.** Step 8 says to plan on cases at the current runs.
2. **Clustering narrowed the error.** The skill described clustering only
   as widening the error. Step 4 now says the clustered error can come out
   smaller when variants move in opposite directions. With fewer than about
   ten scenarios, report both and plan from the larger. It also says to
   record the scenario of every holdout case.
3. **"Scenarios needed" was unexplained.** The helper now prints "planning
   assumes N cases per scenario, as in this sample". Step 7 gives the
   scenario-level formula.
4. **A budget in runs had no recipe.**
   - **Helper fix.** New `--plan-cases N` reports the difference N cases
     could detect, at the current runs and at `--plan-runs`.
   - **Reference fix.** Step 7 converts a run budget into cases.
5. **Unclear plan lines.** The line did not say it assumed the current runs
   per case, and "this sample cannot" was cut short. Each plan line now
   starts "at K runs per case", and the last line reads "this sample
   cannot detect 5.0 points".
6. **Labelling cost is not in the sizing.** Not changed. Labelling cost
   belongs to expert-review's session planning, and the sizing gives the
   number of cases to label.
7. **Whether `pass^k` or the scenario score is required in a comparison.**
   Not changed. `result-auditing.md` now says those figures describe one
   version, and a comparison goes through the per-case method.

**A defect found before the trial.** Rehearsing on the fixture data, the
first version of the helper's clustered sample-size projection multiplied
the per-case variance by the cases per scenario instead of dividing by it.
That overstated cases needed by a factor of the cluster size squared (1,810
instead of 295). It was fixed, and a test was added
(`test_clustered_plan_counts_scenarios_as_units`): duplicated variants in
one scenario must leave the SE unchanged and double the cases needed. The
trial ran on the fixed helper.

The fixes after the trial were not re-trialled with a fresh session. The
judge-only material holds the helper's current output.

## Scenario run (after review)

After the review, the user approved a paid scenario run. All four new
scenarios ran through `scripts/run_scenarios.py run` on 2026-10-29. Agent
and judge were `claude-sonnet-5-5` through `claude-cli`, with three judge
repeats (majority verdict), `--max-budget-usd 3` per agent run and a
project skill install. The evaluation scenario ran with
`--agent-tools Read,Write,Edit,Glob,Grep,Skill,Bash` and the scrubbed shell
environment of the [shell run](shell-run-2026-10-28.md); the other three
ran without a shell. Skills were at `57bd50f` plus this change, before the
two follow-ups below. The cost was $0.88 in all: $0.56 for the agents and
$0.32 for the judges.

| Scenario | Passed | Primary skill loaded | Notes |
| --- | --- | --- | --- |
| evaluation-paired-difference-and-holdout-size | 5/5 | yes | It ran `paired_difference.py` itself and reported +6.7 points (−9.4 to +22.7), within noise, an MDE of 22 points and about 295 cases for 5 points. |
| presenter-lift-within-margin | 3/3 | yes | Two-sample margin of about 6.7 points; the slide title makes no claim of a measured lift. |
| release-nightly-drop-against-noise | 2/4 | yes | The paired gate and the MDE passed. Missed (3 of 3 votes each): choosing `num_runs` from the run-to-run versus between-case split, and stating that the per-case thresholds and every-run check are unchanged. |
| discovery-pilot-sample-size | 2/3 | no | About 1,470 per arm and the short window were right, but it answered in one turn from general knowledge, so it missed the shadow-run route and writing the sample into the outcome measure. |

**Follow-ups.**
- The release reference already held both missed points, in "Read a drop
  against the noise". Its Completion line now names them, so the agent's
  own completion check catches them. Not re-run.
- The discovery miss is skill selection: the skill was never loaded. The
  sizing text was not tested by this run, and no content change follows
  from it.
- adk-system-designer's engagement-scoping reference now sizes a
  live-traffic acceptance sample from the smallest difference the client
  would act on, through adk-discovery (before and during) or
  adk-agent-evaluation (paired). This is a one-paragraph pointer with no
  scenario of its own.

## Checks

- **`.venv/bin/python scripts/check_repo.py`: passed.**
  - 28 offline suites, 1,232 tests (the previous run had 1,215; the 17 new
    tests are `test_paired_difference.py`).
  - 26 skill packages, with 0 errors and the 3 existing warnings.
- **`git diff --check`:** clean.
- **`.venv/bin/python scripts/check_source_freshness.py --validate-only`:**
  "Register valid: 97 sources; nothing was fetched."
- **Formulas checked numerically** with the standard library before they
  went into the skills:
  - the paper's n ≈ 969 and its MDE example (13.3% and 7.6%);
  - the resampling factor;
  - the presenter's margins (5.7 and 8.0 points on 300);
  - the discovery sizing (about 1,468 and 353 per period);
  - Student's t quantiles against printed tables.

## Limits

- **One trial.** One trial on one synthetic fixture. It is not a paired
  comparison with the skills before this change.
- **Same model family.** The trial agent used the same model family as the
  author of the change.
- **No live runs.** No ADK Runner or `adk eval` run, and no model call.
- **Single scenario runs.** Each scenario ran once, so one run cannot
  separate a skill defect from run variance. The post-trial fixes and the
  release clarification were not re-run. The discovery journey's content
  went untested, because the skill was not loaded.
