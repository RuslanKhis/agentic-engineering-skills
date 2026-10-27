I changed the widget pipeline to stage-then-emit, but I haven't run any tests. This session has no shell tool, so the new tests in `tests/test_shopping.py` are `not run`. I read the code against them by hand. Please run `python -m unittest discover -s tests -t .` before merging. Nothing was checked against the real ADK, which isn't installed here.

**How it works now.** The three tools no longer render. They write a small JSON spec per widget id into `state["staged_widgets"]`. The after-agent callback is the only place that calls `render_ui_widget`, and a test fails if a second call site appears.

- **Duplicate cards:** specs are keyed by widget id, so two tools staging `product-cards` in one turn produce one widget. The last one wins.
- **Refresh that reached the browser as nothing:** the callback now marks each widget as emitted in state. That write is what makes ADK produce an event for a callback. Previously a render-only callback changed no state, so nothing was sent. The currency refresh now re-stages the cards in the new currency and emits them once.
- **"Show me those again" re-running the search:** I added a `show_last_results` tool. It re-stages the cards from the last search without searching, and the prompt tells the model to use it. The existing three tools keep their names and result shapes.

**Files.**
- New: `app/staging.py`.
- Changed: `app/callbacks.py`, `app/tools/shopping.py`, `app/agent.py`, `app/prompts.py`, `tests/test_shopping.py`.
- `app/staging.py` and the tools import no `google.adk` code.
- The tests use fakes only.

**Assumptions** (nobody could be asked):
- **New tool is acceptable:** I read "keep the tools' names" as allowing one extra tool. If not, the alternative is a prompt-only fix, which is less reliable.
- **Order and repeats:** cards are emitted before the table. A repeat "show again" re-sends the same cards even though nothing changed, because that is what the user asked for.
- **Which cards the refresh uses:** the refresh re-renders whatever cards were last staged. That includes `recommend_products` results, not only the last search.

**Left undone.**
- A model-free `InMemoryRunner` test on the pinned ADK, to confirm one event per emit and none when nothing is pending.
- Browser rendering of the widgets.
- Checking the A2UI payloads against the published schema.

I didn't check the instruction's `{user:currency?}` placeholder.