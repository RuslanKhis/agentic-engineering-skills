I've written the design and the plan, but neither has been machine-checked and the six-week date probably doesn't hold. This session couldn't run `check_schedule.py`, so the hours and finish dates are my hand arithmetic. The grid, contract and security-rule coverage was checked by reading only.

**What I wrote**
- `docs/architecture/warranty-returns.md` is the design. It has 6 requirements, 10 contracts (C1–C10), 10 decisions and open decisions O1–O11. It also has the web security rule table, the failure grids for 6 external systems, and Google product skill routes.
- `docs/plans/warranty-returns.md` is the plan. It has 19 phase-1 goals, 8 calendar waits, 6 phase-2 goals, a Later list and a ready-to-copy next prompt.

**Key design choices**
- **Profile:** I treated this as production because the data is real customer data.
- **One agent:** A single agent with three tools: list the customer's products, get warranty status, and propose a return.
- **Filing:** The agent can only create a draft return proposal. A separate confirm endpoint, which the customer's click calls, files the request and rechecks eligibility at that moment. Text typed in chat, including injected text, can't file anything.
- **Exactly-once:** A durable operation record with an idempotency key and a reconcile worker keeps a filed return to one request. How well this holds depends on whether the return system supports idempotency and lookup (O2). The first discovery goal (G03) checks that.
- **Warranty status:** Warranty status and eligibility are computed in code from the product database, not by the model.
- **Hosting:** One Cloud Run service behind a load balancer and Cloud Armor, with Cloud SQL for sessions and operation records.

**Assumptions I proceeded on** (nobody could answer; every dependent decision is marked provisional):
- Start date 2026-11-02, 30 working days.
- Two developers at 4.8 focused hours a day each, new to ADK.
- No spend figure or volume.
- A customer identity provider, a product database and a return system with sandbox access all exist.
- Residency and retention are unknown.

**The six-week date is at risk**
- Phase 1 comes to 149–223 hours against 216 usable after a 25% reserve, so only the low end fits.
- The calendar is the bigger problem. Waits on other teams (landing zone, data access, identity, a pen test) put my rough finish between working day 30 and day 41.
- The plan lists remedies I haven't tested: a later external canary, an earlier pen test, a third person, or about 8 weeks.
- The cut line puts ramp to 100%, the ASVS Level 2 review, the support rollout pack and the first live bill in phase 2. Please confirm or move it.

**Left undone**
- **Schedule check:** I didn't run `check_schedule.py`; the plan has the exact command.
- **Skill names:** Google's `finding-google-skills` router is installed, but I didn't run it. The `google/skills:*` names come from the designer's table dated 21 October 2026, so confirm each through the router before first use. None of the product skills or most specialists the plan names are installed.
- **Not looked up:** I looked up no prices, no model ID (G02 picks one from the lifecycle table) and no ADK pin beyond the assumed `google-adk==2.8.0`.
- **Not done:** I wrote no tickets and ran no independent plan review, so treat the plan as unreviewed. Nothing was installed or touched in the cloud.

**Today, before any build:** request W1 (project, billing, IAM), W2 (product database and return system access), W3 (identity client and test customers), W5 (warranty experts' labelling session) and book the pen test (W6).

```text
/adk-engineer Carry out G02 from docs/plans/warranty-returns.md.
Read docs/architecture/warranty-returns.md and preserve its accepted decisions.
Use adk-workflow-design with adk-model-and-output-contracts.
Work locally only, verify A1 to A4, and update the plan with actual evidence.
```