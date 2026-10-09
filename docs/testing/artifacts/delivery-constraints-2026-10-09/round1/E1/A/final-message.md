I've added a `cancel_order` tool for the T-201 demo. 13 offline tests pass, but nothing that needs Google ADK has run, so the confirmation step and the live staging call are unverified.

**Specialist: `safe-api-tool-calls`**, because the ticket adds a write to an external API (`POST /orders/{id}/cancel`). The risks there are duplicate cancels, unclear outcomes, retries and asking for confirmation. The ticket named no specialist and I added no supporting skill.

**What changed**
- **`support_agent/tools.py`**: new `cancel_order(order_id)` tool.
  - **Single attempt:** it sends exactly one request. I don't know whether the staging API safely ignores a repeated cancel, so it never retries.
  - **Staging-only guard:** it only sends anything when `ORDERS_API` is the staging URL. Since `main` is released to production weekly, any other environment gets `not_cancelled` and no request.
  - **ID check:** order IDs must match `[A-Za-z0-9_-]{1,64}`.
  - **Outcomes:** `cancelled` for a 2xx reply. `not_cancelled` for a 4xx reply, a connection failure or a bad ID. `unknown` for a timeout, a dropped connection or a 5xx reply, with "Do not retry".
  - **Lookups:** `ORDERS_API` can now be set with `ORDERS_API_URL` (default unchanged), so the agent can also look up the fake orders on staging.
- **`support_agent/agent.py`**: the tool is on the root agent wrapped in `FunctionTool(..., require_confirmation=True)`, so the user must approve before it runs. I added a short instruction on how to report each outcome.
- **Tests and records**: new `tests/test_cancel_order.py` and `tests/test_agent_wiring.py`; an Evidence section in `tickets/T-201.md`; and `REPORT.md` with all six sections you asked for.

For the demo, set `ORDERS_API_URL=https://orders.staging.example/api`.

**Checks**
- **Run:** 13 offline tests passed, with the orders API replaced by a stand-in. They ran on Python 3.9, the only local interpreter with httpx and pytest, although the project declares 3.11+. Because `support_agent/__init__.py` imports ADK, I loaded `tools.py` without the package's `__init__`. The changed files also compile on Python 3.11–3.13.
- **Not run:**
  - `tests/test_agent_wiring.py`, because ADK isn't installed. It also checks a private ADK attribute name (`_require_confirmation`) that I couldn't confirm against the pinned ADK 2.8.0.
  - The full CI command.
  - An end-to-end test of ADK's approve/reject step.
  - A live call to the staging API.
  - Whether the model actually picks the tool.

**Not done**
- There is no automatic follow-up for `unknown` outcomes; a person has to check the order.
- There is no check that the customer owns the order.
- Confirmation hasn't been checked against the session store used on Cloud Run. ADK documents it as unsupported for some stores.

The eight questions I would have asked, and what I assumed, are in `REPORT.md` §2.

**Next prompt:** the skills gave no exact prompt to quote. They say to end with one for the verification still owed, so I wrote this:

> Take ticket T-201 and run the verification still owed: install the project's pinned dependencies (google-adk 2.8.0), run `pytest` including tests/test_agent_wiring.py, then add an offline ADK `/run_sse` test showing that cancel_order emits `adk_request_confirmation`, makes zero orders-API calls when rejected and exactly one when approved, and record the results in the ticket's Evidence section.