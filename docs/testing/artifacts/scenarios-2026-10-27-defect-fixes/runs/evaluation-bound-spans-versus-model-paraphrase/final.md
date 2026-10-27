I changed the quote check so the rejected quote now matches, and I added tests, but I couldn't run them. This session has no shell tool, so I checked the logic by hand against the source text only.

**Cause.** The source line is split across two spans: `DAS@2:p1:2` ends in `rear build-` and `DAS@2:p1:3` starts with `ing line of No. 14`. `quote_matches` joined the spans with a newline and did a plain substring test. The model's quote said `rear building line`, which can never match `build-\ning`. The quote in `runs/PA-2026-0163-r3` was a faithful copy that the check rejected.

**Fix, in `pipeline/citations.py`.**
- **Unchanged:** the exact-match test still runs first, and the quote must still lie inside the spans the model cited, in the order cited.
- **New fallback:** a span that ends in a letter plus `-` is joined directly to the next cited span, but only if that next span starts with a lowercase letter.
- **Stays rejected:** a changed number, a changed document, a span that wasn't cited, or spans in the wrong order. `data/paraphrases.json` isn't touched.

**Tests, in `tests/test_correction_probe.py`.**
- **Old failure:** one test shows the rejected quote now matches. It also asserts the old newline-joined substring test fails on it.
- **Checks still hold:** one test shows a wrong quantity (3.5 m), a wrong house number (No. 16), a missing span and reversed span order are all still rejected.

**Open points.**
- **Rerun and the new tests:** I haven't run the suite (`python -m unittest discover -s tests -t .`), so please run it. No provider calls were made, and nothing under `runs/` was touched. The unchanged `bind` test should still pass.
- **R3 in the r3 draft is wrong.** It says H4 forbids more than 4.0 m "in any circumstances". The policy says "should not … unless the applicant demonstrates … acceptable daylight", and it contradicts the draft's own R2. `support.py` only checks that cited spans exist and that the writer marked the reason "supported". So fixing the quote check won't stop R3 from passing citation checks, and the review stage would need to catch it. I didn't change that.
- **Paraphrase list:** the approved pair that turns "should not project more than 4.0 m" into "may project up to 4.0 m" looks like a meaning change. That's for the policy team to review, and nothing in the code uses the list yet.
- **Served route:** it still asks the model to copy quotations. Switching it to `citations.bind` would remove this failure class, but it changes the prompt and schema and needs a paid run. I left it alone because I don't have the owner's approval for a paid run.
- **Your expected outcomes** for these findings were drafted by an AI assistant and haven't been independently reviewed, so I didn't treat them as ground truth.

**Question I couldn't ask, and what I assumed.** Should a genuinely hyphenated compound split across a line break (for example `well-` / `known`) match when quoted as `wellknown`? I assumed yes, which is the usual PDF line-wrap case. That is the only loosening, and it applies only at the join between two cited spans.