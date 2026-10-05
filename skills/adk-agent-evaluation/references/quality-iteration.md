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
   conditions. Keep a separate holdout that no change is allowed to look at
   ([evaluation design](evaluation-design.md#curate-cases-with-a-reason-to-exist)).
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
   and no other category grows; otherwise record it and revert.
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
- two exemplar decisions showing the expected structure and tone

HOW TO ANSWER (the schema, sized to the decision)
decision, reasons[{issue, policy_ids, finding}], conditions[{purpose, text}],
uncertainties[{issue, what_is_missing}]

EXEMPLARS
<two labelled decisions from other cases, trimmed to reasons and conditions>
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

## Use the labelled cases as exemplars, not as answers

Labelled reasons and conditions show the model what an officer's reasons
look like: structure, tone, how a policy criterion is cited, how a condition
is worded. Use them as exemplars for unseen cases. For a development case,
select exemplars with leave-one-out so the case under evaluation never sees
its own label:

```python
def exemplars_for(case_id, labelled, n=2):
    """Pick n labelled decisions from other cases; never the case under test."""
    return [c for c in labelled if c["id"] != case_id][:n]
```

Trim exemplars to the parts whose shape matters: reasons and conditions, with
the case-specific facts shortened. Choose exemplars whose issues resemble the
current case when the set is large enough to allow it. This is distinct from
leaking outcomes: the holdout cases have no label in the system at all, and a
development case never sees its own.

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

## Keep the measurement honest

- The development set measures progress; the holdout measures generalization
  once, at the end, with the frozen method. A holdout case used to guide a
  fix moves into development and is replenished.
- Report successes and attempts separately, by category, with case IDs. A
  percentage without the category table hides which defect moved.
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
