# Report: home-insurance claim intake design session (headless)

Date: 2026-10-09. Nobody was available to answer questions, so every answer
is an assumption (recorded below and in the design's **Assumed answers** table).
Nothing was implemented and no network, cloud or install command ran.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked via `/adk-system-designer` (SKILL.md loaded by the harness).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`
   (items 4–7 were read in one `cat`)
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-system-designer/assets/system-design-template.md`
10. `.claude/skills/adk-system-designer/assets/ticket-template.md`
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `grep` over every `.claude/skills/*/references/compatibility.md` to find
    the ADK version the specialists were checked against (2.8.0), plus the
    2.10.0 recommendation in `adk-agent-observability/references/compatibility.md`.

No other skill was invoked. I read no specialist SKILL.md: the designer says
it "needs no other skills" (SKILL.md:24-25), and the request said not to
implement.

## 2. Questions I would have asked, and the answers I assumed

The full table, with the decisions that depend on each answer, is at the top of
`docs/architecture/home-claim-intake.md` (A1–A18).

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Which EU market(s) and languages at GA? | Germany only; German and English |
| A2 | Which Guidewire deployment and API? | ClaimCenter on Guidewire Cloud with Cloud API, a sandbox, and OAuth2 client credentials; idempotency unknown |
| A3 | How do customers sign in? | Existing portal OIDC CIAM; subject maps to the policyholder through an existing policy API |
| A4 | Where does the UI live, and who builds it? | Embedded in the existing web portal (app web view); our frontend engineer builds it and the portal team reviews |
| A5 | What GCP footprint exists? | Organisation exists, EU location policy possible, a platform team creates projects, Terraform |
| A6 | How familiar is the team with ADK and GCP? | Knows Python and GCP, new to ADK (estimates × 1.5); security reviewer about 8 h/week |
| A7 | What budget is there? | ≤ €2k/month non-production, ≤ €8k/month production, ≤ €0.25 model cost per claim |
| A8 | What volume? | ~60k home claims a year, 30 % digital in year 1, storm day 10× |
| A9 | What may the assistant change? | It creates an FNOL plus attachments, only after the customer confirms; no coverage decisions, payments or edits |
| A10 | Who handles the claims? | Existing handlers; claims flagged `digital-assistant`, AI suggestions labelled |
| A11 | How long is data kept? | 30 days in our stores after submission or abandonment; ClaimCenter keeps its normal retention |
| A12 | What SLOs? | 99.5 % availability, p95 reply ≤ 8 s, claim number ≤ 2 min, uncertain cases resolved ≤ 24 h (provisional) |
| A13 | What is the regulatory position? | DPIA needed, AI Act transparency applies, not Annex III high-risk, DORA covered (all to be confirmed by compliance) |
| A14 | May photos go to a model? | Yes, in the EU, under the DPIA |
| A15 | How do customers reach a human? | Hotline and web form fallback; live hand-off in phase 2 |
| A16 | Will there be a pilot? | ~200 invited customers from week 13, in production ClaimCenter |
| A17 | Who acknowledges the claim to the customer? | ClaimCenter or existing communications; the assistant sends nothing |
| A18 | Is the cut line accepted? | Provisionally: phase 1 = G01–G20, phase 2 = G21–G26 |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/home-claim-intake.md`: the full production design. It covers the assumed answers, journey, depth table, guarantees I1–I10, decisions D1–D13, model-facing contracts, data and authority, security posture, budgets, failure table, verification and open decisions O1–O8. It is marked **draft**.
- `docs/plans/home-claim-intake.md`: the plan. It covers the capacity calculation, cut line, per-person load table, longest chain, implementation map, G01–G20 in full, G21–G26 in coarser form, the later list, open decisions and "Resume here".
- `docs/tickets/home-claim-intake/G01-…md` to `G20-…md`: 20 tickets, one per phase 1 goal. Four are `ready` (G01–G04); the other 16 are `blocked` on goals before them.
- `REPORT.md` (this file).

The plan and tickets were generated from one goal table by an inline
`python3 -I -` script, so they cannot disagree. The script was not saved to disk.

Not finished:

- No user has reviewed or accepted any decision; the design stays draft.
- Provider facts are **unverified** because I had no network access. These are: `gemini-3.8-flash` availability, quota, price and data-processing terms in an EU Vertex AI region; Model Armor in the EU; every Guidewire Cloud API detail (endpoints, idempotency, lookup); and the regulatory reading. They are labelled assumptions, and G01, G02 and G03 are the goals that settle them.
- The cost estimate is symbolic only, with no prices.
- The ADK version is a working assumption (2.8.0); G04 chooses the pin.
- I added no ADR files. G01 and G02 will create them.

## 4. Checks run, and checks not run

Run:

- **Estimate arithmetic** (generator assertion): every goal satisfies high ≤ 2 × low, and hands-on plus review equals the total. The phase 1 sum is 820–1,400 h. Passed.
- **Document consistency script** over the 22 Markdown files under `docs/`. Passed with no errors. It checked that:
  - every relative link resolves;
  - every backticked skill name and every ticket `primary_skill` and `supporting_skills` entry exists in `.claude/skills/`;
  - each ticket's total estimate matches both the plan's goal table and its goal section;
  - no template placeholders are left.

Not run:

- Any test that imports `google.adk`: none exist yet, and the dependencies are not installed.
- Any check of ADK interfaces against an installed version (that is G04).
- Any Guidewire sandbox, Vertex AI, Model Armor, pricing or regional-availability lookup, because network and cloud commands were not allowed.
- Markdown rendering and Mermaid diagram rendering.
- Human review of the documents.

## 5. Friction log

- **Production sizing collided with the reference's small-slice estimates.**
  The estimate table at `.claude/skills/adk-system-designer/references/delivery-profiles.md:124-136` only covers 1–16 h slices for one developer. Applying it naively gave about 420–700 h of phase 1 work against roughly 2,830 h of capacity, which would leave most of a six-person team idle for five months.
  I scaled the goals up by judgement (for example, frontend 120–200 h) and kept the leftover capacity as a stated margin rather than filling it.
  The reference gives no guidance for multi-month team programmes, or for work these goals don't cover (Guidewire configuration, the portal team, training).
- **The focus factor was ambiguous for a full-time team over months.**
  `delivery-profiles.md:153-155` offers 0.6 for part-time or interrupted work and 0.8 for a "dedicated block such as a single afternoon". Neither fits five full-time engineers over 19 weeks. I used 0.6.
- **The rule "a range wider than 2× hides a question"** (`delivery-profiles.md:140-141`) was **helpful**. Enforcing it in the generator kept the estimates honest.
- **"Tickets for ready goals" didn't match the user's request for phase 1 tickets.**
  `SKILL.md:268-269` says to write one file per *ready* goal, but the user asked for tickets for all phase 1 goals. The ticket template defaults to `status: ready` (`assets/ticket-template.md:17`) and has no blocked state.
  I wrote all 20 tickets and used `status: blocked` together with `blocked_by`. I was unsure whether that was allowed.
- **What "phase 1" means for a production programme was unclear.**
  `delivery-profiles.md:177-178` says phase 1 delivers the profile's "done". For a production profile that means the whole route to GA, so phase 1 has 20 goals, and the plan document is longer than the design.
  `SKILL.md:85-86` ("as long as its decisions require") allowed this, but I was unsure whether milestones (alpha, pilot, GA) should have been phases instead.
- **The design template contains sections for quality-judged deliverables** (`assets/system-design-template.md:123-127`). They don't apply here. Following `SKILL.md:85-87` (production: "every template section either filled or marked not applicable"), I added an explicit N/A line.
- **The model-lifecycle pointer was genuinely helpful** (`SKILL.md:198-201` together with `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`). It showed that `gemini-3.7-flash` reaches Vertex retirement on 2027-01-28, before GA. Choosing from memory would likely have missed that.
  One friction point: the file is a Gemini API snapshot and does not show EU-region availability on Vertex, so the choice stays provisional (`model-lifecycle-2026-10-01.json:10`).
- **The guidance on which ADK version to assume conflicted.** `SKILL.md:193-196` says to assume the version the specialists were checked against (2.8.0). But `adk-agent-observability/references/compatibility.md` recommends 2.10.0 or later for a new production deployment. I recorded both and gave the choice to G04.
- **The "Assumed answers" instruction worked well for a headless run** (`SKILL.md:121-124`). It turned the scope gate into a table without any back-and-forth.
- **Heavier than needed:** the plan template (`assets/implementation-plan-template.md:56-79`) has 13 fields per goal, and with 20 goals that took about 8k words. Generating it from a table was the only practical way to keep it consistent with the tickets.
- **The trifecta guidance in `references/design-decisions.md:182-196` was genuinely helpful.** It led directly to decision D3: the model never holds the Guidewire write, and submission is a code endpoint the customer triggers.

## 6. The exact next prompt the skills told the user to type

The plan's "Resume here" section, built from `assets/implementation-plan-template.md:121-129`, gives this prompt for the next ready goal:

```text
/adk-engineer Carry out G04 Walking skeleton from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its accepted decisions.
Use adk-workflow-design with adk-release-engineering and adk-agent-instructions.
Work within local code and offline tests, verify the G04 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

The skill's own generic form (`SKILL.md:276-278`) is:
`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`
