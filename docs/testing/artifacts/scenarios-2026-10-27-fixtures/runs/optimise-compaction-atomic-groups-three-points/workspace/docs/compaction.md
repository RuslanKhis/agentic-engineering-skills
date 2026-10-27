# When history is shortened

Two mechanisms run, at different points. Facts about ADK come from the skill's
notes on 2.8.0/2.12.0 source; they were not re-verified against an installed
2.12.0 here (the SDK is not installed in this workspace).

| Point | Mechanism | Runs when | Stored history |
| --- | --- | --- | --- |
| Inside a run, before each model call | `HistorySummariserPlugin` (`app/plugins/summariser.py`) | Every model call where the request holds more than `max_items` (24) contents | Untouched; only the outgoing request is cut |
| After an invocation | `EventsCompactionConfig(compaction_interval=6, overlap_size=1)` in `app/app.py` | Once 6 new invocations have accumulated since the last compaction end; the window includes 1 earlier invocation | A summary event is appended; raw events stay in Postgres |

Notes:

- Only the sliding-window pair is set, so there is no token trigger. Compaction
  is by invocation count, not request size; a few huge tool results can bloat
  requests long before invocation 6.
- No `summarizer` is set, so ADK uses the root agent's model. Each compaction
  is therefore a model call after the invocation.
- Both travel on the `App`; `app/server.py` builds `Runner(app=support_app)`, so
  both are wired.
- The plugin's cut is a turn start (a user content without a
  `function_response`). `max_items` is a minimum: the plugin may keep more, never
  splits a call from its result, and sends the current turn even if it alone
  exceeds the budget.
- The plugin's digest uses text parts only, truncated to 600 characters.

## To confirm on the real stack (not run here)

1. Log compaction: run a session through `DatabaseSessionService` on Postgres
   with a small interval and list stored events whose `actions.compaction` is
   set (known crash report on database sessions, adk-python #3530).
2. Capture the outgoing request with a `before_model_callback` double and
   assert no request has an unmatched call or response.
3. An orphaned `function_call` in storage can disable compaction on some
   versions (#7236); 2.12.0 reportedly fixes it. Verify on the pin.
