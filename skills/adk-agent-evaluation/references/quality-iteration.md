# Improve the decisions with a measured loop

Read this when the request is "the decisions are wrong", "improve the
answers", a prompt or output schema needs designing, or a stronger model is
being considered. The loop below measures decision quality before any
infrastructure beyond spend safety is added. The verification references
(contract qualification, progressive validation, checkpoint reuse) make a
pass honest; this reference makes the output good.

## Run the loop

1. **Labelled development set.** Five to twenty cases with a reviewed
   reference outcome and, where the task produces them, reference reasons and
   conditions. That is enough to find the largest error categories, and too
   few to show that a small score change is real. Keep a separate holdout
   that no change is allowed to look at
   ([evaluation design](evaluation-design.md#curate-cases-with-a-reason-to-exist)),
   sized for the smallest difference the decision turns on
   ([tell a change from noise](#tell-a-change-from-noise)).
2. **One baseline run** through the plainest contract that can produce the
   deliverable: draft plus judge, no checkpoints, no revisions. Retain every
   output and trace.
3. **Error analysis by category.** Read every development output against its
   reference and label each defect. Start from these categories and add the
   ones the domain shows:

   | Category | Meaning |
   | --- | --- |
   | `missed_policy` | an applicable operative provision was not retrieved or not applied |
   | `wrong_attribution` | a fact or rule was attributed to the wrong source, case or drawing |
   | `unsupported_fact` | a stated fact has no support in the supplied sources |
   | `weak_condition` | a condition is missing, unenforceable, or contradicts a reason |
   | `wrong_outcome` | the decision differs from the reference for a substantive reason |
   | `contract_failure` | schema, transport, storage or deadline failure; not a decision error |

   Record the table as data, one row per case and defect:

   ```json
   {"case": "dev-003", "category": "missed_policy", "detail": "H3 criterion c not applied",
    "stage": "retrieval", "fix_candidate": "deterministic lookup of cited policy numbers"}
   ```

   Count rows per category. The largest category names the first change.
   Contract failures are repaired before any decision-quality change is
   judged, and they are excluded from the quality denominator.
4. **One change per iteration.** Change the prompt, the retrieval, an
   exemplar, the schema or the model, never several at once. Re-run the
   whole development set, re-label, and compare category counts with the
   previous iteration. Keep the change when the targeted category shrinks
   and no other category grows; otherwise record it and revert. Re-run the
   cases the change moved before counting them fixed: one lucky run is not a
   fix. A development score that moved by less than the set's minimum
   detectable difference is recorded as "within noise", and the change is
   kept on the category evidence alone, labelled so
   ([tell a change from noise](#tell-a-change-from-noise)).
5. **Re-measure before adding controls.** A revision workflow, export
   acknowledgement or saved-stage recovery is added after the development
   score is known, not before. A spending budget and a stop are the only
   controls the loop needs.

Completion for one iteration: a dated row in the living evaluation summary
with the category counts before and after, the single change made, and the
case IDs that moved. Three iterations that each fix one case while another
breaks are the overfitting signal; prepare the
[experiment re-entry record](experiment-reentry.md) before continuing.

## Shape the prompt around the judgment

Write the prompt in this order, and keep each part to the size shown:

```text
ROLE AND TASK (two sentences)
You are a planning case officer. Decide this application and write the
reasons and conditions an officer would sign.

THE JUDGMENT YOU OWN (one paragraph)
Weigh the operative policies against the facts of this case. Where a policy
criterion is met, say which fact meets it; where it is not met, say what
would be required. Decide approve or refuse on that weighing.

WHAT YOU RECEIVE (list the inputs by label)
- case facts, from the application form and drawings, each with a source ID
- operative policy text found for each material issue, or "none found"
- exemplar decisions from other cases showing the expected structure and tone

HOW TO ANSWER (the schema, sized to the decision)
decision, reasons[{issue, policy_ids, finding}], conditions[{purpose, text}],
uncertainties[{issue, what_is_missing}]

EXEMPLARS
<labelled decisions from other cases, chosen as adk-agent-instructions describes>
```

Positive instructions carry the behaviour; a prohibition is kept only where
no positive phrasing exists, and it is paired with the target behaviour.
Everything the application already knows stays out of the prompt and is
done in code: source IDs, offsets, quotes, ID sets, coverage counts, page
spans. The model selects references and explains relevance; the server
resolves literal text (the workflow-design skill's review-contracts reference
gives the frame pattern when it is installed; the principle applies without it).

Size the output schema to what the model must decide, not what it must copy.
A field the server can fill from its own state is removed from the schema.
Free-text rationale per decision is kept; per-slot evidence maps are added
only when a downstream consumer reads them.

A prompt that has grown past a thousand words of constraints is a signal to
restart from the skeleton above: list the constraints, move each one into
code, an exemplar or the schema, and keep only the judgment.

## Keep each case's own label out of its prompt

Labelled reasons and conditions show the model what an officer's reasons
look like, so they make good exemplars for unseen cases. Which exemplars,
how many, in what order and in what format is prompt design: adk-agent-instructions
owns it (its exemplars reference), and treats the count as a variable to
measure, not a fixed number. This loop owns two things: a development case
never sees its own label, and an exemplar change is one iteration, measured
on the development set like any other change:

```python
def exemplars_for(case_id, labelled, n):
    """Pick n labelled exemplars from other cases; never the case under test.

    n and the candidate order belong to the prompt version under test.
    """
    return [c for c in labelled if c["id"] != case_id][:n]
```

Record the exemplar IDs and count with the prompt version in each
iteration's entry, so error analysis can attribute a bias to an exemplar.
This is distinct from leaking outcomes: the holdout cases have no label in
the system at all, and a development case never sees its own.

Where a library of standard conditions exists, supply it as data with stable
IDs and let the model select and adapt; conditions written free from nothing
are the weakest category in most first runs.

## Escalate the model on the plainest contract

A stronger model tested only inside a failing contract cannot show what it
adds. Compare models in two stages:

| Stage | Contract | Question answered |
| --- | --- | --- |
| 1 | Draft plus judge, no checkpoints, plain schema | Does the model decide better on the development set? |
| 2 | Full workflow with the winning model | Does the workflow preserve that gain? |

Run stage 1 for each candidate on the same development set with the same
exemplars and retrieval. Only the winner enters stage 2. If stage 2 loses the
gain, the defect is in the workflow, not the model; fix the earliest boundary
([progressive validation](progressive-validation.md)) before another model
comparison. Record model, settings and prompt version with every run; a
provider's default settings are part of the experiment.

Reasoning effort and output length are quality variables as well as cost
knobs. Treat each as a factor: vary one, hold the others, and record the
category counts. A shorter output limit that truncates reasons shows up as
`weak_condition` and `wrong_outcome`, not as a cost saving.

## Tell a change from noise

A score is a sample: other cases drawn from the same work would give a
different number, and a model run twice on one case can answer differently.
Before saying that a prompt, exemplar, model or workflow change helped, or
that it lost nothing, compute how far the score could move by chance. The
method is Evan Miller's ("Adding Error Bars to Evals: A Statistical Approach
to Language Model Evaluations", Anthropic, 1 November 2024,
https://arxiv.org/abs/2411.00640, sections 2 to 5, read 2026-10-29),
restated for an ADK project.

1. **Same cases, both versions.** Run the baseline and the candidate on the
   same cases, fixtures, criteria and judge, K runs per case (three is a
   reasonable start for a live run; a scripted-model test runs once). Score
   each trial as the whole case passing (1) or failing (0), or as its
   reward, in the trial record [result auditing](result-auditing.md#check-the-measured-units)
   describes, one file per version.
2. **Average each case's runs first.** A case scored over K runs counts once,
   as its mean. Treating K × n runs as independent samples understates the
   error, because runs of one case share its difficulty.
3. **Take the difference per case.** For each case, candidate mean minus
   baseline mean; the reported change is the average of these differences.
   Pairing removes the variation in case difficulty that both versions share,
   so the interval is narrower than comparing two separate averages.
4. **Cluster on the unit that was sampled.** When cases are variants of one
   scenario (same intent, different data) or several cases come from one
   document, customer or conversation, they move together and are not
   independent. Sum the per-case deviations from the mean difference within
   each scenario; the standard error is √(G/(G−1) × Σ over scenarios of
   (that sum)²) / n, for n cases in G scenarios. With one case per scenario
   this is the usual standard deviation of the differences over √n. The
   paper reports clustered errors more than three times the naive ones on
   some public benchmarks (reported by the source, not verified here). The
   clustered error can also come out smaller, when variants of one scenario
   move in opposite directions. With fewer than about ten scenarios either
   figure is rough: report both, and plan from the larger. Record the
   scenario of every holdout case as well, or the holdout comparison cannot
   be clustered.
5. **Report the interval and the verdict.** The 95% interval is the mean
   difference ± t × SE, with t from Student's t on G − 1 degrees of freedom
   (2.09 at 20 cases, close to 1.96 from about 60). Report baseline and
   candidate scores with the case count and K, the difference, its standard
   error, the interval and the correlation between the two versions' case
   scores. An interval wholly above zero is an improvement; one that
   includes zero is "within noise", whatever the point estimate says.
6. **State the minimum detectable difference before keeping a win.** At 5%
   significance and 80% power it is about 2.8 × SE (with t on few cases,
   slightly more): a true difference that large is found four times in five,
   and a smaller one usually is not. Write it beside every comparison: "+4
   points, within noise (minimum detectable difference 12 points on 20
   cases)".
7. **Size the holdout and the CI set from the difference that matters.**
   Cases needed n = (z[α/2] + z[power])² × V / δ², where δ is the smallest
   difference the decision turns on and V is the variance of one case's
   difference, measured on the development runs (n_dev × SE²). At 5%
   significance and 80% power (z values 1.96 and 0.84) the multiplier is
   7.85. With scenarios, the unit is the scenario: scenarios needed =
   7.85 × G_dev × SE² / δ², times the cases per scenario. The paper's
   worked example, V = 1/9, needs about 970 cases for
   δ = 3 points, about 88 for 10 points and about 22 for 20 points; so a
   20-case development set sees only differences of roughly 20 points. When
   the budget buys fewer cases, report the minimum detectable difference the
   affordable holdout gives instead of a holdout verdict on smaller
   differences. A budget given in runs converts to cases: runs ÷ (versions ×
   runs per case).
8. **Runs reduce run-to-run noise only.** K runs per case divide the
   within-case noise by K and leave the variation between cases untouched.
   In the paper's uniform-difficulty example, two runs cut the variance by a
   third and no number of runs by more than two thirds. When most of V is
   between cases, add cases, not runs. On a small sample the run-noise
   estimate can exceed V itself; the split is then unknown, so plan on
   cases at the runs per case already used. Do not lower the temperature to
   reduce noise: the paper shows it can move the score itself, and
   adk-model-and-output-contracts keeps Gemini 3 at its default of 1.0.

Run the bundled helper on the two trial records rather than computing this
by hand:

```bash
python "$SKILL_DIR/scripts/paired_difference.py" \
  --baseline runs/baseline.csv --candidate runs/candidate.csv \
  --target-difference 0.05 --plan-cases 100 --plan-runs 5
```

It reads CSV or JSON Lines rows with `case_id` and `reward`, `score` or a
`pass`/`fail` `outcome`, and an optional `scenario`; `infra_error` rows are
counted and left out. It averages runs per case, clusters on `scenario`
when present, prints the interval, the verdict, the minimum detectable
difference and the share of the variance that is run-to-run noise. With
`--target-difference` it gives the cases needed, and with `--plan-cases` the
difference that many cases could detect. Both are at the runs per case
already used, and again at `--plan-runs` when the noise split can be
estimated. Plans keep the sample's cases per scenario. `--require improved` exits 1 unless
the interval lies above zero; `--require not-worse --margin 0.02` exits 1
unless the candidate loses less than two points (for a cheaper model or a
refactor). Exit 3 means a case has scores in one file only, and the figures
may change when it runs. The helper uses only the standard library, makes no
external calls and does not import the project.

Error analysis on a development set of five to twenty cases still works:
reading every output finds the defects, and a category that falls from five
cases to zero is evidence a reviewer can check case by case. The interval
governs the claims made from scores: a development score, a holdout result,
a release comparison and a figure in a presentation.

## Keep the measurement honest

- The development set measures progress; the holdout measures generalization
  once, at the end, with the frozen method. A holdout case used to guide a
  fix moves into development and is replenished.
- Report successes and attempts separately, by category, with case IDs. A
  percentage without the category table hides which defect moved. A score
  compared with another carries its paired interval and minimum detectable
  difference ([tell a change from noise](#tell-a-change-from-noise)).
- The judge is calibrated on fixed evidence before it grades candidates
  ([evaluation design](evaluation-design.md#calibrate-the-judge-on-fixed-evidence)).
  Human review of a sample of judge verdicts each iteration keeps it honest.
- The deliverable the reviewer will judge is regenerated with the final
  method ([progressive validation](progressive-validation.md#keep-the-deliverable-and-the-method-together)).

Completion: the living summary shows, per iteration, one change, the category
counts before and after, and the development score; the final holdout run
used the frozen method; and the report names the largest remaining category.

Sources reviewed 6 October 2026 for the loop shape: Hamel Husain's
error-analysis workflow (read traces, binary pass/fail, group failures into
categories, label every trace), summarised at
[tessl.io](https://tessl.io/registry/skills/github/hamelsmu/evals-skills/error-analysis)
and [arize.com](https://arize.com/blog/ai-evals-maven-course-homework-the-recipe-bot-workflow/);
prompt-structure guidance on positive instructions and exemplars at
[tredence.com](https://www.tredence.com/blog/prompt-engineering-best-practices-for-structured-ai-outputs).
These are practice summaries, not evidence for a particular target project.
