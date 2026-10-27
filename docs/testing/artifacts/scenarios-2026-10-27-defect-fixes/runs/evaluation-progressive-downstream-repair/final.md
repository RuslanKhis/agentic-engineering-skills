I can't run the tests in this session. It has no shell tool, so the fix and the new tests are unexecuted.

## What I found
- **Cause:** the export step is the failing part. `accept_review` in `pipeline/review_consumer.py` required every span the review cited to appear in the draft's top-level `citations`. That list holds only the two quoted spans. The reviewer correctly checked the spans each reason cites, so it listed `HWY@1:p1:1` and `LP-T2@2024:p44:4-6`, and export rejected them.
- **Not the cause:** the writer and review outputs are fine. The review's spans for R1 and R2 exactly match what each reason cites, the span line numbers resolve correctly against the sources, and the review covers every reason.

## What I changed
- **Consumer fix:** `pipeline/review_consumer.py` now checks each claim's spans against the citations of that claim's own reason. A span cited only by a different reason is still rejected, and so is one that is merely quoted.
- **Tests:** `tests/test_review_consumer.py` has two negative tests for those cases and one test that reads the saved r1 `writer.json` and `review.json`, read-only, and expects acceptance.
- **Left alone:** `runs/`, the ledger, the pins, and `pipeline/adk_app.py`. I made no provider calls.

## Smallest next run
- **Zero-send export replay:** the saved r1 writer and review are still valid, because the draft, source, prompts and schemas are unchanged. Run `export` only, from those checkpoints, into a new linked run directory such as `PA-2026-0158-r2`, which records "export continuation of r1". This costs $0 and needs no model send.
- **The AP-3 review continuation:** I'd leave it unspent unless you want a fresh review. The fix makes it unnecessary for the diagnostic.
- **Fresh cases:** after that passes, run `cases/fresh/PA-2026-0190` and `PA-2026-0193` through the normal route. They fall under AP-3 (ceiling $3.00 total, $0.80 per case) and need your go-ahead per run.
- **Missing runner:** I didn't write an export-only replay entry point, since a new run directory is a write and I couldn't test it. You'll need that small script, or an approved way to do it.

## Check before release
1. Run `python -m unittest discover -s tests -t .` and confirm it passes. This is not yet done.
2. R2's review claim cites only `APP-FORM@1:p1:4`. The draft's R2 also cites `APP-FORM@1:p1:2` and the Table T2.1 line, which the review never checked. The review passed it as supported, so someone should confirm that is acceptable.
3. R1 and R2 cite spans with no quote in the draft. The draft's only quotes are for `HWY@1:p1:2` and `APP-FORM@1:p1:4`. Decide whether unquoted citations are acceptable.
4. Cohort A passes only if the export is produced and the decision matches the officer's label. PA-2026-0141 and the other dev cases haven't been re-run against this consumer change.
5. Release needs every cohort case passing on one frozen snapshot, plus the full regression suite.

## Questions I couldn't ask
- **Is per-reason citation the intended grounding rule?** I assumed it is.
- **Should the export-only replay count as the "diagnostic continuation" under AP-3?** I assumed it does not use up that approval.