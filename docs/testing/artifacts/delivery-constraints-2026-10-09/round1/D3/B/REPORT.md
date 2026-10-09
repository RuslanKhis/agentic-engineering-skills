# REPORT — ADK shopping assistant design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer` command; SKILL.md loaded).
2. `.claude/skills/adk-system-designer/references/design-decisions.md`
3. `.claude/skills/adk-system-designer/references/failure-review.md`
4. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
5. `.claude/skills/adk-system-designer/assets/system-design-template.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
8. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (read in full)
9. `references/compatibility.md` of every specialist skill — only the first matching version lines via `grep`, not full reads
10. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (its trigger applied: browser delivery, concurrent sessions, release continuity)

I did not open `assets/ticket-template.md`, because no tickets were requested. No other skill was invoked.

## 2. Questions I would have asked, and the answers I assumed

These are also the **Assumed answers** table at the top of the design (A1–A11):

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | How much time and money is there? | 2 weeks, 3 people part-time; spend in the low hundreds of USD/month (exact figure unknown) |
| A2 | Who judges the result, and what do they read? | Founders and customers, through the running assistant on the live store; checkout-started rate |
| A3 | What kind of artifact? | A limited-launch production MVP |
| A4 | What does "place orders through Shopify" mean? | Build a Shopify cart and hand the shopper to Shopify's hosted checkout. The assistant never takes payment and never creates orders through the Admin API |
| A5 | Must customers sign in? | No. Anonymous shoppers in the MVP |
| A6 | How big is the catalogue, and is Shopify search good enough? | Hundreds to low thousands of products. Start with Storefront search and measure it |
| A7 | What infrastructure exists already? | A Shopify Online Store theme and a GCP project with billing. No backend, database or login |
| A8 | How much traffic? | Fewer than ~500 conversations a day; a few concurrent at peak |
| A9 | Which languages, markets and regulations? | English, one market, one currency, GDPR-style privacy; 30-day transcript retention |
| A10 | May the assistant use reviews or other third-party content? | Not in the MVP |
| A11 | May it give discounts or make policy promises? | No discounts. Policy answers come only from merchant-approved text in config |

The design also lists other open questions with their owners, not assumed answers: monthly spend allowance, region, session store choice, and dev-set labelling time.

## 3. Files written or changed; what was not finished

Written:
- `docs/architecture/shopping-assistant.md` — draft system design. It covers the assumed answers, scope gate, deferred controls, invariants I1–I6, targets T1–T2, decisions D1–D10, model-facing contracts, data/authority, security posture, budgets, failure table, verification and open decisions.
  - After writing it, I changed it once with `sed` so the tool count is consistently four (policy moved into state).
- `docs/plans/shopping-assistant.md` — implementation plan.
  - Discovery goal D-01; MVP goals G01–G04, each with full fields and its own run prompt; post-MVP goals G05–G12 kept coarse.
  - A suggested two-week calendar and a "Resume here" section.
- `REPORT.md` (this file).

Not finished, or deliberately left open:
- **No decision is user-accepted.** Everything is a provisional recommendation.
- **Shopify facts are unverified:** Storefront search filters, cart mutations, `checkoutUrl`, cart expiry, rate limits. This is goal D-01.
- **GCP facts are unverified:** region availability, Cloud Run/Cloud SQL/Vertex prices. The cost estimate is symbolic only.
- **ADK version:** 2.8.0 is a working assumption taken from the specialists' compatibility files. API names (`App`, `Runner`, `RunConfig.max_llm_calls`, `DatabaseSessionService`, `output_schema` with tools) still need confirming against the chosen pin in G01.
- No tickets, no code, no scaffolding (design-only request).

## 4. Checks run and checks not run

Run:
- `grep`/`ls` check that every skill named in the design and plan exists under `.claude/skills/`. Result: all exist, none missing.
- Checked that both docs exist at the conventional paths, and counted `Primary skill` lines in the plan: 5, one for each fully specified goal (D-01, G01–G04).
- A manual `grep` for leftover "five tools" wording after the tool-count fix. Result: no matches.

Not run:
- Any test importing `google.adk`. ADK is not installed and no code exists; this was a design-only request.
- Any Shopify, Vertex AI or GCP lookup or call. Network and cloud commands were forbidden, so provider facts, prices, regions and model availability are unverified.
- A Markdown renderer or link checker. Relative links were written by hand and not checked mechanically.

## 5. Friction log

**Unsure what to do:**
- **Artifact size.** The request is a customer-facing service that takes orders, which is "production". But it is also a 2-week MVP for 3 people, which is closer to a "pilot".
  - `SKILL.md:62-67` sizes these very differently: "two to four pages" against "as long as its decisions require, with every template section either filled or marked not applicable".
  - I chose "limited-launch production MVP" and filled every template section, kept compact. The design is about 4.6k words, longer than a pilot.
  - There is no guidance for this common hybrid.
- **The proportionality rule** (`references/design-decisions.md:37-44`) applies "when the artifact is judged on output quality". Here quality is half the story; the other half is a safe order path.
  - I applied it to G01 (measured recommendation quality first).
  - I kept checkout safety in the MVP.
- **Primary skill for G01.** `references/implementation-handoff.md:21` maps "bounded orchestration" to `adk-workflow-design`. But the slice's risk is in the tool interface and quality measurement.
  - I chose `adk-tool-interface-design` as primary.
  - The mapping gives no tie-break rule for a first slice that touches four specialists.
- **Model backend.** The lifecycle JSON is mainly about the Gemini API, with `vertex_retirement` as a secondary field.
  - For `gemini-3.8-flash`, the Vertex retirement field is missing, not null. I read that as "none announced", which is an inference.
  - `SKILL.md:169-173` says to use the table but not how to read missing fields.
- **The ticket template.** `SKILL.md` "Deliver and hand off" says to write tickets only "when the user wants tickets". The user didn't say, so I skipped them.
- **"What the reviewer reads"** (`assets/implementation-plan-template.md:60-71`) and "Name the deliverable the evaluator will judge" (`assets/system-design-template.md:103-107`) are written for assignment/prediction deliverables.
  - Adapting them to a running service took some interpretation.

**Heavier than needed:**
- **The design template** (`assets/system-design-template.md`) plus the "every section filled" rule for production pushed a 2-week MVP design toward 4–5 pages. Its failure table and data table are useful, but fairly heavy for three people.
- **`references/design-decisions.md:226-257`** (external effects and recovery) is long. Most of it turned out not to apply, because of one decision: Shopify hosted checkout. It would help to say early that removing the binding write removes this whole section.

**Genuinely helpful:**
- **The "Assumed answers" table rule** (`SKILL.md:92-96`) gave a clean way to handle a headless run without stalling.
- **The scope gate** (`SKILL.md:52-60`) made the MVP/post-MVP split straightforward.
- **The lethal-trifecta check** (`references/design-decisions.md:180-194`) made it obvious that the MVP is safe as one agent. It also showed that adding reviews (G09) or sign-in (G08) changes the topology, so I could pre-commit the split as a gate.
- **The model lifecycle table, read instead of memory** (`SKILL.md:169-173`). It steered me away from `gemini-3.6-flash`, whose Vertex retirement on 2026-11-19 falls inside the plan horizon.
- **"Model proposals, user confirmation and backend authorization are separate"** (SKILL.md "Turn requirements into contracts"). Together with "what the application already knows belongs in code", this produced the most useful invariants: I1 (product cards rendered from tool data) and I2 (checkout link only from Shopify's `checkoutUrl`).
- **Alerts-only billing budgets do not cap spend** (`references/gcp-decisions.md:64-68`). This directly shaped D8, the application-enforced caps and kill switch.
- **The plan template's per-goal run prompt and "Resume here"** (`assets/implementation-plan-template.md:50-52, 82-98`) made the handoff unambiguous.

## 6. Exact next prompt the skills told the user to type

From the plan's "Resume here", following the template at `assets/implementation-plan-template.md:89-95`:

```text
/adk-engineer Carry out G01 — Assistant recommends real products, measured from docs/plans/shopping-assistant.md.
Read docs/architecture/shopping-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions, adk-model-and-output-contracts, adk-agent-evaluation and adk-workflow-design.
Work within local code changes and a bounded live dev-set run (≤ 400 model calls), verify the offline I1/repair cases and the dev-set score, and update
the plan with actual evidence and remaining blockers.
```

The short form, as given in `SKILL.md`'s example (`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`), instantiated:

```text
/adk-engineer Carry out G01 from docs/plans/shopping-assistant.md.
```
