# frontend-a2ui-route-and-validation-declared: what the fixture holds

Bases: support-assistant, support-web. Overlay:

- `pyproject.toml`: adds `a2a-sdk[http-server]>=1.0,<2` (A4: `a2ui-adk[a2a]` pulls `a2ui-a2a`,
  which pins a2a-sdk below 0.4 — conflicts with this pin; change no pins, install nothing).
- `app/tools/catalog.py` + `help/products.json`: `search_products`, `compare_products` return
  plain dicts; nothing emits A2UI yet (A1: declare one of the three routes — staged
  `render_ui_widget` converters, a2ui-adk `SendA2uiToClientToolset`, AG-UI `generate_a2ui` — and
  where catalogue validation runs on it). `tests/test_catalog.py` passes offline.
- `app/agent.py`, `app/prompts.py`: retail agent with the two catalogue tools.
- `web/package.json`: `@a2ui/web_core` 0.14.0; `web/src/a2ui/surface.ts` constructs
  `new MessageProcessor()` with no options (A2: construct with a `validationConfig` such as
  STRICT_VALIDATION and report VALIDATION_FAILED back; agent-side `validate_payload` is stateless
  per payload).
- A3: `adk web` in google-adk 2.12.0 does not render `actions.render_ui_widgets`; the demo surface
  is the app.

Original context (unchanged): "ADK 2.12.0 project pinning a2a-sdk[http-server]>=1.0,<2; the React
client constructs @a2ui/web_core 0.14.0 MessageProcessor with no options; no a2ui packages
installed; no network."
