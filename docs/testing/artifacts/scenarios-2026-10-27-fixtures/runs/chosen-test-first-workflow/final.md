I fixed the duplicate refund and added two tests for it, but I couldn't run any tests. The shell tool is disabled in this session, so nothing has been run, including the new tests.

**Cause:** `RefundAdapter.refund` in `app/refund_adapter.py` sent a different replay key on every attempt (`{operation_id}-{attempt}`). If the provider accepted a refund and the response timed out, the retry used a new key. The provider saw a new request and refunded again.

**Tests added** in `tests/test_refund_adapter.py`:
- `test_timeout_after_acceptance_does_not_refund_twice` uses the `timeout_after_accept` double. It expects one provider refund, `re_0001` returned, `ok=True`, no error, and the operation recorded as succeeded.
- `test_every_attempt_reuses_the_same_replay_key` expects all three requests in a 503, timeout, ok sequence to carry one key.

I traced the first test by hand against the old code instead of running it. The retry creates a second refund, `re_0002`, so it should fail before the fix.

**Fix:** the adapter now uses `operation_id` as the replay key for every attempt. After a timeout, the retry gets the provider's `200 replayed` response with the original refund. The adapter then returns the same `RefundResult(True, original_id)` as before.

**Assumptions and gaps:**
- **Skill:** no test-first skill is installed. Only `adk-engineer` and `safe-api-tool-calls` are, so I followed test-first manually: tests, then fix.
- **Key length:** operation IDs are `op_` plus 16 hex characters, well inside the provider's 64-character limit.
- **Old in-flight operations:** an operation still pending from before this change may already have a refund accepted under an old `…-N` key. A retry now uses a new key and could duplicate it. I didn't add a lookup for those keys. If such operations exist, a one-time check with `client.find_refund` over the old keys would cover them. Do you have any?
- **Left undone:** run `python -m unittest discover -s tests -t .` to confirm.