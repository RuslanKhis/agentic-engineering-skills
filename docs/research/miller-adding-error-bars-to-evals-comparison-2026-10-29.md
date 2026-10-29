# "Adding Error Bars to Evals" compared with this toolkit — 29 October 2026

Entry 2 of the [engineering-articles reading plan](engineering-articles-reading-plan-2026-10-28.md).

## The article

- **Paper.** Evan Miller, "Adding Error Bars to Evals: A Statistical Approach
  to Language Model Evaluations", arXiv 2411.00640 v1, submitted 1 November
  2024, 14 pages, stat.AP and cs.CL, https://arxiv.org/abs/2411.00640. Only
  v1 exists. Read in full from the arXiv HTML rendering
  (https://arxiv.org/html/2411.00640v1): abstract, sections 1 to 6,
  references and appendices A to C.
- **Blog post.** "A statistical approach to model evaluations", Anthropic
  research, 19 November 2024,
  https://www.anthropic.com/research/statistical-approach-to-model-evals.
  Read in full, to the page footer. It summarises the paper's five
  recommendations for a general audience and links to the paper.
- **Age.** Older than the programme's preferred window (2025 to 2026). It is
  kept because it is still the reference that later evaluation write-ups cite
  for error bars on evaluation scores. Plan entry 46 (Segato, February 2026)
  builds on it.

The paper treats an evaluation as an experiment. The questions are a sample
from a larger population of possible questions, so a score has a standard
error. It makes five recommendations:

1. Report the standard error of the mean.
2. Cluster the standard error when questions come in related groups.
3. Reduce variance within a question by resampling answers (or by using
   next-token probabilities).
4. Compare two models on per-question paired differences.
5. Use power analysis to decide whether an evaluation can detect the
   difference of interest.

## Authorship evidence

- **Paper.** The arXiv HTML prints the sole author as Evan Miller, with the
  affiliation Anthropic.
- **Blog post.** It has no byline. It is filed under Anthropic's Alignment
  team, and its "Read the paper" link goes to arXiv 2411.00640.
- **Criterion met.** The author was at Anthropic when he wrote it (paper
  affiliation).

## Method

1. Read the paper and the blog post in full with a web-fetch tool (both
   pages reached their end). The fetch tool returns a model's rendering of
   the page rather than raw text, so the formulas were re-derived and checked
   rather than copied (step 4).
2. Re-read every file the plan names:
   - `evaluation-design.md`;
   - `quality-iteration.md`;
   - `result-auditing.md`;
   - `ci-eval-gates.md` and `model-migration.md`;
   - `storyline.md` and `value-report.md`;
   - `opportunity-portfolio.md`.
   Also re-read the texts entry 1 changed:
   - "Shape the rubric before writing it";
   - "Re-check where the costly error lands";
   - the Optimisers section of `prompt-as-code.md`;
   - `content-safeguards.md`.
3. Searched `skills/` for "standard error", "confidence interval", "power",
   "sample size", "minimum detectable", "paired", "bootstrap", "noise",
   "margin", "square root", "pass^k" and "repeat". Results:
   - none of the first five appeared in any skill;
   - the only margin rule was the presenter's one-over-root-n;
   - `adk-system-designer`'s `engagement-scoping.md` asks for "a window and a
     sample size" for live acceptance but gives no method.
4. Checked every formula with the Python standard library before writing it
   into a skill:
   - the paper's n ≈ 969 for ω² = 1/9, δ = 0.03;
   - its minimum detectable effect, 13.3% at K = 1 and 7.6% at K = 10 (the
     paper prints 7.5%);
   - the resampling factor (1 + 2/K)/3;
   - the presenter's margins: one proportion at 300 is about 5.7 points;
     two separate samples of 300 are about 8.0 points;
   - the discovery sizing: 60% to 65% needs about 1,468 per period, and 60%
     to 70% about 353.
   Student's t quantiles in the helper match printed tables to three
   decimals (12.706, 2.262, 2.093, 0.861).

## Imported

**adk-agent-evaluation (owns the computation).**

- **`quality-iteration.md`, new section "Tell a change from noise".** Eight
  steps, restated for an ADK project:
  - same cases for both versions, K runs each;
  - each case's runs averaged first, never pooled;
  - the difference taken per case;
  - the standard error clustered on the scenario, with the small-sample
    factor G/(G − 1);
  - a t interval on G − 1 degrees of freedom and the verdict ("within
    noise" when the interval includes zero);
  - the minimum detectable difference (about 2.8 × SE) stated before
    keeping a win;
  - the holdout and CI set sized with the power formula, from the variance
    measured on the development runs, using the paper's worked figures
    (970, 88 and 22 cases for 3, 10 and 20 points);
  - runs reduce run-to-run noise only, and the temperature stays at the
    default.

  It closes with how error analysis on five to twenty cases and the interval
  fit together.
- **`quality-iteration.md`, the loop.**
  - Step 1 says the development set finds error categories but cannot show
    that a small score change is real.
  - Step 1 sizes the holdout for the smallest difference the decision turns
    on.
  - Step 4 re-runs the cases a change moved before counting them fixed, and
    records a move below the minimum detectable difference as "within noise".
  - "Keep the measurement honest" requires the interval with every compared
    score.
- **`evaluation-design.md`, "Build gates and close the feedback loop".** The
  line "use uncertainty methods respecting repeated trials within cases"
  became a named method: a paired difference with a clustered error and the
  minimum detectable difference. The holdout is sized from the difference
  that matters.
- **`result-auditing.md`.** `pass@k`, `pass^k` and the scenario score
  describe one version. Comparing two versions on them goes through the
  per-case paired method.
- **`SKILL.md`.** One sentence in the quality-iteration routing bullet,
  pointing to the section and the helper. The description is unchanged.
- **New helper `scripts/paired_difference.py`, with 17 tests in
  `tests/test_paired_difference.py`.**
  - Input: two trial records (CSV or JSON Lines) in the result-auditing
    shape.
  - Output: the paired difference, the clustered SE, the t interval, the
    verdict, the minimum detectable difference, the correlation, and the
    split between run-to-run noise and between-case variance.
  - With `--target-difference`: the cases and scenarios needed. With
    `--plan-cases`: the difference a given number of cases could detect.
    `--plan-runs` repeats both at another run count, when the noise split
    can be estimated.
  - `--require improved` and `--require not-worse --margin M` turn it into a
    gate.
  - Exit codes 0, 1, 2 and 3 follow the [helper conventions](../helper-conventions.md).
  - Why a helper: averaging runs before differencing, clustering, the G/(G − 1)
    factor and t quantiles are mechanical steps a coding agent gets wrong by
    hand (the paper's own warning about pooled runs is the most common
    error). The helper is standard library only.
  - Why not extend an existing helper: `label_agreement.py` measures label
    agreement and `check_eval_results.py` gates ADK's per-metric CSV, so
    neither has a comparison to extend.
  - **Two choices are this repository's, not the paper's.**
    - The paper prints the clustered SE with a 1/n prefactor and no
      small-sample factor, and uses normal quantiles. The helper adds the
      usual cluster-robust factor G/(G − 1) and uses Student's t on G − 1
      degrees of freedom. With one case per cluster this reduces to the
      ordinary standard error with n − 1. Agent projects usually have 20 to
      100 cases, so normal quantiles would understate the interval (2.09
      against 1.96 at 20 cases).
    - The sample-size projection starts from the paper's z formula and is
      refined with t.

**adk-release-engineering (uses it).**

- **`ci-eval-gates.md`, tier 3.** A drop now opens a blocker only when its
  paired interval lies wholly below zero.
- **`ci-eval-gates.md`, new subsection "Read a drop against the noise".** It
  sets four rules:
  - pair by case;
  - block on a real drop;
  - the suite's minimum detectable difference must be no larger than the
    agreed margin, or the gate's limit is written down;
  - choose `num_runs` against more cases from the variance split.
  The per-case thresholds are left alone.
- **`ci-eval-gates.md`, holdout and Completion.** The holdout is recorded as
  a paired difference and sized by the power formula. Completion asks for
  the minimum detectable difference beside the margin.
- **`model-migration.md`.** The side-by-side reports the aggregate delta as
  a paired difference. A retirement-forced or cost-driven migration is a
  "not worse by more than the margin" question.

**adk-presenter (uses it).**

- **`storyline.md`.** The one-over-root-n rule is replaced:
  - one proportion's 95% margin is at most about 1/√n (corrected from "about
    five points on 300" to about six);
  - a lift between two separate samples is wider,
    1.96 × √(p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂), about eight points for 300 and
    300;
  - grouped outcomes widen it again;
  - when both figures come from the same cases, cite the evaluation skill's
    paired interval.
- **`value-report.md`.** Outcome against baseline points to that formula,
  because this month against a baseline period is two separate samples.

**adk-discovery (uses it).**

- **`opportunity-portfolio.md`, "Window and sample".** "How many" is sized
  from the smallest lift the sponsor would act on, with the two-rate power
  formula:
  - a 5-point lift from 60% needs about 1,470 per period, and a 10-point
    lift about 350;
  - what to do when the volume cannot reach it;
  - a shadow run of the same cases needs fewer, sized by
    adk-agent-evaluation.

**adk-agent-instructions.**

- **`prompt-as-code.md`, Optimisers.** "Keep the candidate only when the
  outcome measure improves on the holdout" now reads "by more than its
  noise", pointing to the paired interval. The rest of entry 1's text is
  unchanged.

**Scenario cases.** Four new cases in `evals/scenarios.json`:

| Case | Fixture |
| --- | --- |
| `evaluation-paired-difference-and-holdout-size` | `evals/fixtures/` overlay with synthetic trial records (20 cases, 8 scenarios, 3 runs, one `infra_error` row), a dashboard, a brief extract and a 12-case holdout, plus judge-only material with the helper's real output |
| `release-nightly-drop-against-noise` | runnable from the context |
| `presenter-lift-within-margin` | runnable from the context |
| `discovery-pilot-sample-size` | runnable from the context |

All four are listed in `evals/scenario-fixtures.json`.

## Linked only

- **The blog post.** It is the accessible summary. The skills cite the paper,
  because the formulas are there.

## Not imported, with reasons

- **Next-token probabilities to remove within-question noise.** This applies
  to single-token answers. An agent's outcome is a trajectory and an end
  state, not one token, and reading log-probabilities changes what is
  measured. No skill decision changes.
- **"Don't touch the thermostat" (lowering temperature to cut variance).**
  Already the repository's rule: adk-model-and-output-contracts keeps Gemini 3
  at 1.0, and `ci-eval-gates.md` prefers rubrics, repeats and trajectory
  criteria to `temperature=0`. The new section adds the paper as a second
  reason in one clause.
- **Standard error of a single score and the Bernoulli form √(p(1 − p)/n).**
  The skills report comparisons, not leaderboard scores. The single-proportion
  margin appears only where the presenter needs it.
- **Unpaired comparison of two models.** The skills always compare on the
  same cases. The unpaired form is used only for the presenter's and
  discovery's two-period comparisons.
- **"New evals should contain at least 1,000 questions."** This is a fixed
  count for public benchmarks. The skills size from the difference that
  matters; the 3-point worked example (about 970) is quoted as an
  illustration.
- **Bootstrap.** The paper mentions it only as common practice that is
  unnecessary when the central limit theorem applies. It gives no procedure.
- **Intervals on judge TPR and TNR in `expert-review.md`.** The judge-rate
  rule refuses a rate below a per-class minimum (`label_agreement.py`
  `--min-per-class`). An interval on those rates (a Wilson interval, for
  example) is not in the paper. Left for a later change, if trials show it
  is needed.
- **adk-system-designer's live acceptance sample size
  (`engagement-scoping.md`).** It asks for "a window and a sample size" for
  acceptance on live traffic, and its example criterion is a one-sample
  threshold on 40 gold cases, not a comparison. The plan did not name it.
  Discovery now gives the sizing method the designer's acceptance can reuse.
  Recorded here for the designer's owner.
- **Facts about Anthropic models and the paper's benchmark tables** (MATH,
  HumanEval, MGSM, DROP and the Llama 3 report). Not imported: they are about
  other vendors' models, and the skills target ADK and Gemini.

## Conflicts

- **`ci-eval-gates.md`'s "run the baseline five times, take the minimum per
  case".** No conflict. That rule sets a per-case ROUGE threshold, which
  decides whether each case passes. The paper is about comparing aggregate
  scores. Both are kept, and the new subsection says the per-case rules are
  unchanged.
- **The paper's clustered SE prefactor and normal quantiles.** The helper and
  the skill text use the small-sample factor and t, as explained under
  Imported. With one case per cluster and many cases, both agree with the
  paper.
- **The presenter's "about five points on 300".** Corrected. 1/√300 is 5.8
  points, and the 95% margin of one proportion near 50% is 5.7. The text now
  says "about six".

## Left for later entries

- **Entry 46 (Segato, infrastructure noise).** Executor resource limits and
  the time window as recorded variables of each run, and "a small difference
  is noise unless configurations match". The new section covers only
  statistical noise between cases and runs, and the same cases, fixtures,
  criteria and judge. Entry 46 can add the run configuration to step 1 and to
  `live-evaluations.md`.
- **Entry 3 (receipt inspection).** Pricing each error type as the gate. The
  paired interval says whether a rate moved; entry 3 says what the move is
  worth.
- **Entry 23 (GDPval).** Review-adjusted savings in the value report. The
  presenter change touches only the margin sentence.

## Limits

- **Reading.** The paper and blog were read through a fetch tool that renders
  the page through a model. The formulas used here were re-derived and
  checked numerically, not copied. The paper's benchmark figures (for
  example "clustered errors more than three times the naive ones") are
  marked "reported by the source, not verified here".
- **Small samples.** The helper's split between run noise and between-case
  variance is unstable on small samples. When the run-noise estimate exceeds
  the observed variance, the helper reports the split as not estimable. It
  then plans only at the runs per case already used.
- **Synthetic data only.** No model was called. The trial project's trial
  records are synthetic, generated with a seeded script.
- **Trial.** See the
  [testing record](../testing/miller-adding-error-bars-to-evals-alignment-2026-10-29.md).
