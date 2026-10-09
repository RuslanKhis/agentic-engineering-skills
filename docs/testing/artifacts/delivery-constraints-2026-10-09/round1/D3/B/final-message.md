I've written the design and a two-week plan, but everything in them is a draft built on my assumptions — you haven't agreed any of it yet. No code was written, nothing was run against Shopify or Google Cloud, and no tests were run (ADK isn't installed).

**The biggest assumption: what "place orders" means.** The assistant builds a Shopify cart and gives the shopper a Checkout button that opens Shopify's own checkout. Shopify takes payment and creates the order. The assistant never handles payment or creates orders itself. That removes almost all of the hard parts (duplicate orders, checking whether an order went through, payment handling). If you want orders placed inside the chat, it becomes a much bigger design, which I've parked as post-MVP goal G12.

**MVP shape:**
- **One assistant, four tools:** search products, get product details, update cart, view cart. It runs on Cloud Run with conversations stored in a small Postgres database. Shoppers don't sign in.
- **Only real products and links:** product cards and the checkout button are built from Shopify's data, not from the model's text, so it can't show a made-up product or link.
- **Spend limits enforced by the app:** a cap on model calls per reply, rate limits, a daily cap and a manual off switch. Google Cloud budget alerts only warn; they don't stop spending.
- **Model:** `gemini-3.8-flash`, fixed to that version. I chose it because the two previous versions are scheduled to retire on Google Cloud within the plan's timeframe.
- **Measuring quality first:** the first goal measures recommendation quality on about 40 labelled requests you write. It needs about two hours of founder time.

**The plan:**
- **MVP:**
  - D-01: check Shopify and Google Cloud facts.
  - G01: recommendations, measured.
  - G02: cart and checkout handoff.
  - G03: chat widget and API.
  - G04: launch on Cloud Run.
- **After:**
  - G05: automatic regression checks before each release.
  - G06: model upgrade drill.
  - G07: better search, if quality is too low.
  - G08: signed-in order status.
  - G09: reviews (this needs the assistant split in two for safety).
  - G10: streaming replies.
  - G11: screening for personal data.

**Decisions still open:**
- Is the checkout handoff acceptable as "placing orders"?
- What Shopify's storefront API can actually do on your store (search filters, cart, rate limits). D-01 checks this.
- Your monthly spend limit and which region to run in.
- Postgres versus Google's managed session storage.
- How long to keep transcripts (I assumed 30 days).

REPORT.md lists my 11 assumed answers, the checks run and not run, and the friction log.

Files are in `docs/`:
- docs/architecture/shopping-assistant.md
- docs/plans/shopping-assistant.md
- REPORT.md (in the project folder, not under `docs/`)

Next prompt to run:

```text
/adk-engineer Carry out G01 from docs/plans/shopping-assistant.md.
```