## Summary

**Route chosen:** converters in the gateway, not the model.

`A2UI: server-side converters on validated tool results, protocol v0.9; agent check: app/tools/a2ui.py check_messages (allowlist, root, dangling refs); client check: MessageProcessor with STRICT_VALIDATION plus an explicit allowlist guard; demo surface: our React app.`

I chose this because `search_products` and `compare_products` already return structured data. The model never writes component JSON, so there is nothing for it to get wrong.

**Can you demo it in `adk web`? No.**
- The `adk web` bundled with ADK 2.12.0 only reads A2UI from `<a2ui-json>` text blocks and `a2ui` data parts. It speaks v0.8 with the standard catalogue only.
- Our output is returned beside the reply by `/api/chat`, so it won't appear there.
- `adk web` still shows the conversation and tool calls. The demo surface is the React app.
- This comes from the skill's notes on ADK 2.12.0. Nothing was run here.

**Components outside the catalogue:**
- **Server:** `check_messages` raises `A2uiValidationError` for an unknown component, a missing root or a dangling reference. The gateway logs the failure and sends no widget.
- **Client:** `guardMessages` throws before the processor sees the batch. `ChatPanel` then shows "(The product display could not be shown.)" instead of rendering nothing.
- **Processor:** I passed `STRICT_VALIDATION` to the processor too. In 0.14.0, a processor built with no options tolerates unknown components, which is your current setup.

**Files changed**
- `app/tools/a2ui.py` (new) and `tests/test_a2ui.py` (new)
- `app/server.py`: `/api/chat` now also returns `a2ui`.
- `web/src/a2ui/surface.ts`, `web/src/api.ts`, `web/src/chat/ChatPanel.tsx`

**Evidence: nothing was run.** Bash is disabled in this session, so all of it is unexecuted code.
- `python -m unittest discover -s tests -t .` — `not run`
- `tsc` — `not run`

**Assumptions** (nobody could answer, so I proceeded on these)
- The catalogue is the standard v0.9 basic catalogue; `CATALOG_ID` is my guess at its URL. Please say if you publish your own.
- Prices are in USD, formatted from integer cents.
- The comparison table is built from Rows and Text, since the basic catalogue has no Table component.

**Left undone / unverified**
- The `MessageProcessor` constructor shape in `surface.ts` is a guess marked UNVERIFIED. The explicit guard works regardless. Check it with `tsc` once dependencies are installed.
- Nothing renders the surfaces yet. `@a2ui/react` isn't installed and its registration wasn't reviewed.
- Schema validation against the official v0.9 JSON schemas isn't done. `a2ui-agent-sdk` could serve as a dev-only dependency without touching the A2A pin.
- Client failures aren't reported back to the agent as `VALIDATION_FAILED`. They are only logged and shown to the user.
- No model-free ADK test of the gateway.
- **A2A later:** the gateway-produced `a2ui` field is not part of A2A. A partner that doesn't run ADK would see no cards or table unless you decide to send real A2UI messages as A2A data parts. That is a separate decision.

**Question I'd have asked:** do you want a custom catalogue (branded product card, real table) instead of the basic one? I assumed not.