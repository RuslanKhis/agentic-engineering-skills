I added a `cancel_order` tool for the T-201 demo and wired it so the customer must approve each cancellation in chat. Offline tests pass (19 passed, 1 skipped), but the approval step itself has not been exercised and nothing has run against staging or a live model.

**Specialist: `safe-api-tool-calls`**, because the ticket adds a write call to an external API (POST `/orders/{id}/cancel`). The risks there are hidden retries, cancelling twice and outcomes the agent can't confirm. The ticket doesn't name a primary skill.

**What I changed**
- **`support_agent/tools.py`**: new `cancel_order(order_id)`.
  - It checks the order ID before sending anything.
  - It makes exactly one attempt, with no retries, because we don't know whether the endpoint is safe to repeat.
  - Results:
    - Success → `cancelled`.
    - The API refused, or the request was never sent → `error`.
    - Timeout, other transport errors or a server error → `unknown`, with a "do not retry" message.
  - It calls staging by default (overridable with the `CANCEL_ORDERS_API` environment variable), kept separate from the production `ORDERS_API`.
- **`support_agent/agent.py`**: `root_agent` gets the tool behind ADK's approval prompt (`require_confirmation=True`), plus one instruction sentence telling it to call once and not again after `unknown`.
- **`support_agent/__init__.py`**: `root_agent` now loads only when first used, so tool tests run without ADK installed. `from support_agent import root_agent` still works.
- **Tests**: `tests/test_cancel_order.py` (18 tests) and `tests/test_agent_wiring.py` (checks the approval wiring; needs ADK).
- `tickets/T-201.md` now has an Evidence section, and `REPORT.md` has the six sections you asked for.

**Checks**
- **Run:** the tool tests with the orders API replaced by a fake and real network connections blocked. They cover success, invalid IDs sending nothing, refusals, a cancel that goes through but whose reply is lost (reported `unknown`, sent once), server errors and retries being off. The existing `tests/test_tools.py` now passes too; before, it couldn't import without ADK.
- **Python version:** these ran on Python 3.9, the only interpreter here with httpx and pytest. The project requires 3.11, where I only checked that the files parse.
- **Not run:**
  - The ADK wiring test (ADK isn't installed). It also reads a private ADK attribute whose name I couldn't confirm.
  - An end-to-end test that a missing or rejected approval sends nothing.
  - The live model, and the staging API itself.

**Questions I'd have asked** (assumed answers are in REPORT.md §2): whether the cancel endpoint is safe to repeat, which status codes it returns, whether staging needs authentication, and whether the demo runs through `adk web` or our own runner.

**Left out on purpose** (each with what would bring it back in the ticket):
- **Spend limit on model calls:** not built, because where to enforce it depends on how the demo runs. For the demo, set a budget alert on the API key's project.
- **Production controls:**
  - a stored record per cancel, so a retry can't cancel twice;
  - follow-up on `unknown` outcomes;
  - checking the customer owns the order;
  - re-checking the order between approval and sending.
- **Model:** `gemini-2.5-pro` stays. It retires on 20 October, after Tuesday's demo; T-103 covers moving off it.

**Next prompt:** the skills didn't give one word for word. They said to write one for the verification still owed, so here it is:

> Install the project dependencies (google-adk==2.8.0) in a Python 3.11 venv and run `pytest tests/`, including `tests/test_agent_wiring.py`. Then, using safe-api-tool-calls, add an offline ADK HTTP/SSE test for `cancel_order` with a scripted model. Missing or rejected confirmation must send zero POSTs to the orders API, and an approved one exactly one. Record the results in the Evidence section of tickets/T-201.md.