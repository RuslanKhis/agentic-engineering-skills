ADK resume is enough for now: the double refund came from a bug in our payments client, not from resume. I haven't run any of the tests, because this session has no shell tool. The new test is written but unverified, and I never ran it against the old code either, so the claim that it fails on the old uuid4 key is from reading the code.

**Why resume is enough.** `PaymentsClient.create_refund` sent a fresh `uuid4()` as the `Idempotency-Key` on every call, so the provider couldn't tell the replay from a new refund. ADK documents resume as running tools at least once, so the tool running a second time after the pod eviction was expected. Waiting days is fine, since a paused session sits in Postgres rather than in a process. A durable engine wouldn't fix this alone either, because a crash after the provider accepts but before the engine checkpoints would still re-run the step.

**What I changed:**
- `app/tools/refunds.py` now builds the key from the user, the function call ID, the order and the amount. The call ID is stable across resume and across a second approval of the same paused call. The tool refuses to run if there is no call ID. The local refund ID comes from the same hash.
- `app/clients/payments.py`: `create_refund` takes the key as a required argument.
- `app/store.py`: `record_refund` uses `INSERT OR IGNORE`, so a replay writes one row.
- `tests/fakes.py`: a provider double that returns the original refund for a repeated key, and a default `function_call_id` on `FakeToolContext`.
- `tests/test_refund_resume.py` is the test that proves the choice. It simulates a crash after the provider accepts, then replays the tool. It expects two provider requests, one provider refund and one local row. It also covers a plain replay, a different call ID, a missing call ID, and a control showing the double detects fresh keys.
- `docs/decisions/refund-resume-vs-engine.md` records the decision and when to revisit it. DBOS is the first choice, since it needs only Postgres. Revisit if nothing can re-invoke after a crash, if waits need timers or expiry, or if more side-effecting steps follow the refund.

**Questions I couldn't ask, and what I assumed:**
- I assumed `function_call_id` is identical on resume in real ADK, as documented. I couldn't verify it because the SDK isn't installed and there's no network. This is the main thing to check.
- I assumed the provider accepts the same key with the same body. The "same key, changed body" case is not modelled.

**Left undone:**
- Run `python -m unittest discover -s tests -t .`.
- `app/approvals.py` still lets a manager approve the same call twice. The back office should store the decision and refuse a second answer for the same call ID. The key now makes a second approval harmless, but the stale "pending" display is still a bug.
- The provider keeps keys for 7 days, so an approval later than that after the first attempt could pay again.
- No end-to-end test through the real `Runner` with an evicted worker.