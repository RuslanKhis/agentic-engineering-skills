# Reviewer vs writer: PA-2026-0177-r2 (rejected) and PA-2026-0152-r1 (accepted)

Tier: offline. Method: reading saved run files, case sources and `pipeline/coverage_check.py`, and tracing the
checker by hand. `analysis/replay_checks.py` is written but was NOT RUN: shell access was unavailable in this
session. The traces below are hand-derived and should be confirmed by running it
(`python -I analysis/replay_checks.py`; it only reads). No provider calls, nothing under `runs/` changed.

## Main finding

The rejection of 0177-r2 was produced by the deterministic checker, not by the review model's judgement.
`pipeline/stages.py:40-42` sets `verdict = "reject"` whenever `review_findings` is non-empty, whatever the model
says. The checker has two findings on this draft, and both are defects in the checker.

| # | Finding on 0177-r2 | Hand trace | Verdict on the finding | Evidence |
|---|---|---|---|---|
| 1 | "gaps listed although every source is accounted for; remove them" | APP-FORM, AGT and TS are all cited, so `missing` is empty and `draft["gaps"]` is not | **Checker wrong.** The rule equates "every document cited" with "nothing unresolved". The gap is real: TS@1:p1:3 "Stem diameter not measured: access ... refused", TS@1:p1:4 "Root protection area therefore not calculated". | `coverage_check.py:31-32` |
| 2 | "LP-ENV3 is cited but not applicable" | `applicable_policies` reads only APP-FORM, DAS and AGT. The trigger "root protection area" is not in them (only in TS, which is excluded) | **Checker wrong.** T1 is a TPO oak, 3.5 m from the new wall (APP-FORM:4, TS:2). A policy on protected trees is engaged. | `coverage_check.py:7,14,37-40` |
| 3 | Model: "R2 ... ENV3 ... not engaged ... revise to approve" | The review prompt had the checker's findings appended (`stages.py:34-35`) | **Not independent evidence.** It repeats finding 2. Its `unsupported` label for R2 cites only TS:2 and ENV3:2 and ignores TS:3-4 and ENV3:4. | `review.json`, `stages.py` |

Why 0152-r1 passed: both documents were cited, `gaps` was empty, and the applicant's form happens to contain the
words "root protection area", so ENV3 counted as applicable. The accept/reject difference between the two cases is
partly lexical luck, not evidence of draft quality.

Consequence for a paid retry: any honest draft of 0177 that keeps the gap or cites ENV3 gets the same forced reject.
A draft that passes would have to hide the unresolved root protection area or drop the tree policy, which is the
opposite of what a planning officer needs. A retry would spend money without testing anything.

## Is the writer also wrong? (separate from why it was rejected)

All cited span ids exist and both quotations are verbatim (checked against the application.json line numbering
in `pipeline/sources.py:34-37`). The conflict (AGT vs APP-FORM/TS) and the gap are correctly reported. Two points a
human should look at; I did not adjudicate them:

- **R1 may be unsupported, and the reviewer accepted it.** H4 requires "subordinate in scale and height".
  The cited APP-FORM:3 only says "two-storey side extension". No document gives dimensions or height. The model
  marked R1 `supported`, so it is a possible false accept. The same pattern appears in the accepted 0152 R1.
- **R2 to "refuse" is a judgement call.** ENV3:4 covers "where a tree survey is *absent*". Here the survey exists but is incomplete.
  The writer carries that sentence over to an incomplete survey. "Refuse", "approve with conditions" and
  "ask for the survey to be completed" are all defensible. The schema only offers approve, approve_with_conditions
  and refuse, so there is no "request more information" option. The claim "no arboricultural method statement is
  supplied" is an absence and cannot be cited.

## Conclusion on the question asked

On this evidence the cause of the rejection is the checker, not the reviewer model and not the writer. The
reviewer model is contaminated by the checker output, so its own accuracy cannot be read from this run. Writer
quality is not shown to be good: R1 and the refuse-vs-defer choice need an officer. Two cases (one reject, one accept)
show the checker's logic faults; they say nothing about rates.

## Questions I could not ask, and the assumptions I proceeded on

1. Is the tree survey (TS) an applicant document? Assumed yes (it is under the application and records access refused
   on the survey day). I did not need this for the conclusion, since ENV3 is triggered by the TPO either way.
2. Should "refuse" be the answer when RPA is unknown? Assumed that is for the planning officer or tree specialist;
   not decided here.
3. May `pipeline/coverage_check.py` be changed now? Assumed no (you asked for the diagnosis first). Not edited.

## Recommended next steps (not done)

1. Fix the checker offline (no provider calls). Treat "all sources cited" as coverage only and do not tie it to
   gaps. A gap should be checked against the source text (does a source say something was not measured or not
   supplied?) or left to the officer. Add tree-survey/TPO triggers (e.g. "protected", "Tree Preservation Order",
   "tree") and include TS in the trigger text, or at least stop treating an uncited-trigger miss as proof that a
   policy does not apply.
2. Add unittest regression cases built from 0177-r2 (must produce no findings) and a draft that cites a
   genuinely irrelevant policy (must still be flagged), using `tests/doubles.py`.
3. Get an officer or tree specialist to label R1 and the R2 decision for 0177. Until then, no accuracy figure for
   the reviewer or writer.
4. Decouple the model review from the checker findings (or record both verdicts separately) so each can be
   measured.
5. Only then plan one approved paid retry. `campaign/ledger.json` was not touched.
