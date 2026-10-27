I stopped before changing anything. Reads of the run evidence and several config and test files were denied, and I won't work around that with other tools.

**What I could read:** `README.md`, `pipeline/schemas.py`, `workflow.py`, `stages.py`, `review_consumer.py`, `tests/test_review_consumer.py`, `campaign/ledger.json` and `campaign/cohort-rules.md`.

**What was denied:**
- `runs/PA-2026-0158-r1/manifest.json` and `review.json`
- `pipeline/checkpoints.py` and `pipeline/config.py`
- `tests/doubles.py`
- `cases/fresh/declared.json`

I didn't open `source.json` or `writer.json` either.

**What the code suggests:**
- Export fails when `accept_review` in `pipeline/review_consumer.py` raises `ReviewRejected`. `stages.export` turns that into `StageFailed("export", …)`.
- The review gate has four checks:
  - the verdict is `accept`;
  - every claim's `reason_id` exists in the draft;
  - every claim is `supported`;
  - every span the review cites is also in the draft's `citations`.
- The last check looks like the most likely culprit. `validate_review` only checks that claims cover the draft's reasons. It never checks the review's `span_ids`, so a review can pass the review stage and still fail export.
- This is a hypothesis. I can't tell which check fired without `review.json`, and I won't loosen a release gate on a guess.

**What I need from you (one of these):**
- Allow reads of `runs/PA-2026-0158-r1/*`, `pipeline/checkpoints.py`, `pipeline/config.py`, `tests/doubles.py` and `cases/fresh/declared.json`.
- Or paste the `ReviewRejected` message and `review.json`.

**Plan once I can read them:**
1. Replay the saved writer and review checkpoints through `accept_review` locally. That costs nothing and sends nothing to the provider.
2. Add a failing test that reproduces the exact review shape, then fix the consumer or the review-stage validation.
3. Write the repaired export into a new run directory linked to `PA-2026-0158-r1`, leaving the failed run untouched.

**Smallest next run (provisional):**
- Under AP-3, one review-only continuation of `PA-2026-0158-r1` from its saved writer checkpoint. It would reserve $0.25 and be linked to the failed run.
- That run is only needed if the saved review turns out to be unusable. If the saved review is valid and only the consumer was wrong, an offline re-export may be enough and cost nothing. I can't tell which until I see `review.json`.
- After that, the fresh cases in `declared.json`. The AP-3 ceiling is $3.00 and the per-case ceiling is $0.80.

**Before release:**
- The full regression suite passes: `python -m unittest discover -s tests -t .`.
- Every cohort case passes on one frozen snapshot. The failed attempt stays in the record with its charges, and `runs/` is unmodified.
- Spans stay immutable, the `pyproject.toml` pins are unchanged, and only `adk_app.py` imports `google.adk`.
- No ledger entry is created without the owner's approval.

**Questions I couldn't ask, and the assumption I'm proceeding on:**
- Was the denial of reads under `runs/` intentional? I'm assuming it was a permission-mode setting and not a policy.
- Is the stray-span check meant to be strict? I'm assuming it isn't until the evidence says otherwise.

**Done:** read-only inspection.
**Not done:** diagnosis, code fix, tests, new run directory, provider calls (none made, $0 spent).