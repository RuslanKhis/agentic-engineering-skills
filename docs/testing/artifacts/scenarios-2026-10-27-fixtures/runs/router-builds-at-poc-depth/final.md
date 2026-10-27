The cancel-order feature for T-201 is written, but I couldn't run any of it. This session had no shell, so the tests, the ADK confirmation gate and the staging call are all unexecuted. I left the ticket at `in_progress`.

**Specialist:** `safe-api-tool-calls`, because cancelling an order is a state-changing call to an external API. That brings in the write rules: no blind retries, an honest "unknown" outcome, and a confirmation step. I treated the work as a proof of concept (3 hours, demo, fake staging orders) and added no other specialists.

**What I did**
- **New files:** `app/clients/orders.py`, `app/tools/cancellations.py` and `tests/test_cancellations.py` (7 tests).
- **Edited files:** `app/store.py`, `app/services.py`, `app/settings.py`, `app/agent.py`, `app/prompts.py`, `tests/fakes.py` and the ticket's Evidence section.
- **Ownership check:** the tool uses the signed-in user from the verified principal. Another customer's order, or one already shipped, delivered or cancelled, makes no API call.
- **Single attempt, no retries:** a 409 is reported as "already shipped". A timeout, a 5xx or an unexpected response body is reported as `unknown`, never as a failure.
- **Staging only:** the base URL defaults to the staging API. The token is read from `ORDERS_API_TOKEN`, so no secret is in the code.
- **Confirmation:** the tool is registered with `require_confirmation=True`, so the customer is asked before anything is cancelled.

**Not done**
- No tests run, including the 7 new ones and the existing suite.
- The ADK confirmation gate is unchecked because the SDK isn't installed, and no live staging call was made.
- I did not fetch the 1Password token. Someone needs to put it into `ORDERS_API_TOKEN`.
- Left out on purpose and listed in the ticket for the production ticket:
  - a durable record of operations and reconciliation of `unknown` results
  - idempotency
  - a guard against pointing the tool at a non-staging URL
  - spend limits
  - observability

**Questions, with the assumption I proceeded on**
1. **Order IDs:** staging holds HO-9xxxx fake orders, but the ticket's example HO-10518 is a local ID. I assumed the demo store gets seeded with HO-9xxxx orders for the demo user. That seeding is still owed.
2. **Repeat safety:** I don't know whether the cancel endpoint answers safely to a repeat call, so there are no retries. Ask the orders team before productionising.
3. **Confirmation:** I assumed you want a confirm step in the demo.

**Owed from you (about 1 hour):**
1. Run `python -m unittest discover -s tests -t .`.
2. Install ADK in a virtual environment and confirm the prompt appears and that a rejection makes no call.
3. Seed the demo orders and do one manual cancel against staging.

**Next prompt:** `/adk-engineer Resume tickets/T-201.md; run the tests, then verify confirmation with ADK installed.`