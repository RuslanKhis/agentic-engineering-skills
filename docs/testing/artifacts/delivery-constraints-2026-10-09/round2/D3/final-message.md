I've written the design and plan for the shopping assistant, plus `REPORT.md`. No code was written and no tests were run: there's no code yet and google-adk isn't installed. Everything is a **draft** built on ten assumed answers, recorded in a table at the top of the design.

- **Design:** `docs/architecture/shopping-assistant.md`
- **Plan:** `docs/plans/shopping-assistant.md`

**Profile:** MVP. External shoppers use it and real orders go through Shopify, so order safety and spending limits are built in the first two weeks. Testing in CI, tracing and polish come later.

**The main design call.** "Place orders" means the assistant fills the shopper's Shopify cart and hands them Shopify's own checkout, where they pay. The agent has no tool that can take payment, create an order, change a price or apply a discount. Prices, stock and cart totals on screen always come from Shopify, not from the model's text.

**Cut line:**
- **Capacity:** I assumed 3 people × 25 h/week × 2 weeks. That gives about 90 focused hours, or about 67 h after a 25 % reserve.
- **Phase 1 (G01–G07):** 49–70 h. It covers the agent with product search, a set of test conversations, the cart and checkout hand-off, the backend and store chat widget, usage and spending limits, Cloud Run deployment with rollback, and a check before launch.
- **Fit:** the low estimate fits; the high one runs about 3 h into the reserve. If work runs high, the widget becomes a separate chat page linked from the store, and the test set stays at 20 conversations.
- **Phase 2 (G08–G14), when things are quieter:** tests in CI, tracing and alerts, streaming replies, logged-in customers with order status, sales attribution, better search, and screening of personal data.

**Still open:**
- Whether a checkout hand-off counts as "placing orders" for you.
- Your real hours and budget (I assumed a $20/day model limit).
- The widget delivery route.
- Privacy wording and keeping conversations for 30 days.

I couldn't check any Shopify or Google Cloud facts or prices because network access was off. Those checks are part of G01, so the cost section is a formula without prices.

`REPORT.md` lists the files I read, the questions with assumed answers, the checks I ran and didn't run, and where the skill was unclear. The main one: the MVP example in `delivery-profiles.md` puts per-user budgets in phase 2, but the same file says that limit can't be cut. I kept the limit in phase 1.

Next step, ready now:

```text
/adk-engineer Carry out G01 (Local agent recommends real catalogue products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-model-and-output-contracts and adk-tool-auth-and-secrets.
Work locally with read-only catalogue access, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```