I rewrote the declarations of the three weak tools. Tests pass (14, `unittest`), but I haven't tested the model's behaviour. The agent instruction is untouched.

**Diagnosis.** ADK 2.8.0 sends the model only the docstring and the parameter names, and no per-parameter descriptions. `search_orders(value)` and `get_order(data)` each had a one-line docstring ("Search orders." / "Get an order.") and an opaque parameter name. The model had no signal that `get_order` takes an order ID, or that `search_orders` only matches ID, status and date text. So it reached for the "search" tool and passed names. This is inferred from source, because no recorded events exist.

**Changes**
- **`app/tools/orders.py`:**
  - `search_orders(value)` is now `search_orders(query)`. Its docstring says to use it only when there is no order ID, that it matches ID, status or date, and that it does not search by product or customer name. It also gives examples and the return shape.
  - `get_order(data)` is now `get_order(order_id)`. Its docstring says to use it whenever an ID is known and never to pass a name, with the ID format `HO-10518`. `not_found` now returns a `hint` pointing to `list_my_orders`.
- **`app/tools/help.py`:** `search_help` returned a bare string. It now returns `{"status": "ok", "articles": ...}`, or `{"status": "not_found", "hint": ...}` when nothing matches. Its docstring says it is for policy questions, not a customer's own orders.
- **`tests/test_tools.py`:** the help test reads `["articles"]`. Both renamed parameters are only ever called positionally, so nothing else needed changing.

**Questions I couldn't ask, and what I assumed**
- **Name lookup:** should customers be able to find orders by name or product? I assumed no, since the store has no such field. Each docstring now says "do not pass a name".
- **`search_help` return shape:** I assumed any caller outside the repo can handle the new dict. The instruction file doesn't mention the return shape.

**Left undone**
- The skill's linter found nothing because `tools=TOOLS` isn't a list literal. I read the source by hand instead and did not run a before/after declaration dump.
- I didn't add a scripted-model Runner test, which would need the ADK SDK. I also didn't measure selection accuracy on a real model; that needs a case set (e.g. "where's my order from last week", "status of HO-10518") and belongs with `adk-agent-evaluation`.
- Nine other tools have fuller docstrings and were not reviewed in depth.