# optimise-compaction-atomic-groups-three-points: what the fixture holds

Base: support-assistant. Overlay:

- `app/plugins/trimming.py` `trim_contents`: keeps the newest `max_items` contents by count, so the
  cut can fall between a model `function_call` content and its `function_response` content (the
  "function call without its result" rejection; A1 expects call and responses treated as one
  atomic group kept or dropped together, with a test that a trimmed history never carries a call
  without its result or a result without its call).
- `app/plugins/summariser.py`: `before_model_callback` prepends "Earlier in this conversation:
  <digest>" to `system_instruction`, so the static instruction prefix changes on every trimmed
  request (A3: keep the static prefix intact; measure with the retained-history accounting).
- `app/app.py`: `App(..., plugins=[HistorySummariserPlugin(max_items=24)],
  events_compaction_config=EventsCompactionConfig(compaction_interval=6, overlap_size=1))` —
  App-level compaction plus the custom plugin; nothing documents when either runs (A2: name the
  three compaction points — inside the run, before persisting, maintenance over stored history —
  with a budget and a test for each).
- `app/server.py`: `DatabaseSessionService` on PostgreSQL, `Runner(app=support_app, ...)`.
- `tests/test_trimming.py`: passes offline; covers only text turns.
- No model access: A4 expects model-dependent checks reported as not run.

Original context (unchanged): "An ADK 2.12 agent with App-level compaction plus a custom trimming
plugin, a Postgres session store, no model access in the session."
