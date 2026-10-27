**Decision:** keep ADK resume for the multi-day wait. You don't need a durable engine yet, but the refund write has to be safe to replay.

The long wait wasn't the cause of the double refund. The paused session sits in Postgres and survives days. The cause was `PaymentsClient` sending a fresh `uuid4()` as the `Idempotency-Key` on every call. When the pod was evicted, the resumed tool ran again with a new key. The provider's de-duplication never applied. Temporal activities are at-least-once too, so an engine would need the same stable key.

**What I changed**
- `app/tools/refunds.py`: the key is now a hash of user, order, amount and the tool call's `function_call_id`.
  - The local `refund_id` comes from the same hash.
  - A replay of an already-recorded refund returns the existing result.
  - With no call id, nothing is paid.
- `app/clients/payments.py`: `create_refund` takes the key from the caller.
- `app/store.py`: added `get_refund`, and `record_refund` now ignores duplicates.
- `tests/fakes.py`: `FakeToolContext` gained an optional `function_call_id`.
- `tests/test_refund_resume.py` (new): a provider fake that de-duplicates on the key, and four tests.
  - A second approval of the same call pays once.
  - A crash after the provider accepts but before the local record is written pays once, and both provider calls carry the same key.
  - A separate request creates a separate refund.
  - A missing call id sends nothing to the provider.
- `docs/decisions/refund-resume-vs-durable-engine.md`: the decision, the triggers for revisiting it, and my assumptions.

**What I left undone**
- **Tests not run.** I had no shell in this session, so I haven't run the new tests or the existing suite. Run `python -m unittest discover -s tests -t .`.
- **Existing tests unchecked.** `tests/test_tools.py` and `app/services.py` were denied on read, so I didn't check whether existing tests call `create_refund` directly. That signature changed.
- **ADK assumption unverified.** I assumed ADK 2.12 re-runs the tool on resume with the same `function_call_id`. I couldn't check that without the SDK, so confirm it with a real resume before relying on it.
- **`app/approvals.py` unchanged.** It should reject a second approval for a confirmation that is no longer pending, and I didn't add that.
- **Provider key window.** The provider's key window is 7 days. A crash that falls between the provider call and the local record, followed by a resume more than 7 days later, is not covered.
- **Open questions** (written down because nobody could answer them):
  - Should the back office show an "approved, processing" state?
  - Is the 7-day window measured from the first use of a key?

Revisit the durable engine if the flow adds ordered or compensated side effects, needs timers or escalation, or the provider drops idempotency keys.