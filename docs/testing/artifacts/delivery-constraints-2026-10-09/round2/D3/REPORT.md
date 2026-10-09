# REPORT: ADK shopping assistant design session

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `/adk-system-designer` (by the user). No other skill was invoked; the design is design-only and the handoff points to `/adk-engineer`.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. Listing only: `.claude/skills/adk-model-and-output-contracts/assets/` and `references/`, and the set of `*/references/compatibility.md`
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
9. `grep` excerpts (first matching lines only) of every specialist's `references/compatibility.md`, to find the ADK version pin (2.8.0)
10. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (its trigger applied: browser contract, concurrent sessions, release continuity)
11. `.claude/skills/adk-system-designer/assets/system-design-template.md`
12. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
13. `grep` excerpt of `.claude/skills/adk-model-and-output-contracts/references/model-selection.md` (model lifecycle notes)

Not opened: `assets/ticket-template.md` (the user did not ask for tickets) and the `agents/openai.yaml`.

## 2. Questions I would have asked, and the answers I assumed

These are also the *Assumed answers* table (A1–A10) at the top of `docs/architecture/shopping-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Deadline, and what happens after it? | Live on the store in 2 weeks; work continues afterwards (phase 1 code is kept) |
| A2 | How many hours each, and how familiar with ADK/GCP? | 3 people × ~25 h/week; comfortable with Python and web, new to ADK, light GCP |
| A3 | Budget for models and cloud? | ≤ USD 300/month; model spend stop at USD 20/day |
| A4 | Who uses it, and is login required? | Anonymous external shoppers using a chat widget on the live store; no login |
| A5 | What does "place orders" mean? | The assistant builds the shopper's Shopify cart and hands over to Shopify's hosted checkout. The shopper pays and places the order; the agent never takes payment |
| A6 | What data does it touch and change? | Reads the public catalogue and writes only the session's own cart. Chat text may contain personal data; no customer accounts or order history in phase 1 |
| A7 | Catalogue size and existing stack? | ≤ 2,000 products on Shopify (Online Store 2.0 theme); no existing GCP project or backend |
| A8 | Languages and markets? | English, one currency, one market |
| A9 | Is there a Shopify development store for write tests? | Yes, or one can be created |
| A10 | Retention and privacy obligations? | 30-day conversation retention, a privacy note in the widget, no regulated data |

Also implied but not asked separately: the target ADK version (assumed `google-adk==2.8.0`), the model (assumed `gemini-3.8-flash` on Vertex AI), and the widget delivery route (theme app embed vs App Proxy vs hosted page; left to a G04 spike).

## 3. Files written or changed; what is not finished

Written (new):
- `docs/architecture/shopping-assistant.md`: the system design (draft). It covers assumed answers, journey, MVP profile, depth/floor/deferred table, invariants I1–I7, decisions D1–D10, model-facing contracts, data authority, security posture, budgets, failure table, verification and open decisions.
- `docs/plans/shopping-assistant.md`: the implementation plan. Phase 1 has G01–G07 with every field filled. Phase 2 has G08–G14, coarser, each with primary skill, estimate, acceptance and a run prompt. It also has the later list, the cut line, the parallel streams and a *Resume here* section.
- `REPORT.md` (this file).

No other files were changed. No code, dependencies or cloud resources were created.

Not finished:
- **No decisions are user-accepted.** The document stays **draft** until the founders confirm A1–A10, especially A5 and the cut line.
- **Provider facts are unverified (network was forbidden).** This covers Shopify Storefront cart mutation names and semantics, the cart attribute reaching the order, rate limits, cart expiry and API version, plus Vertex AI region availability and pricing for `gemini-3.8-flash` and Cloud Run/Cloud SQL prices. All are acceptance items of G01. The cost estimate is symbolic, with no prices filled in.
- **ADK API names** (`DatabaseSessionService`, `RunConfig.max_llm_calls`, `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS`) come from the skills' 2.8.0 notes. They have not been checked against an installed package.
- No tickets were written (not requested).

## 4. Checks run and not run

Run (local, no network):
- Relative-link check across both documents: all links resolve (`../plans/...` and `../architecture/...`).
- Capacity arithmetic: phase 1 sums to 49–70 h. Capacity is 3 × 25 × 2 × 0.6 = 90 h, and 67.5 h after the 25 % reserve. The low end fits; the high end is 2.5 h over. The plan states this and names the fallback (a hosted chat page instead of the theme embed, and a smaller eval set).
- Field-completeness check: every phase-1 goal (G01–G07) has Primary skill, Supporting skills, Prerequisites, Acceptance, Status and Run this goal. No field is missing.
- Word count: design 3,512 words, plan 3,332 words.

Not run:
- Any test importing `google.adk`. There is no code, and google-adk is not installed.
- All the acceptance checks in the plan (offline, local integration, live dev store, hosted). These are planned, not executed.
- The `adk-model-and-output-contracts` model-config audit script. There is no code to audit.
- Provider documentation lookups (network forbidden).

## 5. Friction log

**Unsure what to do**
- **No lookups possible.** `.claude/skills/adk-system-designer/SKILL.md:199-200` says "Check service availability, regions, limits and prices before relying on them; cite sources and dates", and `references/gcp-decisions.md:37-41` says the same. The session forbade network access. SKILL.md:201-203 ("keep those decisions provisional and name the exact verification needed") resolved it; I folded every check into G01. This was clear enough, but it meant the cost section could only be a formula.
- **Two tables disagree on what phase 1 needs.** `references/delivery-profiles.md:58` puts budgets at MVP as "Build: per-user allowance", and `:63` puts release engineering at MVP as "Build: evaluation in CI". But the worked example at `:187-190`, which is almost exactly this request ("Three people, two weeks to an MVP, customers can place orders"), says "Evaluation in CI, per-user budgets and traces follow in phase 2". Separately, `:114-115` says a per-user allowance on a public service is part of the floor and not to be cut. I kept the per-visitor allowance in phase 1 because it is the floor (G05). I moved CI evaluation and traces to phase 2 (G08, G09), following the example, and kept a manual pre-deploy eval run. The example contradicts the floor rule; it should say "per-user budgets beyond the floor allowance".
- **Which prompt to give.** The short form in `SKILL.md:275-277` (`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`) differs from the long form in `assets/implementation-plan-template.md:67-69` and `:113-119`. I used the long form in *Resume here* and the template's run line per goal. Two forms is mildly confusing.
- **How long the documents should be.** `SKILL.md:84-85` and `delivery-profiles.md:36` say an MVP gets "two to four pages per phase". Meanwhile `system-design-template.md` has 10 sections, and `SKILL.md:86-87` says a production design fills or marks every section. It was unclear whether an MVP should drop sections like the compact form does or keep all of them. I kept all sections, but tight; the design came out at ~3,500 words, likely a little over four pages.
- **Which model to pick.** `SKILL.md:195-199` says to choose from the lifecycle table, and the JSON (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12-15`) gives the dates. But no rule says how far out the "plan horizon" is when the user says "keep improving it". I assumed about 6 months. On that basis `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later) is borderline, so I chose `gemini-3.8-flash` and made 3.5-flash the comparison in G02.

**Heavier than needed**
- `references/design-decisions.md:198-226` (credential lifecycle, sensitive-data mapping, public-output release) and `:261-289` (shared allowance reservations, control-store outage) are aimed at bigger systems. I skimmed them and used one or two lines each. The reference's first lines (`:3-6`) do say to select, which helped.
- The plan template's full goal block (`implementation-plan-template.md:48-69`, 13 fields) × 7 phase-1 goals makes the plan about as long as the design. The coarse phase-2 form allowed by `delivery-profiles.md:132-134` was a relief.

**Genuinely helpful**
- `references/delivery-profiles.md:187-190` almost exactly predicted this request. It pointed straight at "idempotent order creation and explicit confirmation are in phase 1", which led to the checkout hand-off (D2), where the shopper is the confirmation.
- The floor at `references/delivery-profiles.md:70-92` (nothing irreversible without a human; spend stop) shaped the core structural decision: the agent has no payment or order tool at all.
- The capacity formula and reserve (`delivery-profiles.md:104-121`) gave a concrete cut line and the "if only the low end fits, say so" wording.
- The trifecta check (`design-decisions.md:182-196`) gave a clean security answer: no private-data leg in phase 1, and a re-check is triggered when G11 adds orders.
- The supporting-skill selection rules (`references/implementation-handoff.md:39-51`) made the Primary/Supporting lines quick and consistent.
- `adk-agent-observability/references/compatibility.md:9` noted that `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults to on. That became a concrete control for I7.
- The headless rule at `SKILL.md:119-122` (an Assumed answers table, provisional decisions) removed any doubt about how to proceed without the user.

## 6. Next prompt the skills told the user to type

The skill (`SKILL.md:272-277`) required an exact prompt for the next ready goal. Its example is, verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

The prompt given to the user, filled in from the plan's *Resume here* section:

```text
/adk-engineer Carry out G01 (Local agent recommends real catalogue products) from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-model-and-output-contracts and adk-tool-auth-and-secrets.
Work locally with read-only catalogue access, verify the G01 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```
