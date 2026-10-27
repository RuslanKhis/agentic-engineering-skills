I fixed the hyphen failure in `pipeline/citations.py` and added tests. I couldn't run them, because Bash is disabled in this session, so none of this is verified. Please run `python -m unittest discover -s tests -t .`.

**The fix** is in `quote_matches` (`pipeline/citations.py`):
- The exact check against the spans joined with newlines still runs first.
- If that fails, it tries a second reading where a line-break hyphen is dropped.
- That reading applies only when the first line ends in a letter followed by `-`, and the next span is the very next line of the same document, version and page, starting with a lowercase letter.
- So a quote can't bridge unrelated lines or documents, and numbers, names and span identity are still compared exactly.
- I also made an empty `span_ids` list return False.

**Tests** are in `tests/test_correction_probe.py`:
- One test shows the old failure: the r3 quote isn't a substring of the raw join of `DAS@2:p1:2` and `DAS@2:p1:3`. It then asserts the quote now matches.
- Another checks that the following still fail:
  - a changed number (No. 15 instead of No. 14, 4.0 m instead of 3.0 m);
  - a quote that runs past the end of the source text;
  - the first span alone;
  - a span from a different document.
- I dropped a "non-adjacent lines" assertion because `DAS@2:p1:4` doesn't exist, so it passed for the wrong reason. That case has no real test.

**Questions I couldn't ask, and what I assumed:**
- Is the finding that was "actually right" the R1 citation, the one the quote check rejected? I assumed yes.
- Should the served route copy to bound spans? I did not change `stages.py` or `adk_app.py`, because the request was to fix the check. Binding server-side text via `bind` would remove this failure class entirely and is the better long-term fix.
- I did not use your expected outcomes, since they are unreviewed.

**Left undone:**
- Nothing under `runs/` was edited, and no provider calls were made. r3 still shows as rejected. Re-checking it would need a new run directory, which I didn't create.
- The r3 draft has a separate problem the quote check doesn't catch. R3 says H4 forbids more than 4.0 m "in any circumstances", but the approved paraphrase list only allows "should not project more than 4.0 m" to be restated as "may project up to 4.0 m". R2 also concedes 4.6 m is acceptable. `reason_supported` only trusts the writer's own `support` flag. I did not change it. Making it stricter is a decision for you.