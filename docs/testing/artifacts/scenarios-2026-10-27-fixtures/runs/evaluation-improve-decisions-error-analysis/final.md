I made one change, to retrieval, and nothing was run, so the change is untested. This session had no shell, so I couldn't run the tests or the new recall script. The recall figures below are my own hand calculation.

**Error analysis of the baseline** (read against the officer's labels; the full table is in `evals/summary.md`):

| Category | Cases | What happened |
|---|---|---|
| missed_policy | 0201, 0202 | Retrieval searched only the one-line proposal. It never fetched `LP-T2-1` for 0201 or `LP-ENV3` for 0202, so the writer approved both, and the labels say refuse. |
| wrong_attribution | 0203 | The writer read the 4.2 m **height** on drawing 05 as the **depth** on drawing 03 (3.8 m) and refused. |
| weak_condition | 0204 | Condition C1 imposes the visibility splay that reason R2 says is waived. |
| contract_failure | 0205 | The draft failed validation ("missing gaps", "condition C1 has no reason"). I left it out of the quality count. |

The baseline agreed with the labels on 1 of 5 decisions, and that one (0204) is only partly right. Retrieval found 5 of the 7 labelled policies.

**The change:** `queries_for` in `pipeline/retrieval.py` now searches the application's page text as well as the proposal line. The prompt, model, schema and k (still 2) are untouched. By my hand calculation, recall rises from 5/7 to 7/7 on the dev cases and the other three cases keep their policies. For 0202, `LP-H4` beats `LP-T2` only on document order after a tie, so that result is fragile.

**Added:**
- `evals/retrieval_recall.py`, an offline recall check against the labels.
- A unit test in `tests/test_pipeline.py` that fails if any labelled policy is missed.
- `evals/summary.md`, the analysis and iteration log.

**Left undone:**
- **Decision quality is unmeasured.** A retrieval fix can't change what the writer decides without a model run. That needs the owner's approval and a charge to the ledger, which I didn't touch.
- **The writer prompt is the likely cause of 0203, 0204 and 0205.** `WRITER_RULES` is about 7,000 words of rules that partly contradict each other. Rewriting it is the next iteration. I held it back because the loop allows one change at a time.
- **Questions, with the assumption I carried on with:**
  - Do you want recall judged on the labelled policies only? I assumed yes.
  - May I spend on a dev-set writer run? I assumed no.
- I didn't open the holdout cases, `runs/` is unmodified, and no dependencies changed.