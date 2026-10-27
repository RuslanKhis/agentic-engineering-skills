I wrote the production design and plan, but the schedule helper never ran and the plan is unreviewed. This session has no shell and no subagent, so every hour and day figure is hand-computed and the plan has had no independent review.

**Files**
- `docs/architecture/claims-production.md` is the design. It is a draft, and nothing in it is accepted yet.
- `docs/plans/claims-production.md` is the plan: goals G00–G15 in phase 1, G16–G19 in phase 2, and a later list.
- I added one pointer line to the PoC design (`docs/architecture/claims.md`). It says the production design supersedes C5 and widens C4. Nothing else in the PoC documents changed.

**How the $1,500 ceiling is enforced**
- Billing export and budget alerts arrive hours to a day late and only notify. They cannot stop a request.
- The stop is an admission ledger in the application. Before any model call it reserves worst-case cost in Cloud SQL, then settles actual usage afterwards. It refuses work at the monthly and daily caps and at a per-handler cap.
- The plan includes an operator stop and starts the four PoC handlers under a $300 staged ceiling.
- Vertex AI quota, BigQuery bytes and quota, and Cloud Run max instances are backstops.
- The budget alert feeds a ratchet that can only tighten limits within the month, and a daily query compares the ledger with the billing export.
- The sponsor should know that the live bill isn't proven until G15 reads it against the contract.

**Biggest finding.** The PoC spent about £0.62 per claim (£38.20 over 62 claims). The ceiling works out to about $0.05 per request on average, assuming the fixed costs stay under $300. If one claim was one request, that is about 16 times over. G01 settles this before anything is sized. I used an illustrative $1.30 per £ for that comparison; that rate is my assumption.

**Profile and cut line**
- **Profile:** production.
- **Phase 1:** builds the service and takes it live for the four PoC handlers. It has 122–174 hours of goals plus 8–16 of handoffs, against 216 usable hours.
- **Finish:** limited go-live lands around working day 25–36 of 40. The first-bill reading lands around day 35–45, so at the high end it runs about five days into week 9.
- **Phase 2:** the 14-handler rollout, Fenwick IT handover and results review.

**Assumptions I proceeded on** (the Assumed answers table at the top of the design lists them with the decisions that depend on each)
- A "request" is one agent invocation. 20,000 a month is far more than the roughly 1,000 claims you'd expect from 14 handlers.
- The $1,500 covers the production project only.
- Both developers are close to full time, at 3.6 focused hours a day.
- "Eight weeks" means build plus the four-handler go-live, not all 14 handlers live.

**Left undone**
- **Schedule check:** the helper wasn't run. The command is in the plan; run it before trusting the figures.
- **Independent plan review:** it wasn't done. The prompt is at `.claude/skills/adk-system-designer/assets/plan-review-prompt.md`.
- **Prices, quotas and model retirement dates:** none were looked up because there was no network. They're placeholders that G01, G02 and G08 fill in.
- **ADK 2.12.0 behaviour:** the callback and `usage_metadata` behaviour is assumed. G03 and G04 confirm it.
- **Provider spend-cap budgets:** eligibility is unchecked, and the design does not rely on them.
- **Skills:** several skills the plan names aren't installed in this workspace, and no tickets were written.
- **Deferred security rules:** ASVS L2, a penetration test and Cloud Armor are deferred as an accepted risk that Fenwick security must confirm.

**Next prompt**
```text
/adk-engineer Carry out G00 from docs/plans/claims-production.md.
Read docs/architecture/claims-production.md and preserve its accepted decisions.
Send the wait requests W1–W5 and W9 and book W7; record owners and dates.
```