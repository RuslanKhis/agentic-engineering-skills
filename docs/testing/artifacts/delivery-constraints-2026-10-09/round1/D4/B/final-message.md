I've written the design and the build plan for the card dispute assistant, plus `REPORT.md`, and implemented nothing. Both documents are drafts: you weren't available, so all 14 scope answers (A1–A14) are assumptions I made, listed in a table at the top of the design, and nothing in it has been approved yet.

**Delivery profile:** production service. It serves external customers, handles regulated personal data, and opens cases that can lead to money being refunded.

**Core design:**
- **One agent, no power to submit.** A single ADK agent has five tools, all of which only read data or save a draft. It can't open a case itself.
- **The customer confirms in code.** A case is opened only when the customer presses Confirm on a summary card that our code renders. The confirmation is tied to a hash of that exact summary, so a "yes, submit it" typed into the chat does nothing.
- **At most one case per confirmation.** Each confirmed dispute gets a durable record in our own database. A reconciliation job checks for a case before any resend; if it can't tell, the item goes to a manual queue.
- **Customer identity comes from the login token, not the model.** Only the customer's own transactions are ever looked up.
- **Full card numbers are stripped** before anything is stored, sent to the model or logged.
- **If the model is down,** customers fall back to the existing static dispute form and a "talk to a person" option.
- **Hosting:** Cloud Run and Vertex AI in an EU region, with pinned versions: `gemini-3.8-flash` (picked from the dated model-lifecycle table) and `google-adk==2.8.0`.

**Cut line:** capacity is about 2,450 focused hours, or about 1,840 after a 25% reserve. Phase 1 (G00–G15, up to general availability around 2027-02-08) is estimated at 1,440–2,184 hours. The middle estimate (about 1,810) fits; the high end doesn't. If it runs over, the plan cuts in this order: the load test, then per-customer allowances, then dashboards. Safety controls and the pilot are never cut; if they don't fit, the launch date moves. Phase 2 adds evidence uploads, a second language and case-status questions.

**Main open decisions:** the most important is whether core banking can deduplicate a repeated "create case" request or look one up by our reference; that decides how strong the one-case guarantee is (G00 finds out). Others:
- whether `gemini-3.8-flash` is offered in the chosen EU region, and on what quotas and data-retention terms (G01);
- whether the bank's platform team requires its own Kubernetes platform instead of Cloud Run;
- how long conversations are kept, pending the data protection officer's confirmation;
- baselines and target numbers for accuracy and service levels;
- the monthly spend ceiling.

All ten are in the design with an owner and the goal each one blocks.

**Checks:** links between the two documents resolve, every phase 1 goal has all required fields, and the estimate totals add up. Nothing that imports ADK was run, there was no network lookup of models, regions or prices, and the diagrams weren't rendered to check their syntax. The regulations named (PSD2, GDPR, the EU AI Act, DORA) come from general knowledge and need the bank's compliance team to review them.

To get the right model ID, I read the model-lifecycle table from your skills source folder, because it isn't installed in this project; I logged that in the report's friction log.

Files are in `docs/`:
- `docs/architecture/card-dispute-assistant.md`
- `docs/plans/card-dispute-assistant.md`
- `REPORT.md`

The next goal ready to run is G02, a minimal end-to-end version that shows a customer only their own transactions. It runs locally with a fake core banking system and a test login, so it doesn't wait on any open decision:

```text
/adk-engineer Carry out G02 (walking skeleton with scoped transaction lookup) from docs/plans/card-dispute-assistant.md.
Read docs/architecture/card-dispute-assistant.md and preserve its accepted decisions.
Use adk-tool-auth-and-secrets with adk-workflow-design and adk-tool-interface-design.
Work locally with a fake core-banking adapter and a test token issuer, verify the
cross-customer denial, session-ownership and restart acceptance cases, and update
the plan with actual evidence and remaining blockers.
```