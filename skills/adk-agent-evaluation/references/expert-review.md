# Label with domain experts

Read this when the labels do not exist yet: someone must decide what a good
answer is, the people who know are subject-matter experts (underwriters,
case officers, clinicians, support leads), and a development set, a failure
taxonomy or a judge calibration set has to come out of their time. The
[quality iteration](quality-iteration.md) loop and the judge calibration in
[evaluation design](evaluation-design.md#calibrate-the-judge-on-fixed-evidence)
start where this ends: with reviewed labels, versioned criteria and a gold
set whose provenance is recorded.

The deliverables are a failure taxonomy, a criteria file with a version, a
gold set in the [gold-set schema](../assets/gold-set-schema.md), the
agreement report from `scripts/label_agreement.py`, and a dated row in the
living evaluation summary (the document the plan's "What the reviewer reads"
table names; `docs/evaluation/README.md` when the project has none). Use the [session plan](../assets/expert-session-plan.md)
and the [labelling guide](../assets/labelling-guide.md) as the experts'
material.

## Settle who decides before anyone labels

- **One quality decision-maker.** Name one domain expert whose verdict is
  final on what counts as a failure, and record the name in the plan.
  The evals FAQ (Husain and Shankar) calls this the "benevolent dictator"
  and recommends it for most small and medium teams because it removes
  annotation conflicts. On a
  client engagement this is a client person, not the consultant; the
  consultant runs the session and owns the method.
- **The builder reads first.** Before the session, the developer annotates
  at least the first 30 traces alone (the FAQ: "annotate at least the first
  30 yourself"). That finds the broken traces, the unreadable displays and
  the obvious failures, so the experts' hours go on judgement.
- **A second expert only to measure agreement.** Two experts label the same
  overlap set independently, before any discussion, when the criteria will
  be used by more than one person (several reviewers, a judge, a release
  gate). Their disagreements go to the decision-maker, who records the
  reason with the verdict.

## Run the session

When labels already exist (a first pass, a pilot's reviews), the session is
a follow-up, not a first one: spend expert time first on disagreements
that form a pattern (one ruling settles many), then on the borderline
rulings that raise the criteria version, then on a fresh independent
overlap to re-measure agreement; open coding of new traces comes last, to
check saturation. The [session plan](../assets/expert-session-plan.md) has
both agendas.

Ask the decision-maker for a slot in the plan's calendar as early as the
invitation allows; expert time is a calendar wait as well as hours, and the
designer's labelling estimate covers the experts' hours as well as the
developer's.

1. **Sample traces.** Draw about 100 diverse traces: real or replayed
   conversations covering the outcome classes, the hard cases the experts
   name, and recent failures. Show each trace whole (input, retrieved
   sources, tool calls and results, final answer), never the answer alone.
2. **Open coding.** For each trace the expert writes, in their own words,
   what is wrong from the user's side, and a pass or fail for the trace.
   No categories yet; the notes are data.
3. **Axial coding.** Group the notes into a failure taxonomy: named failure
   modes with a one-line definition, a pass example and a fail example
   each, and a count. The FAQ calls this "the most important step". Merge
   notes that describe the same defect; split a category whose examples
   need different fixes.
4. **Stop at saturation.** Keep reviewing until new traces stop revealing
   failure modes or changing existing ones (the FAQ recommends at least 100
   traces, and more while still learning). Make the stop observable: record
   the trace number at which each category first appeared, and stop when a
   further block of traces adds no category and changes no definition. The
   block size is the project's choice (20 is a reasonable start); a count
   below 100 needs a recorded reason, such as a narrow task with few
   outcome classes.
5. **Write the criteria.** One binary criterion per failure mode, stated so
   a second expert can apply it: what fails, what passes, the borderline
   ruling. Version the file (`v01`) and date it.
6. **Label per criterion.** Each trace gets pass or fail on every criterion
   that applies, with a one-sentence critique on every fail and on every
   borderline pass. Binary labels force a decision boundary; a 1 to 5 scale
   is hard to calibrate for people and judges alike, and Yan reports that
   none of the stakeholders he has seen ask for granular scores, to move
   thresholds later, went on to do so. The critiques become the judge's few-shot examples and the
   explanation in the gold set.

## Expect the criteria to drift, and re-review

Shankar et al. ("Who Validates the Validators?", UIST 2024, arXiv
2404.12272) observed that people need criteria to grade outputs, but
grading outputs is how they define the criteria: participants refined and
reinterpreted criteria as they graded, and went back to change earlier
grades. Plan for it:

- Raise the criteria version whenever a definition or borderline ruling
  changes, and record which version each label was given under.
- When the criteria settle, re-review the labels given under an older
  version of a criterion whose definition or borderline ruling changed:
  all of them when the definition changed, and at least those whose
  critique touches the changed ruling when only a ruling was added. The
  checker reports a rater whose labels span versions; `--criteria-version`
  computes agreement within one version, to see whether a change helped.
- When the agent, model or prompt changes the outputs substantially,
  sample new traces and check that the taxonomy still covers them before
  reusing the criteria.

## Measure agreement, then adjudicate

Run the checker on the overlap set:

```bash
python3 "$SKILL_DIR/scripts/label_agreement.py" --labels labels/experts.csv
```

It reports per criterion and rater pair the shared cases, percent
agreement, Cohen's kappa (agreement beyond chance for two raters) and the
fail share, and lists every disagreement. There is no universal kappa
threshold; the script's 0.6 is a placeholder to set in the plan. Yan
reports human inter-rater kappa as low as 0.2 to 0.3 in practice. When it
is low:

- **High raw agreement, low kappa:** the classes are imbalanced (nearly
  everything passes), so chance agreement is high. Add cases of the rarer
  class before concluding anything.
- **Genuine disagreement:** read the listed cases with both critiques. A
  pattern means the criterion is ambiguous: rewrite it, raise the version
  and relabel the overlap. Scattered cases go to the decision-maker.
- **Kappa undefined:** each rater gave one label to every case; the set
  cannot show agreement.

Before any adjudication, `--judge <name> --reference consensus` scores the
judge against the cases every expert labelled alike. That set leaves out
the hard cases, so the rates are indicative only: useful to decide whether
the judge is worth calibrating, never a calibration result.

For more than two raters or an ordinal scale, use Krippendorff's α as in
[evaluation design](evaluation-design.md#calibrate-the-judge-on-fixed-evidence).
The adjudicated verdict is written as rater `adjudicated`, with the
decision-maker in `labeller` and the reason as critique.

## Keep the gold set with its provenance

Every gold row carries the case, criterion, label, critique, labeller,
date, criteria version and split ([schema](../assets/gold-set-schema.md)).
A label without its criteria version cannot be told apart from a
pre-drift label; the checker reports gold rows missing the labeller, the
date or the version.

Size and split it for the judge it will calibrate. The FAQ's figures: label
100 to 200 examples per failure mode; put 10 to 20 percent in a train split
(examples that may appear in the judge prompt), 40 to 45 percent in dev
while refining the judge, and keep 40 to 45 percent as a test split used
once; aim for 30 to 50 passes and 30 to 50 fails in each of dev and test.
Yan recommends at least 50 to 100 failures in 200 or more samples. Where
real failures are scarce, Yan prefers organic failures (for example from a
smaller model) over synthetic defects, which tend to be out of
distribution. A 20 to 50 case development set for quality iteration is a
smaller thing; label it the same way and grow it towards these sizes when a
judge needs calibrating.

## Calibrate one judge per failure mode

Both the FAQ and Yan recommend a separate judge per failure mode over one
judge asked to catch everything. For each judge:

1. Write its prompt from the criterion, with train-split critiques as
   examples. Never show it dev or test labels.
2. Iterate on dev. Measure on test once, with the frozen prompt and pinned
   model.
3. Report TPR and TNR with **fail as the positive class**, as the FAQ
   defines them: TPR is the share of real failures the judge catches; TNR
   the share of good outputs it passes. Raw agreement hides a judge that
   passes everything: on a set with 10 percent failures it scores 90
   percent agreement and catches none.

```bash
python3 "$SKILL_DIR/scripts/label_agreement.py" \
  --labels labels/gold.csv labels/judge-cites-policy.jsonl --judge judge-cites-policy
```

The checker scores the `test` split by default, notes when the gold set has
no split (the rates are then not held out), and reports NOT REPORTED when
either class has fewer than `--min-per-class` cases (default 30, after
the FAQ's 30 to 50 per class). Set `--min-tpr` and `--min-tnr` in the plan;
favour TPR when a missed failure is costly and TNR when false alarms would
flood a human review queue. A judge below threshold is fixed by rewriting
the criterion or examples and rerun on dev, never tuned on test.

When the judge then grades unlabelled production traces, its observed fail
rate is biased by its errors. With the measured rates, the corrected
failure rate is (observed fail rate + TNR − 1) / (TPR + TNR − 1), meaningful
only when TPR + TNR is well above 1; report it beside the observed rate,
with the test-split sizes.

## Completion

The plan records the decision-maker; the taxonomy has counts and the trace
number of the last new category; the criteria file is versioned; labels
given under older versions have been re-reviewed; the agreement report and
its adjudications are retained; each judge has TPR and TNR on a test split
with both class counts, or a NOT REPORTED line naming the labels still
needed.

Sources read 25 October 2026: Hamel Husain and Shreya Shankar,
[AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/)
(the evals FAQ, last modified 21 September 2026) (trace counts,
saturation, open and axial coding, benevolent dictator, Cohen's kappa,
TPR and TNR with fail as positive, splits, one judge per failure);
Shankar et al., [Who Validates the Validators?](https://arxiv.org/abs/2404.12272)
(criteria drift; nine-practitioner qualitative study); Eugene Yan,
[Product evals in three simple steps](https://eugeneyan.com/writing/product-evals/)
(binary labels, failure counts, one evaluator per dimension, observed
kappa ranges). These are practitioner guidance and one qualitative study,
not measurements of any target project.
