# NOTES — improving the draft-stage decisions

Dated log in the order the steps were actually done. Method: the
`adk-agent-evaluation` skill's quality-iteration loop (labelled development
set, one baseline run, error analysis by category recorded as data, one
change per iteration, re-measure after each). Everything ran offline against
the rule-based model double in `draft_stage.py`; no provider was called.
Interpreter: `python3.11` (3.11.4). The bare `python3` on PATH is 3.9.13; it
produces identical outputs for this workspace but all measurements below
were taken with 3.11.

Retained artefacts: `runs/<NN>-<name>/` holds the outputs and prompt of each
measured run; `analysis/iteration-N*.json` holds the hand-labelled error
table for each run.

## 2026-10-06 — Step 0: inspect and reproduce the baseline

Read `README.md`, `request.txt`, `prompt.txt` (1,600 words), `draft_stage.py`
(the double's triggers are documented in its docstring), `score.py`,
`policies.json`, the five cases and the five retained outputs.

Boundaries: no identity, mutation or credential surface here; the only
"provider" is the double, and the only contract limit is
`REQUEST_BYTE_LIMIT = 10_500` bytes on the request. The double never reads a
case label. Labelled set: 5 development cases, no holdout exists (recorded
as a gap at the end).

Ran:

    cp outputs/*.json runs/00-baseline-retained/
    python3.11 draft_stage.py && python3.11 score.py
    diff -r outputs runs/00-baseline-retained   # identical

Observed (baseline):

    case     decision  recall  conds  schema  cited
    dev-001  True      1.0     1      True    D1,H3
    dev-002  False     0.0     1      True    D1
    dev-003  True      0.5     1      True    G4
    dev-004  True      1.0     1      True    D1,H3
    dev-005  False     0.0     0      False
    decisions matched 3/5; mean policy recall 0.50; schema failures 1

Request sizes: 10,363 / 9,912 / 10,113 / 10,360 / 10,594 bytes. dev-005 is
94 bytes over the limit and the double returned truncated non-JSON.

## 2026-10-06 — Step 1: error analysis by category (before any edit)

Read every output against its label; table in
`analysis/iteration-0-baseline.json`. Counts:

| category | rows | cases |
| --- | --- | --- |
| missed_policy | 2 | dev-002 (H3 not retrieved), dev-003 (SPD-T2 not retrieved) |
| wrong_outcome | 1 | dev-002 (approve vs refuse; downstream of the missed H3) |
| weak_condition | 2 | dev-003 (splay imposed despite written waiver), dev-004 (materials "match" condition where D1 requires samples) |
| wrong_attribution | 1 | dev-004 (7.8 m ridge attributed to roof-plan-G, stated in elevation-H) |
| unsupported_fact | 0 | |
| contract_failure | 1 | dev-005 (request over the byte limit) |

Not counted as defects: dev-001's conditions are strings rather than
`{purpose, text}` objects, which is what the current prompt's Section 7 asks
for, so it is a schema-shape difference, not a decision error.

Decision from the table: repair the contract failure first (it is excluded
from the quality denominator, which is 4 cases until it is repaired). The
largest decision-quality category is then `missed_policy` (2 rows, and the
single `wrong_outcome` is caused by one of them), so the first quality
change targets retrieval, not the prompt and not a checker.

## 2026-10-06 — Step 2 (iteration 0b): repair the contract failure

Change (one): `prompt.txt` — removed Section 10 "Repetition of critical
prohibitions", which repeated Section 1 word for word (497 bytes). Nothing
else edited; the double keys on none of that text.

Ran `python3.11 draft_stage.py && python3.11 score.py`; retained in
`runs/01-contract-repair/`.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  False     0.0     1      True    D1
    dev-003  True      0.5     1      True    G4
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 4/5; mean policy recall 0.70; schema failures 0

Request sizes 9,866 / 9,415 / 9,616 / 9,863 / 10,097 bytes. dev-001..004
outputs are byte-identical to the baseline apart from `request_bytes`, so
the repair moved only the contract failure. dev-005 is now in the quality
denominator (5 cases). Re-labelled in
`analysis/iteration-0b-contract-repair.json`: dev-005's decision and all
three policies match; its H3 finding cites the driveway dimensions, a real
fact that bears on T2 rather than H3(a), so I added the domain category
`irrelevant_finding` (1 row). Counts: missed_policy 2, wrong_outcome 1,
weak_condition 2, wrong_attribution 1, irrelevant_finding 1,
contract_failure 0. Kept. Largest category is still `missed_policy`.

## 2026-10-06 — Step 3 (iteration 1): retrieval — the largest category

Change (one): `draft_stage.py` gained `retrieve(case)`, run before
`build_request`. It is a deterministic lookup over `policies.json`:
(1) any policy named inside an already-retrieved policy's text is added
(G4 says "Table 2 of the Design SPD", which is SPD-T2); (2) any policy that
shares at least two content terms with the case facts is added. The
output now records `retrieval_added`. The double (`model`, `_facts`) and
the prompt were not touched.

Why first: `missed_policy` was the largest category, and the one
`wrong_outcome` (dev-002 approve instead of refuse) was caused by it.

Ran `python3.11 draft_stage.py && python3.11 score.py`; retained in
`runs/02-retrieval/`. Policies added: dev-002 +H3 (7 shared terms),
dev-003 +SPD-T2 (cross-reference from G4, and 12 shared terms); nothing
added elsewhere.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 5/5; mean policy recall 1.00; schema failures 0

Re-labelled (`analysis/iteration-1-retrieval.json`): missed_policy 2 -> 0,
wrong_outcome 1 -> 0, nothing grew; dev-001/004/005 byte-identical to the
previous run. Kept. Limits noted: D1 overlaps zero terms with every case,
so the term rule could never retrieve D1 on its own (untested here because
upstream retrieval already supplies it); dev-002 carries a surplus D1
reason with no fact, which is not an unsupported fact and is not counted.

Remaining: weak_condition 2 (dev-003, dev-004), wrong_attribution 1,
irrelevant_finding 1. Largest is weak_condition; dev-003 is the movable row.

## 2026-10-06 — Step 4 (iteration 2): output schema `waives` — REVERTED

Change (one): `prompt.txt` Section 7 gained a `"waives"` list (requirement,
policy_ids, source_id) and Section 8's "never impose a waived requirement"
became the positive instruction to record the written confirmation under
`waives` and rely on it (+477 bytes). Target: `weak_condition` (largest, 2
rows), movable row dev-003.

Ran the stage and scorer; retained in `runs/03-waives-schema/`.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  False     0.0     0      False
    decisions matched 4/5; mean policy recall 0.80; schema failures 1

dev-003 moved as intended (finding "splay waived in writing", condition is
the 5.0 m setback / inward opening, no splay). But dev-005's request grew
to 10,574 bytes and failed the contract again: `contract_failure` 0 -> 1.
Rule: a change that grows another category is recorded and reverted.
Reverted `prompt.txt` to `runs/02-retrieval/prompt.txt`, re-ran, and
confirmed the outputs are byte-identical to run 02.

Diagnosis: the prompt (~1,590 words of constraints) has no headroom, so any
addition breaks the largest case. That is the reference's restart signal.
Next: iteration 3 restarts the prompt from the skeleton with the plain
schema, no exemplars and the existing FACTS / SOURCE IDS layout, so that the
only thing it should move is request size. `waives` comes back afterwards
as its own iteration.

## 2026-10-06 — Step 5 (iteration 3): restart the prompt from the skeleton

Change (one): `prompt.txt` replaced by a 211-word version 42 built on the
reference skeleton: role and task, the judgment owned, the inputs by label,
and a plain output schema (decision, reasons, conditions, uncertainties).
Deliberately without exemplars, without `waives`, and keeping the FACTS /
SOURCE IDS layout, so that the restart itself is the only thing measured.

Ran the stage and scorer; retained in `runs/04-prompt-restart/`. Requests
fell to 2,455 / 2,484 / 2,553 / 2,452 / 2,686 bytes.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 5/5; mean policy recall 1.00; schema failures 0

All five outputs are byte-identical to run 02 apart from `request_bytes`.
Categories unchanged (weak_condition 2, wrong_attribution 1,
irrelevant_finding 1), contract failures 0, headroom about 8 KB per case.
Kept (`analysis/iteration-3-prompt-restart.json`). Observation: the schema
now describes `{purpose, text}` conditions but outputs are still strings;
the double writes objects only when exemplars are present.

## 2026-10-06 — Step 6 (iteration 4): `waives` in the skeleton schema

Change (one): `prompt.txt` schema gained the `"waives"` list (requirement,
policy_ids, source_id) and one positive sentence: where the highway
authority has confirmed in writing that a requirement is not required,
record it under `waives` with the letter's source ID and rely on it instead
of imposing the condition. 262 words. Same change as iteration 2, now with
headroom.

Ran the stage and scorer; retained in `runs/05-waives-schema/`. Requests
2,806 / 2,835 / 2,904 / 2,803 / 3,037 bytes.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 5/5; mean policy recall 1.00; schema failures 0

dev-003 now reads "splay waived in writing" and imposes the setback /
inward-opening condition instead of the splay, matching the label's
condition in substance. The other four outputs are byte-identical to run
04. weak_condition 2 -> 1, nothing grew, no contract failure. Kept
(`analysis/iteration-4-waives-schema.json`).

Remaining: weak_condition 1 (dev-004, the double has no samples-condition
behaviour), wrong_attribution 1 (dev-004), irrelevant_finding 1 (dev-005,
the double attaches its first measured fact to H3). The only movable row is
the attribution one.

## 2026-10-06 — Step 7 (iteration 5): inline source labels on facts

Change (one): `build_request` now renders each fact as `[source-id] text`
on its own line and drops the separate SOURCE IDS list; the prompt's WHAT
YOU RECEIVE line describes that layout. Target: `wrong_attribution`
(dev-004), the only remaining row with a fix outside the double.

Ran the stage and scorer; retained in `runs/06-inline-facts/`.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 5/5; mean policy recall 1.00; schema failures 0

The score table cannot see this change (no attribution column); the
category table can: dev-004's `facts_used` now lists 7.8 m under
elevation-H. Only dev-004 changed. wrong_attribution 1 -> 0, nothing grew.
Kept (`analysis/iteration-5-inline-facts.json`).

Remaining: weak_condition 1 (dev-004) and irrelevant_finding 1 (dev-005),
both inside the double with no documented trigger. Uncounted: conditions
are still strings against a `{purpose, text}` schema.

## 2026-10-06 — Step 8 (iteration 6): two leave-one-out exemplars

Change (one): `exemplars_for(case_id, labelled, n=2)` in `draft_stage.py`
appends two labelled decisions from other cases, trimmed to reasons and
conditions, as EXEMPLAR blocks; the prompt's WHAT YOU RECEIVE names them as
examples of form. Checked before the run that no case's own label text
appears in its exemplars. Not a counted category: it closes the shape
mismatch between the `{purpose, text}` schema and the string conditions the
outputs carried, which the reference assigns to exemplars.

Ran the stage and scorer; retained in `runs/07-exemplars/`. Requests
3,948 / 4,175 / 4,078 / 3,977 / 4,211 bytes.

    dev-001  True      1.0     1      True    D1,H3
    dev-002  True      1.0     0      True    D1,H3
    dev-003  True      1.0     1      True    G4,SPD-T2
    dev-004  True      1.0     1      True    D1,H3
    dev-005  True      1.0     2      True    D1,H3,T2
    decisions matched 5/5; mean policy recall 1.00; schema failures 0

Decision, reasons and `facts_used` byte-identical to run 06 for all five;
only the conditions changed shape (now objects with purposes matching the
labels). Nothing grew. Kept (`analysis/iteration-6-exemplars.json`).
Stopped here: the two remaining rows are limits of the double.

## 2026-10-06 — Step 9: verification and living summary

Second invocation: ran `python3.11 draft_stage.py` again; outputs
byte-identical to `runs/07-exemplars/`, no extra files, no configuration
churn. The bare `python3` (3.9.13) produces the same outputs and score.

### Living evaluation summary (one row per measured run)

| run | change (one) | missed_policy | wrong_outcome | weak_condition | wrong_attribution | irrelevant_finding | contract_failure | decisions | recall | kept | cases moved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 00 baseline | none | 2 | 1 | 2 | 1 | n/a (dev-005 unreadable) | 1 | 3/5 | 0.50 | - | - |
| 01 contract repair | prompt: drop duplicated Section 10 | 2 | 1 | 2 | 1 | 1 | 0 | 4/5 | 0.70 | yes | dev-005 |
| 02 retrieval | code: deterministic lookup over policies.json | 0 | 0 | 2 | 1 | 1 | 0 | 5/5 | 1.00 | yes | dev-002, dev-003 |
| 03 waives schema | prompt v41: `waives` entry | 0 | 0 | 1 | 1 | 1 | 1 | 4/5 | 0.80 | NO, reverted | dev-003 fixed, dev-005 broke |
| 04 prompt restart | prompt v42 skeleton, plain | 0 | 0 | 2 | 1 | 1 | 0 | 5/5 | 1.00 | yes | none (size only) |
| 05 waives schema | prompt v42: `waives` entry | 0 | 0 | 1 | 1 | 1 | 0 | 5/5 | 1.00 | yes | dev-003 |
| 06 inline facts | code: `[source-id]` fact labels | 0 | 0 | 1 | 0 | 1 | 0 | 5/5 | 1.00 | yes | dev-004 |
| 07 exemplars | code+prompt: two leave-one-out exemplars | 0 | 0 | 1 | 0 | 1 | 0 | 5/5 | 1.00 | yes | none (condition shape) |

Final development score: decisions matched 5/5, mean policy recall 1.00,
schema failures 0, conditions as `{purpose, text}` on all approvals, none
on the refusal, attribution correct in all `facts_used`.

Largest remaining category: `weak_condition` and `irrelevant_finding`, one
row each, both dev-004/dev-005 behaviours inside the model double that no
documented trigger moves (the double has no samples-condition rule and
attaches its first measured fact to H3). With a real model these would be
the next targets: a standard-conditions library with stable IDs for the
samples condition, and an exemplar whose H3 finding cites a scale fact.

### What was and was not verified

- Everything ran offline against the rule-based double in
  `draft_stage.py`; no provider was called and no network was needed. The
  double, `_facts` and `model`, were not modified.
- The five development cases are the whole labelled set; there is no
  holdout, so the 5/5 is a development score, not evidence of
  generalisation. A holdout with reviewer-labelled references is the
  missing prerequisite before claiming more.
- The term-overlap retrieval rule never retrieved D1 on its own (zero
  shared terms with every case); it is untested, not failing, because
  upstream retrieval already supplied D1 everywhere.
- `score.py` was not changed; it still measures decision, recall,
  condition count and schema only. Attribution and condition shape are
  measured in the `analysis/` category tables, not in its output.
- The overfitting signal (three iterations that each fix one case while
  another breaks) did not occur; the one reverted iteration failed on
  request size, not on a decision.

### Files changed

- `prompt.txt`: version 41 (1,600 words) replaced by version 42 (298 words)
  built on the skeleton; original retained in `runs/00-baseline-retained/`.
- `draft_stage.py`: added `retrieve()`, inline fact labels in
  `build_request()`, `exemplars_for()`, and `retrieval_added` in the output
  record; docstring notes what the stage now does. The double is untouched.
- `README.md`: two table rows refreshed to point at the retained runs.
- New: `NOTES.md`, `analysis/iteration-*.json` (seven error tables),
  `runs/00..07` (outputs and prompt of every measured run), `outputs/`
  overwritten by the final run.
