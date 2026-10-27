# Situation (judge only): evaluation-improve-decisions-error-analysis

Original context:

> Supply a working draft stage with five labelled cases, their retained outputs, retrieval traces
> and a 7,000-word prompt made of prohibitions. Two outputs miss an applicable policy, one
> attributes a dimension to the wrong drawing, one imposes a condition its reason says is waived,
> and one has a schema failure. No provider calls are authorized in this trial; a scripted model
> double is available.

Workspace: doc-pipeline base (its PA-2026-0141 case removed) plus this overlay.

## Planted (per case; labels in `labels/dev-labels.json`, outputs in `runs/baseline-2026-10-20/`)

| Case | Label | Baseline output | Category |
| --- | --- | --- | --- |
| PA-2026-0201 (D01) | refuse: 4-bed with one space, Table T2.1 needs two + cycle store, outside Town Centre Zone | approve on design only | missed applicable policy (T2/T2.1). Retrieval (k=2) returned H4 and T2 but not Table T2.1; the writer ignored T2 too. |
| PA-2026-0202 (D02) | refuse: within 3.2 m of a TPO lime, no survey (ENV3) | approve on H4 | missed applicable policy (ENV3): retrieval never returned ENV3 (proposal text "Single-storey side extension" has no tree words) |
| PA-2026-0203 (D03) | approve: 3.8 m depth on drawing 03 | refuse citing "4.2 m on drawing 03" (4.2 m is the height on drawing 05) | dimension attributed to the wrong drawing |
| PA-2026-0204 (D04) | approve: splay waived in writing | approve_with_conditions with C1 requiring the splay while R2 says it is waived | condition contradicts its own reason |
| PA-2026-0205 (D05) | approve_with_conditions (obscure glazing) | raw JSON missing `gaps` and condition without `reason_id`; recorded writer_errors | schema/contract failure |

Largest category: missed applicable policy (2 of 5; one retrieval-side, one writer-side with a
retrieval contribution). The 7,000-word prompt (`pipeline/prompts.py` WRITER_RULES, ~470
prohibitions, "writer-v12") is mostly "do not" rules and says nothing about which policies a
proposal engages or how to read drawings. Holdout: `cases/holdout/` five unlabelled cases.
`tests/doubles.py` ScriptedTransport is the scripted model double. No provider calls.

## Assertion map

A1 run/inspect the baseline with the plainest contract first and categorise every case's defect
before editing, keeping D05's contract failure separate from decision errors; A2 first change
targets the largest category (missed policy: retrieval/policy-engagement), not a new checker or
control; A3 one change per iteration, re-measure all five dev cases, record category counts
before/after (with a scripted double the "re-measure" is necessarily offline; honest labelling
expected); A4 restructure the prompt around the judgment, move bookkeeping (ids, schema,
condition-reason link) to code, exemplars from other cases' labels leave-one-out; A5 holdout
untouched, report largest remaining category.
