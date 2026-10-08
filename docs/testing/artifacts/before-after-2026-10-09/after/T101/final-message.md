I fixed T-101 in code and the offline tests pass, but nothing here shows the real model now picks the right tool. That needs a live evaluation run, which wasn't possible in this session.

**Specialist:** `adk-tool-interface-design`, because the ticket is "wrong tool picked, wrong value in an argument", and the routing table sends exactly that case to this skill. I also used `adk-agent-instructions` for one sentence: the billing agent's instruction said "ALWAYS call search_orders first", which forces the bug the ticket describes.

**What changed:**
- **`support_agent/tools.py`:**
  - The two order tools now have clear parameter names: `get_order(data)` became `get_order(order_id)` and `search_orders(value)` became `search_orders(query)`.
  - Their descriptions now say when to use each one and point to the other: if the customer gives an order ID, use `get_order`; if not, use `search_orders`.
  - `get_order` now rejects names and e-mail addresses before calling the orders API. It returns an error telling the model to ask for the ID or use `search_orders`. "Not found" and "service unavailable" also come back as errors with a next step.
- **`support_agent/agent.py`:** the billing agent is told to call `get_order` when it has an ID, and to ask the customer if it doesn't.
- **`support_agent/__init__.py`:** the agent now loads only when first used, so the tool tests run without google-adk installed.
- **Tests:** 12 new offline tests in `tests/test_tools.py`. A new `tests/test_tool_declarations.py` checks what the model is shown, but it skips itself when google-adk is missing.
- **`tickets/T-101.md`:** added an Evidence section.
- **`REPORT.md`:** all seven sections you asked for, including the friction log with file:line pointers.

**Checks:**
- `pytest`: 13 passed, 1 skipped (the declaration test). These ran on Python 3.9, the only interpreter here with httpx and pytest; the project requires 3.11 or later.
- The skill's linter: the two "vague parameter name" findings are gone, the "short description" findings dropped from 5 to 3 (the remaining three are tools this ticket didn't touch), and nothing new appeared.
- **Not run:**
  - the declaration test, because google-adk isn't installed;
  - the check where a fake model calls the tools (not written, since I couldn't build it against the SDK here);
  - the result-size report, because there are no recorded sessions;
  - the real-model check of whether the agent now picks the right tool.

**Main assumptions** (all questions are listed in REPORT.md):
- **Order ID format:** one word of letters, digits, `-` or `_`, 3–64 characters, containing at least one digit. If real IDs can be letters only, `get_order` will wrongly reject them, so this is the first thing to confirm.
- **What `search_orders` searches:** customer name, e-mail address or a description of the purchase.
- **Tool names:** I kept `get_order` and `search_orders` rather than renaming them.

**Friction rating:** 3/5. Picking the specialist was instant and the references had near copy-paste patterns. The main friction:
- The skill's linter also scanned the installed skills folder and stopped partway because of a broken file in one of the skills, so I had to filter its output down to the project.
- Several validation steps assume google-adk, a fake model for tests, and recorded sessions, none of which exist here.

**Next prompt from the skills:** none given. The entry skill says to end with a prompt for the next ticket but supplies no wording. My suggestion: `/adk-engineer Please take ticket tickets/T-102.md and carry it out.`