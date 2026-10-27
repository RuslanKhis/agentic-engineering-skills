# frontend-tool-widgets-staged-emission: what the fixture holds

Base: support-assistant (only for the package shape; the overlay's agent replaces the support
agent). Overlay:

- `app/tools/shopping.py`: three tools (`search_products`, `recommend_products`,
  `compare_products`), each calling `tool_context.render_ui_widget(...)` inline. Both
  `search_products` and `recommend_products` render widget id `product-cards`; ADK's duplicate-id
  check is per call context, so when the model calls both in one turn the cards ship twice (the
  "cards twice" symptom; A2).
- `app/callbacks.py` `refresh_cards_after_preference_change`: an after_agent_callback that calls
  `render_ui_widget` but writes no state and returns None, so no event is produced and the refresh
  reaches the browser as nothing (A2: write the per-widget emitted flag as the state delta). It
  also never records `cards_currency`.
- "Show me those again" has no staged payload to answer from: `last_search` holds only SKUs, so
  the model calls `search_products` again (A3: answer from the staged payload, suppress a
  byte-identical re-render).
- `app/widgets.py`: converters and `to_ui_widget` (lazy SDK import). A1 expects rendering moved
  into one after_agent_callback emitting staged payloads in a declared order, with a test that
  fails on any second `render_ui_widget` call site.
- `tests/test_shopping.py` (passes offline, patches `to_ui_widget`): A4 expects tool names and
  result shapes kept (`{"status", "skus", ...}`), Runner tests written but reported as not run
  without the SDK, no installs.

Original context (unchanged): "An ADK agent whose three tools each call render_ui_widget inline and
an after_agent_callback that renders without writing state. google-adk not installed; no network."
