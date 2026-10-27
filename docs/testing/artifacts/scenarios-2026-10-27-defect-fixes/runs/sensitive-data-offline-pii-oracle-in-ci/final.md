I added the offline leak check, but I haven't run any of it. This session had no shell tool, so there are no pass or fail results (`offline`/`not run`).

**It can't replace the SDP tests.** It's a second layer that doesn't need cloud credentials. They check different things:
- **What the check does:** it catches data that reaches model requests, session events and state, logs or tool calls. It matches the canaries, our credential formats (`hpk_`, `hmr-`, JWTs) and email, Luhn-valid card and E.164-style phone shapes. It doesn't use the fakes to decide what counts as a leak.
- **Why it can't stand in for SDP:** `FakeDlp` redacts only the known canaries, so it never exercises the real SDP template, its infoTypes, likelihood thresholds or de-identification transformations.
- **What stays in a separate layer:** it also can't prove Model Armor's template behaviour, or catch names, addresses, free-text identifiers and re-encoded values. Template and detector coverage still needs a scheduled or pre-release run against real SDP and Model Armor with credentials. That run was not set up here.

**Files:**
- `tests/runner/leak_guard.py` is the detector and a `LeakGuard` that collects every sink. It needs no ADK. Findings print masked, never the leaked value. Authorization headers on provider calls are exempt, and email and phone shapes are skipped on provider calls, where a recipient address is legitimate.
- `tests/test_leak_guard.py` tests the detector without ADK. It checks it flags leaks and stays quiet on order IDs, UUIDs and timestamps.
- `tests/runner/test_conversations.py` now scans every Runner test at cleanup and fails it if anything leaked. It also reads the session back from the session service. I changed the refund test to use clean user text, because the card number now belongs in the new test below.

**A likely real gap I found by reading `app/callbacks.py`:** `screen_input` passes an allowed message on unchanged, and only replies are de-identified. A card number typed by a customer therefore probably reaches the model request and the stored user event. I recorded it as an `expectedFailure` test, `test_card_typed_by_customer_reaches_no_sink`, so the build stays green now and goes red once someone fixes the gap and the test needs its marker removed. I haven't confirmed this. If the production Model Armor template blocks cards, `FakeArmor` doesn't model that.

**Assumptions I proceeded on, since nobody could answer:**
- Should a card in the customer's own message be kept out of the model request? I assumed yes.
- Is `example.test` email data a leak? I treated every email as one, since app code and fixtures contain none.
- Log capture runs at DEBUG on the root logger, so ADK's own debug logging is scanned. If ADK logs the raw model response before `deidentify_reply` runs, the first Runner test may fail. That would be a real finding, not a false alarm.

**Not done:**
- I haven't run `python -m unittest discover -s tests -t .`. Please run it in CI first. Besides the open questions above, the first run may need small fixes to the new code, such as the `model_dump_json` serialization.
- I didn't change app code to fix the card gap.
- I didn't add a check that new Runner test classes use the guard.