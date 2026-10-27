# Evaluation summary (living)

## 2026-10-27 — error analysis of baseline-2026-10-20 (writer-v12, retrieval k=2)

Source: saved outputs and traces under `runs/baseline-2026-10-20/` against `labels/dev-labels.json`.
No provider calls. Baseline decision agreement: 1/5 (PA-2026-0204 only, and its conditions contradict its reason).

| Case | Label | Baseline | Category | Detail | Stage |
| --- | --- | --- | --- | --- | --- |
| 0201 | refuse | approve | missed_policy | LP-T2-1 not retrieved (LP-T2 was); parking after works (1 space, 4 beds) never weighed; cites only H4 | retrieval |
| 0202 | refuse | approve | missed_policy | LP-ENV3 not retrieved; TPO lime 3.2 m and "no tree survey" ignored | retrieval |
| 0203 | approve | refuse | wrong_attribution | 4.2 m is the height (DWG-05) but cited as depth on DWG-03 (3.8 m); H4 was retrieved | writer |
| 0204 | approve | approve_with_conditions | weak_condition | C1 imposes the 2.4 x 43 m splay that R2 says is waived | writer |
| 0205 | approve_with_conditions | null | contract_failure | "missing gaps", "condition C1 has no reason"; excluded from quality denominator | schema |

Counts: missed_policy 2, wrong_attribution 1, weak_condition 1, contract_failure 1 (excluded).
Retrieval recall of labelled policies: 5/7. Largest category: missed_policy, so retrieval is changed first.

Observation, not acted on: `WRITER_RULES` is ~7,000 words of accumulated, partly contradictory rules
(e.g. "check the heritage statement first" for sources that do not exist in these cases). It is the likely cause
of the 0203/0204 defects and the 0205 contract failure, but it is a second change and is left for the next iteration.

### Iteration 1 — retrieval queries use the application's page text, not the proposal line only
- Change: `pipeline/retrieval.py::queries_for` (k stays 2, scoring unchanged). Prompt, model, schema untouched.
- Offline measure: `python -m evals.retrieval_recall` (also a unit test).
- Expected by hand calculation (NOT executed; no shell was available): recall 7/7. 0201 -> T2, T2-1; 0202 -> ENV3, H4
  (H4 and T2 tie at 2 hits; H4 wins on document order only, a fragile tie); 0203, 0204, 0205 unchanged and correct.
- Decision quality after the change is unmeasured: it needs a writer run on the dev set (owner approval, ledger charge).
