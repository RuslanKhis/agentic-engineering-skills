Both fixes are written, but none of it has been run. Bash is disabled in this session, so I couldn't run the unit tests or import the code.

**Questions I couldn't ask, and what I assumed**
- **Confirmation lifetime:** I assumed 15 minutes (`CONFIRMATION_TTL_SECONDS` in `app/approval_policy.py`). Please confirm or change it.
- **What counts as approval:** I assumed only a clear "yes" (or similar) approves, and "no", "cancel" or "stop" declines. Everything else is treated as unclear.
- **Screening:** I assumed a short added delay on replies is acceptable, since the screen now has to finish before the reply goes out. I also assumed that if Model Armor errors, the reply is withheld rather than let through.

**1. Weekend refund (`app/server.py`, `app/approval_policy.py`)**
- **Cause:** `to_message` treated any message as "yes" unless it started with no/cancel/stop. Monday's "any news about my parcel?" therefore approved the refund. Nothing about the request's age was checked.
- **Fix:** the chat endpoint now handles a pending confirmation in four ways:
  - **Clear yes within 15 minutes:** the refund is approved.
  - **Clear no within 15 minutes:** the refund is declined.
  - **Anything else within 15 minutes:** the endpoint replies with a fixed prompt to answer yes or cancel. No model call is made, no tool runs, and the request stays pending.
  - **Older than 15 minutes:** the endpoint sends a decline to the model first. Your new message then runs as a normal fresh request, so even a late "yes" cannot approve it. This costs one extra model call.

**2. Output screen running in parallel (`app/screening.py`)**
- **Cause:** `OutputScreenPlugin` screened in a background task. The tool call had already fired by the time the verdict came back. That is the 14 October `send_email` case.
- **Fix:** the screen now runs inside `after_model_callback` and waits for the verdict. I believe ADK only dispatches a response's tool calls after that callback returns, but I haven't confirmed that against the installed SDK.
- **Flagged or failed screen:** the whole response is replaced with the fixed blocked message, so its tool calls never run.
- **What gets screened:** the screen now also covers the tool-call arguments, not just the text.

**Tests added**
- `tests/test_approval_policy.py` has new cases, including the Monday "any news about my parcel?" message and a weekend-long gap.
- `tests/test_screening.py` is new. It covers a flagged response, an unavailable screen, a clean response and screened arguments. It skips itself if `google-adk` isn't installed.

**Not done**
- **Test run:** run `python -m unittest discover -s tests -t .` yourself.
- **Runner test:** there is no test through a real ADK runner with a scripted model, which would prove a flagged response leaves zero tool dispatches and that a declined or expired confirmation leaves zero provider calls. The `/api/chat` flow in `server.py` is untested.
- **SDK versions:** I didn't check the installed ADK 2.12 against these APIs, including `LlmResponse` and `event.timestamp`.
- **Incident doc:** `docs/incidents/2026-10-20-weekend-refund.md` still says "No root cause written yet". I left it for Priya to fill in.