# Expert labelling session: <agent or workflow>

Fill the angle brackets from the plan and the discovery brief; send the
invitation once the decision-maker has agreed the slot.

## Invitation

> **Subject:** <n> hours to decide what a good <answer / decision> looks like
>
> We are building <agent> to help <users> with <task>. Before we measure
> it, we need your judgement on real examples: which of its answers you
> would accept, which you would not, and why. Your verdicts become the
> standard the system is tested against.
>
> **When:** <date, time, length>; <second session if needed>
> **What you will do:** read about <n> recorded <cases / conversations>,
> each shown in full (question, documents found, actions taken, answer);
> mark each one acceptable or not and write one sentence on anything wrong.
> No preparation needed. <Optional: a short note from you beforehand on
> the two or three mistakes you would most hate to see.>
> **Data:** <synthetic / de-identified / production under <access rule>>;
> nothing leaves <where it is stored>.
> **Who decides:** <decision-maker> has the final say where reviewers
> differ.

## Roles

| Role | Person | Responsibility |
| --- | --- | --- |
| Quality decision-maker | <name, role> | Final verdict on failures and borderline rulings; signs off the criteria version |
| Second expert (agreement only) | <name, role or none> | Labels the overlap set independently, before discussion |
| Facilitator | <developer or consultant> | Runs the session, records notes, maintains the criteria file and gold set |

## Before the session

- [ ] Developer has annotated the first 30 or more traces alone and fixed
      broken traces and displays.
- [ ] About 100 diverse traces sampled: outcome classes, expert-named hard
      cases, recent failures. Sample recorded with case IDs.
- [ ] Each trace shown whole: input, retrieved sources, tool calls and
      results, final answer.
- [ ] Labelling guide and an empty label file in the
      [schema](gold-set-schema.md) ready; criteria file at `v01` (may be
      empty before open coding).
- [ ] Overlap set chosen for the second expert: <n> cases, both classes
      expected.

## Agenda for a first session (<length>)

| Block | Time | Output |
| --- | --- | --- |
| Purpose and the decision-maker's role | 10 min | Agreement on what a failure is for this task |
| Open coding: read traces, pass or fail, one-sentence note | <most of the session> | Notes per trace |
| Axial coding: group notes into failure modes, name and define each | 30–45 min | Draft taxonomy with counts and first-seen trace numbers |
| Criteria: one binary criterion per failure mode, borderline rulings | 20–30 min | Criteria file `v01` or a raised version |
| Next steps: overlap labelling, re-review, who adjudicates | 10 min | Dates in the plan |

Stop open coding at saturation: a further block of <20> traces adds no
failure mode and changes no definition, and at least 100 traces have been
read (or the reason for fewer is written down).

## Agenda for a follow-up session, when labels already exist (<length>)

| Block | Time | Output |
| --- | --- | --- |
| Agreement report: kappa per criterion, the patterns in the disagreements | 15 min | Shared view of where the criteria are ambiguous |
| Rule on patterned disagreements, a few cases per pattern | 40–60 min | Borderline rulings; criteria version raised |
| Independent labelling of a fresh overlap under the new version | 45–60 min | Labels to re-measure kappa |
| Adjudicate the remaining disagreements; re-review older labels the new rulings could flip | rest, or offline | `adjudicated` rows with reasons |
| Open coding of new traces to check the taxonomy still covers them | if time remains | New failure modes or none |

## After the session

- [ ] Taxonomy recorded with counts and the trace number of the last new
      failure mode.
- [ ] Criteria file versioned and dated; every change since `v01` noted.
- [ ] Labels given under older criteria versions re-reviewed.
- [ ] Overlap labelled by both experts independently; `label_agreement.py`
      run; disagreements adjudicated by the decision-maker with reasons.
- [ ] Gold set written with provenance and splits; living evaluation
      summary row dated.
- [ ] Hours spent by each expert recorded against the plan's estimate.
