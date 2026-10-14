I've written the design, the plan and 33 phase 1 tickets, but the plan does **not** reliably meet the 15 March 2027 GA date: it finishes in 67–102 working days against the 95 available. My first draft passed the schedule check, but an independent review of the plan found real gaps. Once those were fixed, only the low end fits. Nothing was implemented.

**Profile:** production service. Real customers, personal data and photos, and it writes real claims into Guidewire ClaimCenter.

**Design in brief:**
- **One assistant, no write access.** The assistant can only fill in the customer's own claim draft. It has no way to create a claim or send anything out.
- **Filing:** application code files the claim, and only after the customer confirms a summary rendered by the server. It runs as a durable step-by-step operation, so retries or lost responses can't create a second claim.
- **Hosting and data:** Cloud Run and Cloud SQL in Frankfurt, with photos in an EU storage bucket.
- **Model:** `gemini-3.8-flash` on Vertex AI, pinned. The two models before it retire before GA.
- **Fallback:** if the assistant is unavailable or a storm overloads it, customers continue in the existing claim form, prefilled from their draft.

**Effort and date:**
- **Hours aren't the problem.** Phase 1 needs 573–853 agent-assisted hours, about a third of the ~2,209 h the team has after a 25 % reserve.
- **The calendar is.** The longest chain runs through infrastructure, the fallback and portal screens, then the external pen test and its retest, go-live approval, launch and rollout soak time.
- **Recommendation:** move GA to **2027-03-25** (103 working days), which fits with half a day to spare. Every other remedy I tested falls short. If the pen test takes more than 15 days, even that date slips.

**What ships at GA:** goals G01–G26 and G33–G39. Phase 2 (G27–G32) and a later list wait. Two phase 2 items, a deterministic guard against coverage promises (G32) and cost tuning (G30), could move into phase 1 without changing the finish.

**What I couldn't check:**
- No network access, so these are unverified: EU availability of the model and of Model Armor, the Guidewire API details (including how it de-duplicates requests), and prices. Each is assigned to an early ticket.
- No application tests exist, and `google-adk` isn't installed.
- I did run the skill's schedule checker (final run exits 1 at 95 days, 0 at 103) and its own 16 unit tests, which passed.

**Decisions open for you:**
- the GA date, or the cut line;
- the 14 assumed answers at the top of the design;
- three residual risks: coverage promises are prevented only by instructions and testing, photos aren't checked for authenticity, and it runs in a single region;
- whether the 18 calendar-wait lengths are right; all are my assumptions.

Send the day-1 requests now. The biggest are Guidewire non-prod access, the pen-test and retest bookings, the GCP projects, the customer-login test tenant, the claim-form prefill change and the claims-handler booking.

`REPORT.md` has the skills and files used, the assumed answers, the checks run and not run, and the friction log.

Files are in `docs/`:
- architecture/home-claim-intake.md
- plans/home-claim-intake.md
- tickets/home-claim-intake/ (33 tickets)

Next ready goal:

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-agent-service-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

G01, G13 and G15 can start in parallel on day 1.