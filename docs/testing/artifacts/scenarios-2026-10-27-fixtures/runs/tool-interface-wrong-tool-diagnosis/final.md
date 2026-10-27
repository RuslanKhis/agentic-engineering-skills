I fixed the two order tools' interface in `app/tools/orders.py`, but I couldn't run the tests or the linter. Bash is disabled in this session, so the changes are untested.

**Diagnosis**
- **Tool choice:** `search_orders` had the docstring "Search orders." and `get_order` had "Get an order." Neither said when to use it or named the alternative. "Search" sounds like the right tool for any lookup, so the model picked it.
- **Names passed as IDs:** the parameters were called `value` and `data`. On ADK 2.8.0 the docstring is the whole description and no per-parameter text reaches the model, so the names were its only hint about what to pass.
- **No way to recover:** `get_order`'s not-found result had no hint on how to find a valid ID.
- **Unfixable by search:** `search_orders` only matches order ID, status and date. It can't find an order by a person's name, so those calls could never have worked.
- **Evidence:** no recorded events exist, so this comes from reading the source. It hasn't been confirmed against real model behaviour.

**Changes**
- `search_orders(value)` is now `search_orders(query)`.
  - Its docstring says to use it only when the customer has no order ID.
  - It points to `get_order` and `list_my_orders` as the alternatives.
  - It says it matches order ID, status or date, and never a person's name.
- `get_order(data)` is now `get_order(order_id)`.
  - Its docstring says to use it whenever an ID like "HO-10442" is given.
  - It says not to guess an ID.
  - It documents the return shape.
- The `get_order` not-found result now includes `"hint": "Call list_my_orders to see this customer's order IDs."`.
- I added two tests in `tests/test_tools.py`: one for the not-found hint, and one for the new parameter names and the cross-references in the docstrings.
- I didn't touch the agent instruction.

**Assumptions**
- Customers give order IDs and statuses, not product names. If you want name search, that's a feature for you to decide on.
- Renaming the parameters is safe because every caller and test passes them positionally. I found no keyword calls in the code I searched.

**Left undone**
- **Tests and linter:** please run `python -m unittest discover -s tests -t .` and `python .claude/skills/adk-tool-interface-design/scripts/lint_tool_schemas.py --project . --max-tools 20`.
- **Declaration dump:** I didn't take a before/after dump of the tool declarations or run a scripted-model test.
- **`search_help`:** it returns a bare string. I left it alone because `test_help_search_returns_text` asserts on the string. Changing it to `{"status", "articles"}` plus a no-match hint is a small follow-up.
- **Other tools:** I only read the order tools. The other ten tools, including whichever other tool has a one-line docstring, haven't been reviewed.
- **Accuracy:** nothing measures tool-selection accuracy on a real model. I'd build a labelled set from prompts like "where's my order HO-10442?" and "show my processing orders" and run it through `adk-agent-evaluation`.