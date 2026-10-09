# REPORT: Card Dispute Assistant design session

Date: 2026-10-09. Mode: headless, user unavailable, design only.

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (via `/adk-system-designer`). No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (its trigger applies: concurrent sessions, capacity, release continuity)
7. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
10. `.claude/skills/adk-system-designer/assets/ticket-template.md` (read; no tickets written because the user didn't ask for them)
11. `.claude/skills/adk-system-designer/agents/openai.yaml` (read alongside the templates; not relevant)
12. Outside the project, read only: `…/agentic-engineering-skills/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
    (SKILL.md:193-197 says to choose model IDs from it, but this project's `.claude/skills/` doesn't contain it)
13. Outside the project, read only, grep excerpts: each specialist's `references/compatibility.md` in the same source tree, to find the ADK version (2.8.0) per SKILL.md:189-192

## 2. Questions I would have asked, and the answers I assumed

These are the same as the design's **Assumed answers** table (A1–A14) and open decisions (O1–O10).

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Channel? | Chat panel in the existing authenticated mobile and web banking app, behind the bank's API gateway |
| A2 | Authentication and token? | Bank OIDC IdP with PSD2 SCA. Gateway forwards a signed token mapping to one customer ID. |
| A3 | Core-banking dispute API: idempotency, lookup, sandbox? | A create-case API exists with a client reference. Its dedup and lookup semantics are unknown. A test environment exists. (Discovery goal G00) |
| A4 | Who decides eligibility, liability, provisional credit? | Back office and core-banking rules. The assistant only opens a complete, categorised case. |
| A5 | Dispute types in scope? | Card debit and credit, last 13 months. Six categories. No ATM, SEPA or business cards. |
| A6 | Languages at GA? | One (the bank's primary language). The second comes in phase 2. |
| A7 | Evidence uploads at GA? | No. Phase 2, behind a quarantined reader. |
| A8 | Volume? | ~5,000 conversations/month, ~30 concurrent at peak (illustrative) |
| A9 | Cloud footprint, region? | Existing GCP org with VPC-SC, Interconnect, approved EU region, platform-team Terraform |
| A10 | Retention? | Sessions 90 days. The confirmed summary goes with the case under the records policy. DPO to confirm. |
| A11 | Team familiarity and focus? | Experienced Python/GCP, new to ADK, one frontend engineer among the six, focus 0.6, security reviewer ~25% |
| A12 | Model and cloud budget? | Not given. The product owner sets a ceiling before the pilot. |
| A13 | Compliance gates? | DPIA, model-risk sign-off, AI Act Art. 50 transparency, DORA register, external pentest |
| A14 | Human handoff? | Always available, to the existing secure-messaging or contact-centre queue |
| O1–O10 | Gateway claims; core-banking contract; EU model availability, quotas and retention terms; hosting mandate (Cloud Run vs bank GKE); retention values; screening fail-open vs fail-closed; baselines and SLO targets; languages; same-family judge acceptability; spend ceiling | Provisional defaults are in the design. Each lists its owner and the goal it blocks. |

I also assumed a start date of 2026-10-12, which puts GA around 2027-02-08.

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/card-dispute-assistant.md`: the design, marked **draft**. It contains the assumed-answers table, journey, profile and depth table, floor, capacity and cut line, invariants I1–I8 and targets T1–T3, component and sequence diagrams (Mermaid), decisions D1–D14, model-facing contracts, data and authority, security posture, budgets, failure and recovery table, verification ladder, and open decisions O1–O10.
- `docs/plans/card-dispute-assistant.md`: the plan, marked **draft**. It has phase 1 goals G00–G15 with every template field filled, coarse phase 2 goals G16–G18, a Later table and the Resume block.
- `REPORT.md`: this file.

Not finished or not done:

- No decision was accepted by the user, so the whole design is provisional.
- The cut line was not confirmed by the user.
- No tickets were written under `docs/tickets/`, because they weren't requested.
- No provider facts were verified, because network access was forbidden. EU-region availability of `gemini-3.8-flash`, quotas, prices, Model Armor/SDP availability and Vertex data-retention terms are all open (G01). No URLs are cited with fresh access dates.
- Regulatory references (PSD2, GDPR Art. 35/17, AI Act Art. 50, DORA) are named from general knowledge, not cited sources, and need the bank's compliance review.
- No code, scaffolding or dependency changes were made, as instructed.

## 4. Checks run and checks not run

Run (local, `python3 -I` script):

- Relative Markdown links between the design and the plan resolve: 4/4 OK.
- Each of G00–G15 has all 12 template fields (Phase and estimate, Outcome, Scope, Depth, Prerequisites, Primary skill, Supporting skills, Acceptance, Verification, Execution scope, Status and evidence, Run this goal): none missing.
- Phase 1 estimate sum from the goals table: low 1,440 h, high 2,184 h (the docs say "2,180", rounded). Capacity 6 × 17 × 40 × 0.6 = 2,448 h, or 1,836 h after a 25% reserve. The mid estimate (~1,812 h) fits. The high end does not, which is why the plan states a cut order.

Not run:

- Any test that imports `google.adk`. The project has no code, and ADK is not installed (not run, as the rules require).
- Any ADK interface verification against a pin. This is deferred to G02's first acceptance item.
- Any network, cloud, model, quota or pricing lookup (forbidden this session).
- Mermaid rendering of the two diagrams (no renderer available; syntax not validated).

## 5. Friction log

**Unsure what to do**

- `.claude/skills/adk-system-designer/SKILL.md:193-197` says to pick model and judge IDs from `adk-model-and-output-contracts`' `assets/model-lifecycle-*.json`. That specialist isn't in this project's `.claude/skills/` (only the designer is), and it isn't in `~/.claude/skills` either. I found it in the user's skills source tree and read it there. `references/implementation-handoff.md:52-53` says "a missing skill is a setup prerequisite". It's unclear whether reading a sibling checkout counts as "available". Several primary skills named in the plan (`adk-agent-security`, `adk-agent-instructions`, `adk-tool-interface-design`, `adk-release-engineering`, `adk-agent-observability`) also aren't installed locally. They do appear in the session's skill list, so I treated them as available.
- `SKILL.md:79` ("Record the answers at the top of the design document") and `SKILL.md:117-120` ("put an **Assumed answers** table at the top") both want the top slot. The template's "Delivery constraints" table (`assets/system-design-template.md:12-21`) holds the same answers again. I put Assumed answers first and the scope-gate table under Delivery constraints. This means some overlap.
- `references/delivery-profiles.md:101-103` gives focus factors for "part-time or interrupted" (0.6) and a "single afternoon" (0.8), but nothing for a full-time team over four months with meetings and approvals. I chose 0.6 and labelled it.
- `SKILL.md:86-90` says to ask the user to confirm the cut line. In a headless run, the only option was to state it as provisional. `SKILL.md:117-120` covers questions, not this confirmation step.
- `assets/implementation-plan-template.md:84-95` ("What the reviewer reads … At most three documents … raw run records") reads as aimed at quality-judged assignments. For a production plan I kept it short and pointed to a future `evals/README.md`.
- In the 343-line `references/design-decisions.md`, it was hard to tell which sections were "relevant to the journey". I used almost all of them, because a regulated write path touches nearly every section.

**Heavier than needed**

- `SKILL.md:93-95` ("Every design reads design decisions … and failure review") plus four more references and three templates add up to about 1,500 lines of guidance before writing anything. For a production design this is justified. The ticket template and `agents/openai.yaml` weren't needed.
- The plan template asks for 12 fields for every goal (`assets/implementation-plan-template.md:48-69`). With 16 phase-1 goals, the plan becomes long and repetitive. The run prompt is the same for every goal except the ID.

**Genuinely helpful**

- `references/delivery-profiles.md:70-89` (the floor) and `:95-113` (capacity, reserve, cut order) gave a concrete method for the capacity check and the "cut scope, not the floor" order.
- `references/design-decisions.md:182-196` (lethal-trifecta check) led directly to the key security decision: the model has no submit tool, and submission is code behind a hash-bound confirmation.
- `references/design-decisions.md:228-259` (operation identity, uncertain writes, "a later rejected attempt cannot prove an earlier attempt had no effect") shaped D6/D7 and the G00 discovery goal.
- `references/failure-review.md:23-43` (scenario table) made the failure and recovery table quick to fill and fairly complete.
- `SKILL.md:189-197` (record the ADK version from compatibility.md, pick models from the dated lifecycle table) prevented choosing `gemini-3.7-flash`, whose Vertex retirement (2027-01-28) falls before GA. It also surfaced that `FallbackModel` is absent in ADK 2.8.0, which led to D8 (static-form fallback).

## 6. The exact next prompt the skills told the user to type

The skill (`SKILL.md:271-276`) says to end with the prompt for the next ready goal. Following the plan template's Resume block (`assets/implementation-plan-template.md:111-119`), the prompt given is:

```text
/adk-engineer Carry out G02 (walking skeleton with scoped transaction lookup) from docs/plans/card-dispute-assistant.md.
Read docs/architecture/card-dispute-assistant.md and preserve its accepted decisions.
Use adk-tool-auth-and-secrets with adk-workflow-design and adk-tool-interface-design.
Work locally with a fake core-banking adapter and a test token issuer, verify the
cross-customer denial, session-ownership and restart acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

The skill's own literal example (`SKILL.md:274`) is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`. In this plan G01 is a discovery goal that needs the platform team, so the prompt names G02, the first goal that can run locally without outside help.
