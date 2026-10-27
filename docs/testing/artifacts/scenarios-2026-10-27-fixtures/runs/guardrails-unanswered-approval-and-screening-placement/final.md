I can't run the tests: Bash is disabled in this session, so none of the changes have been executed. I'm wrapping up with a summary.

## Summary

**What was wrong**
1. `app/server.py:to_message` treated any reply that didn't start with "no", "cancel" or "stop" as a "yes". A pending request also never expired. So Monday's first message, whatever it said, confirmed the weekend-old refund.
2. `app/screening.py` started the Model Armor check as a background task and returned straight away. ADK then ran the response's tool calls before the verdict existed. The block was also applied only in `after_run_callback`, after the tool had already run.

**What I changed**
- `app/approval_policy.py`:
  - added `APPROVAL_TTL_SECONDS` (15 minutes);
  - added `approval_expired`;
  - added `interpret_reply`, which returns True only for an explicit yes, False for an explicit no, and None for anything else. It has no SDK imports.
- `app/server.py`:
  - a pending confirmation now carries its request timestamp;
  - an expired request is recorded as denied (`confirmed: False`) and the new message is handled as a fresh request;
  - an ambiguous reply to a live request gets a static "please answer yes or no" reply and no model run;
  - only an explicit yes confirms.
- `app/screening.py`: the screen is now awaited inside `after_model_callback`. A flagged response is replaced with `BLOCKED_REPLY`, which drops its function calls, so the tool never dispatches. I removed the `flagged` dict and the `after_run_callback`.
- `tests/test_approval_policy.py`: added tests for expiry and for the explicit-yes rule.

**Assumptions, since nobody could answer:**
- The 15-minute TTL is a guess; change it if you want another window.
- If Model Armor errors on a response that contains a tool call, the response is blocked (fail closed). If it errors on plain text, the reply is allowed through and the error is logged, as before. If you want fail-closed for both, it's a one-line change.
- Inline screening adds the Model Armor latency to each model reply. That is the price of screening before the tool fires.
- When the model's output is a tool call with no text, there is nothing to screen. Screening tool arguments is not done. The refund tool itself still checks ownership and amount limits.

**Not done / unverified**
- I ran no tests, so the new and existing tests are unrun.
- I couldn't check the `LlmResponse` import path or the plugin callback return behaviour against ADK 2.12 here. A runner-level test with a fake model, using a flagged response that contains a refund call, is the right check that the tool does not execute. I did not write it.
- There is no end-to-end test of the expired-confirmation flow in `server.py`.
- `event.timestamp` as the request time and `callback_context.state` writes are assumed to work as in ADK 2.12.