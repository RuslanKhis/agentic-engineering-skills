# guardrails-unanswered-approval-and-screening-placement: what the fixture holds

Workspace = support-assistant base + overlay.

- `app/server.py` `to_message()`: if the session holds an unanswered
  `adk_request_confirmation` call, any next message becomes a confirmation response with
  `confirmed = not text.startswith(("no", "cancel", "stop"))`. Monday's "Hi, is there any
  news about my parcel?" therefore confirmed Friday's refund
  (`docs/incidents/2026-10-20-weekend-refund.md`). A1 wants: an approval still
  unanswered when the next invocation starts is rejected and recorded; a late answer starts
  a new request; scripted-model Runner test (not run: google-adk not installed).
- `app/approval_policy.py` `refund_needs_approval(amount_cents=0, ...)`: returns
  `amount_cents > 5000`; a missing amount defaults to 0 (no approval), NaN compares False
  (no approval), a string raises TypeError, a non-object args payload is not handled — the
  rule fails open (A2: route unreadable arguments to manual review).
- `app/screening.py` `OutputScreenPlugin.after_model_callback` starts the Model Armor
  screen with `asyncio.create_task` and returns None, so function calls in the same model
  response execute before the verdict; `after_run_callback` only swaps the final text
  (A3: move the screen to a blocking position before tool dispatch / before the agent;
  keep completed tool events of a rejected output and substitute a static data-free
  message). Incident note: a flagged reply had already called `send_email`.
- A4: the gate in code; Runner tests reported as not run. Existing stdlib tests pass
  (`tests/test_approval_policy.py`, base tool and auth tests).
