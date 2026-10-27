I fixed both problems and added tests, but I haven't run any of it. My session has no shell tool, so the new tests and the existing suite are unrun (`not run`). Please run `python -m unittest discover -s tests -t .`.

**Why it failed and what changed**
- **KeyError:** there were two causes, both in `app/prompts.py`.
  - **`{order_id}`:** it sits inside the JSON example, and nothing in the app ever writes an `order_id` state key. I replaced it with a literal `"<order id if the customer gave one>"`. The JSON example now renders as written.
  - **`{customer_profile}`:** `load_profile` only writes it after the first model request, so the first render would also have raised. It is now `{customer_profile?}`, which renders as empty until the tool has run.
- **Routing:**
  - **Descriptions:** the sub-agent descriptions were one or two words ("Billing", "Refunds", "Order help"). I rewrote them as `BILLING_DESCRIPTION`, `REFUNDS_DESCRIPTION` and `ORDERS_DESCRIPTION`, and `app/agent.py` now uses them. The billing description names `refunds_agent` as the owner of refunds and cancellations.
  - **Coordinator instruction:** it now picks the colleague by what the customer wants to happen and tells the coordinator to choose `refunds_agent` when a message mixes a refund request with an invoice question.
  - **Refund rule:** I reworded "Never promise a refund yourself" to say only `refunds_agent` decides refunds.

**Tests (`tests/test_prompts.py`)**
- **Render test:** it renders the coordinator instruction with and without profile state. It uses an SDK-free copy of the 2.8.0 placeholder rules, because `google.adk` can't be imported in the unit tests. It also asserts that every state placeholder is optional.
- **Routing check:** it covers the routing contract:
  - Descriptions are at least 8 words and overlap by less than 0.6 between siblings.
  - Billing names its boundary with refunds.
  - The coordinator names every colleague.
  - The `ROUTING_CASES` list has at least one case per agent.

**Left undone**
- **Model choice:** no test shows which agent a model actually picks, since no credentials are available. `ROUTING_CASES` is a labelled set ready for a live evaluation that checks the `transfer_to_agent` target. That run needs your approval and credentials.
- **Real ADK render:** I did not run the instruction through the real `inject_session_state`, so the render is only verified against my copy of the rules. The version-specific details came from the skill's 2.8.0 notes, not from the installed source.

**Assumptions I made**
- **Refund vs billing:** a message mixing both goes to `refunds_agent`. Change that line if you want the reverse.
- **Order id in the note:** the model fills the `"order"` field in the JSON note itself, since the app has no order-id state.