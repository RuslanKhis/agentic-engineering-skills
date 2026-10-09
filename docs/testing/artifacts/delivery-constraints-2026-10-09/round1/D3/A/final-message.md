I've written the design and the phased plan. Nothing was confirmed by you; every answer I'd have asked for is recorded as an assumption, so both documents are marked **draft**.

**Where things are:**
- Design: `docs/architecture/shopping-assistant.md`
- Plan: `docs/plans/shopping-assistant.md`
- Session report: `REPORT.md`

**The design in brief:** this is planned as an MVP for real external customers. It is one ADK agent with four tools:
- **Search and view products:** it reads your Shopify catalogue live, so prices and stock are always current.
- **Build the cart:** it sets an absolute quantity rather than adding, so a retry can't double an order line.
- **Show the cart with a checkout link:** prices and cart contents on screen come from Shopify's data, not from what the model writes.

"Placing an order" here means the assistant builds the cart and sends the customer to Shopify's own checkout to pay. The assistant never takes payment and never creates paid orders itself.

To keep costs bounded on a public site, it has a cap on model calls per turn, a turn limit per conversation, a per-visitor rate limit, a daily spending stop and an off switch. It runs on Cloud Run with a small Postgres database, using the `gemini-3.8-flash` model.

**Cut line:** I assumed about 25 hours a week each, which gives roughly 90 focused hours. After a 25% reserve, about 68 hours are left for building.
- **First two weeks (57–79 h):** check the Shopify details (D01), then G01–G07: the local agent, the cart, a 30–40-case test set, the chat API with its limits, the chat widget on your store, staging and production, and a launch check.
- **Day-6 fallback:** if you're behind, the widget becomes a separate chat page linked from the store header, saving about 5 hours. The spending limits and the test run before launch are never cut.
- **When things are quieter (G08–G14):** automated testing on every release, monitoring dashboards, streamed replies, smarter search, customer login with order status, abuse protection and personal-data screening. Each has a trigger that brings it forward.

**Decisions still open:**
1. Is sending customers to Shopify checkout acceptable as "placing orders"? If you need orders created inside the chat, that adds about 20 hours and doesn't fit the first two weeks.
2. The Shopify cart details my design relies on haven't been checked, because I had no network access. Checking them is the first discovery task, D01.
3. Your real hours, budget, cloud region and markets (EU/UK disclosure).
4. Whether you accept the risk of off-brand answers at launch, with test cases and the off switch as protection.
5. How to put the widget into your theme (a one-hour spike inside G05).
6. Model and database prices, which I couldn't look up.

**Not checked:** nothing was installed, run or provisioned. There's no code yet, so no tests ran, and the ADK version (2.8.0) still has to be confirmed in G01.

Next ready goal (D01 and writing the test cases can start in parallel):

```text
/adk-engineer Carry out G01 (local agent recommends real products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-workflow-design with adk-tool-interface-design, adk-agent-instructions and adk-model-and-output-contracts.
Work locally against the Shopify dev store only, verify G01's acceptance cases, and update
the plan with actual evidence and remaining blockers.
```