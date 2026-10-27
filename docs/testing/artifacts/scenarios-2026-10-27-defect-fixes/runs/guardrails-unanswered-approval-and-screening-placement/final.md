Both fixes are written, but I haven't run any of it. I had no shell in this session, so none of the new tests have been executed.

**1. Unanswered approval executing on Monday**
- **Cause:** in `app/server.py`, any reply to a pending confirmation that didn't start with "no", "cancel" or "stop" counted as approval. Monday's first message, whatever it said, therefore approved the refund.
- **Fix:** the new `app/confirmation.py` decides what a message means. `app/server.py` calls it.
  - Only an explicit "yes" or "confirm" approves, and only within 15 minutes of the request.
  - A late "yes" rejects the stale request and replies "waited too long, nothing was refunded".
  - Any other message rejects the pending request first, then runs as a normal new message.
  - A clear "no" rejects it.
- **Tests:** `tests/test_confirmation.py` covers each of these cases, including a request that sat for three days.

**2. Output screen running beside the tool call**
- **Fix:** in `app/screening.py`, the Model Armor check now finishes inside `after_model_callback`, before ADK runs any tool in that response. If the response is flagged, it is replaced with the static blocked message, which has no tool call. I removed the background task and the `after_run_callback` that tried to block afterwards.
- **Screen failure:** if the screen itself errors, the response is treated as flagged.
- **Tests:** `tests/test_screening.py` covers flagged, error and clean responses. It skips itself when `google-adk` isn't installed.

**Assumptions and open questions (nobody was available to answer)**
- Is 15 minutes the right expiry? I chose it; it's `CONFIRMATION_TTL_SECONDS`.
- Should a screen outage block replies? I assumed yes. If you'd rather let plain text through, the change is in the `except` branch in `app/screening.py`.
- I treated "sure" and "ok" as not approving, on purpose.

**Left undone**
- Running `python -m unittest discover -s tests -t .`.
- A real-runner test with a fake model.
- Screening is blocking now, so each model reply waits on Model Armor. Its latency is untested.
- Streaming (`partial`) chunks aren't screened. The server uses non-streaming responses today.
- Tool-call arguments with no text alongside aren't screened. The refund confirmation is the only guard on those.
- ADK's docs list `DatabaseSessionService`, which the server uses, as unsupported for in-session confirmation. A multi-day approval should become a durable review record outside the session. That is a larger change, and I didn't make it.
- A duplicate "yes" after approval relies on ADK 2.12 running a confirmed tool once. `issue_refund` has no idempotency key of its own.