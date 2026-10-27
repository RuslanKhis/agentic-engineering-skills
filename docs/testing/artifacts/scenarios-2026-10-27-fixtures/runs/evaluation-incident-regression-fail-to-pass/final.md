I've written the regression tests and a case record, but I haven't run anything. This session has no shell, so no test has executed and the case is unvalidated.

## What I added
- **Tool-level test:** `test_second_issue_after_one_proposal_does_not_refund_twice` in `tests/test_tools.py`. After one proposal, the first `issue_refund` returns `refunded` and the second returns `nothing_pending`. Exactly one payments request and one stored refund result.
- **Runner-level test:** `test_second_yes_does_not_refund_twice` in `tests/test_runner_refunds.py`. A scripted model gets the same refund request and then two "yes" turns, and it calls `issue_refund` on both. It asserts one payments request, one stored refund and that every scripted step was consumed.
- **Do-nothing control:** `test_do_nothing_control_fails_the_double_yes_assertions`. A model that only replies with text must fail the one-refund assertions, so the case can't pass without a refund happening.
- **Case record:** `tests/regressions/double_yes_refund.json` holds the two lists below and the control. The base and fix commits are marked `UNKNOWN` and the validation status is `unvalidated`.

## When the case counts as passing
Run `python -m unittest discover -s tests -t .` on an environment with `google-adk` installed.

- **`fail_to_pass`:** the two double-yes tests above. It must be non-empty. Each test must pass, and a skip counts as a failure. The Runner test skips without ADK, so a run without ADK does not pass.
- **`pass_to_pass`:** the four other refund tool tests and the two existing Runner tests (eligible refund, foreign-order denial). Any failure or error fails the case. A skip leaves it NOT RUN, not resolved.
- **The control test must also pass.**
- **No partial credit.**

Before CI treats the case as accepted, two runs must be recorded:
1. On the base commit, both `fail_to_pass` tests must fail and all of `pass_to_pass` must pass.
2. With the merged fix, every test in both lists must pass.

A test that already passes on the base proves nothing about the fix. If the fix fails any `pass_to_pass` test, it is not the reference fix, and the failing test stays red in CI.

## Questions I couldn't ask, and the assumptions I used
- **Base and fix commits:** the workspace has no git metadata. I left both `UNKNOWN`, so I could not run the base and fix checks above.
- **What "yes twice" means:** I assumed two separate turns, with the model calling `issue_refund` on each. I did not test two calls in one turn.
- **The fix:** I assumed it is the line in `app/tools/refunds.py` that clears `pending_refund` before the payment call. That line is in the current code, but I couldn't confirm it is the merged change.

## Left undone
- Running the tests, so no results exist for any of them.
- Whether the new tests fail on the base commit. Please run that before merging.
- Filling in the commit IDs and ticket reference in the case record.
- Wiring the case into CI. The workspace has no CI config, so I left that to you.

One thing I noticed in the code: `issue_refund` clears the pending refund before calling the provider. If the provider rejects the refund, the customer must start the refund again. That may be acceptable, but I didn't test or change it.