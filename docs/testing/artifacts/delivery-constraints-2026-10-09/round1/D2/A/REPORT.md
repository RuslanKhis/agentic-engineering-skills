# REPORT — ADK expense assistant design session (2026-10-09)

Skill paths below are relative to `.claude/skills/`.

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (slash command, by the user). No other skill was invoked.
2. Listed project files; the repo is empty apart from `.claude/skills`, so this is a greenfield design.
3. `adk-system-designer/references/design-decisions.md` (full)
4. `adk-system-designer/references/failure-review.md` (full)
5. `adk-system-designer/references/implementation-handoff.md` (full)
6. `adk-system-designer/references/gcp-decisions.md` (full)
7. `adk-system-designer/assets/system-design-template.md` (full)
8. `adk-system-designer/assets/implementation-plan-template.md` (full)
9. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
10. Grepped every `*/references/compatibility.md` for the ADK version. All of them name 2.8.0, except deploy, which also mentions 2.2.0 for Runtime.
11. `adk-sql-agent-engineering/SKILL.md` lines 1–40, to check whether it covers PostgreSQL. It is oriented to BigQuery.
12. `adk-system-designer/references/runtime-and-delivery.md` lines 1–25 only, for the same-conversation overlap policy.
13. `adk-model-and-output-contracts/references/compatibility.md` lines 1–30, to confirm the default model and schema-with-tools behaviour in 2.8.0.

Not opened: `assets/ticket-template.md`, because no tickets were requested. I also did not open any specialist SKILL.md beyond the SQL one.

## 2. Questions I would have asked, with the answers I assumed

The design records the same list in its **Assumed answers** table.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Is ~15 engineer-days the whole budget? Is there a cloud or model spend limit? | Yes. No hard spend cap, but pilot running cost should be small (illustrative: tens of USD/month). |
| A2 | Who judges the result, and what will they read? | The finance team lead, using a running service plus a one-page evaluation summary. |
| A3 | What kind of artifact is this? | A pilot that might later become a production service. |
| A4 | Should users see only claims where they are the claimant? Do finance staff need other employees' claims, for example as approvers? | Own claims only. No approver or on-behalf access. |
| A5 | Read-only, or can it submit, edit or approve claims? | Read-only. |
| A6 | Where does the PostgreSQL database run? Can we get a read-only role? | Cloud SQL in the company's GCP organisation. The DBA can create a read-only role on a view. |
| A7 | How does a Workspace identity map to an employee row? | A unique work-email column in an `employees` table. |
| A8 | Where are the policies, how big are they, who owns them, and how often do they change? | A few documents, ≲ 30 pages (~20k tokens), owned by the finance lead, changed a few times a year. |
| A9 | Any data-residency or vendor constraints? | Vertex AI Gemini in one org-chosen region is acceptable. |
| A10 | Which UI: web page, Google Chat or Gemini Enterprise? | A minimal internal web page. |
| A11 | How long may conversations that contain claim data be kept? | 30 days. |
| A12 | What does "good" mean for policy answers, and is there a baseline? | Cited answers scored on a labelled set written by the finance lead. Baseline: policy emails to the finance inbox, to be counted. |

## 3. Files written or changed, and what was not finished

Written:
- `docs/architecture/expense-assistant.md`: draft system design. It covers the assumed answers, scope gate, deferred controls, invariants I1–I7, decisions D1–D9, model-facing contracts, data and authority, security posture, budgets, failure table, verification and open decisions.
- `docs/plans/expense-assistant.md`: implementation plan. It has two discovery goals (Q1 DB access, Q2 identity mapping) and five goals. G01 and G02 are ready and detailed. G03–G05 are coarse; G04 is blocked on cloud authorisation.
- `REPORT.md` (this file).

No other files were changed. No code was written: the request was design-only.

Not finished or still provisional:
- No prices, region availability, IAP or Cloud SQL facts were looked up, because network access was not allowed. The cost estimate is symbolic.
- The ADK 2.8.0 interfaces are an assumption. Confirming them is G01 acceptance item 1.
- All decisions are provisional on A1–A12. The user has not reviewed any of them.
- The design runs to ~3,750 words, longer than the skill's "two to four pages" for a pilot. Its tables are dense, but it was not trimmed.

## 4. Checks run and not run

Run, all local with `python3 -I` and no network:
- **Relative links** in both docs: 3 of 3 resolve.
- **Model IDs** against `model-lifecycle-2026-10-01.json`: `gemini-3.5-flash` is stable, with Vertex retirement "2027-05-19 or later". `gemini-3.8-flash` is stable but has no Vertex retirement field. `gemini-3.6-flash` has Vertex retirement 2026-11-19, so I avoided it. The design's statements match the table.
- **Word counts:** design 3,755 words, plan 1,762 words.
- **Run prompts:** G01–G03 each have a "Run this goal" prompt, and the plan has a "Resume here" block.

Not run:
- Any test importing `google.adk`. There is no code, and the dependencies are not installed.
- The bundled `audit_model_config.py` and `check_response_schema.py`. There is no project code or schema for them to check.
- Any cloud, IAM, Vertex, network or package-install command, which the session rules forbid.
- A freshness check on the lifecycle table. The table itself says to refresh it from Google's pages before relying on it, which requires the network.

## 5. Friction log

**Unsure what to do:**
- `adk-system-designer/SKILL.md:52-60` and `:92-96` (scope gate vs headless run). It was clear I should ask nothing and add an Assumed answers table. It was less clear whether the three scope-gate questions also belong in that table or only in the scope block. I put them in both: rows A1–A3 and the scope table.
- `adk-system-designer/SKILL.md:65` ("a pilot, roughly two to four pages"). There is no word or line budget, and the design template (`assets/system-design-template.md`) has ten sections, several of them tables. Filling every section relevant to a pilot pushed me past four pages. I could not tell whether to drop template sections or compress them.
- `adk-system-designer/SKILL.md:152-154` (runtime-and-delivery trigger includes "concurrent sessions, capacity"). Nearly every web app has concurrent sessions, so the trigger technically fired. I read only the first section and applied a single overlap rule (409 on a second in-flight turn).
- `adk-system-designer/SKILL.md:163-168` (record the ADK version from the specialists' compatibility files). The files mostly agree on 2.8.0. `deploy-adk-on-google-cloud/references/compatibility.md:34` also mentions 2.2.0 for Runtime, and `adk-agent-observability/references/compatibility.md:40` mentions 2.10.0+. I chose 2.8.0, but the skill gives no rule for resolving a disagreement.
- `adk-system-designer/references/implementation-handoff.md:34` maps "governed analytical answers" to `adk-sql-agent-engineering`. That skill's description is BigQuery and analytics oriented (`adk-sql-agent-engineering/SKILL.md:3`). A fixed-query, own-rows Postgres lookup fits it poorly, so I made it a supporting skill and gave the G02 lead to `adk-tool-auth-and-secrets`. Picking a primary skill for "scoped read of a business database by a tool" was a judgment call.
- `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` has no `vertex_retirement` for `gemini-3.8-flash`. I could not tell whether that means "no date" or "not captured", so I chose the older model, which has a known date.

**Heavier than needed:**
- `adk-system-designer/assets/system-design-template.md:109-118` (observability and release bullets) and `:103-107` (the "deliverable regenerated by the method" rule). Both are oriented to production or to graded assignments. For a 40-user read-only pilot, the release-bundle line and the outcome-hypothesis line added little.
- `adk-system-designer/references/design-decisions.md:226-257` (external effects and recovery). The section is long, but the product is read-only. `failure-review.md:5` explicitly says not to invent write machinery, which helped me skip it quickly.

**Genuinely helpful:**
- `adk-system-designer/references/design-decisions.md:180-194` (lethal-trifecta check). It surfaced that employee-typed claim descriptions are untrusted content. That led to the "scope fixed in code, no egress, no image rendering" posture and to adversarial cases in G02.
- `adk-system-designer/references/design-decisions.md:113-121` ("what the model sees is its only interface"). It directly produced the rule that tools take no employee parameter, which is invariant I1's mechanism.
- `adk-system-designer/references/design-decisions.md:150-152` plus `:338-341` (no matches vs unavailable). This became invariant I5: never say "no claims" when the database is down.
- `adk-system-designer/SKILL.md:169-173` together with the lifecycle JSON. Picking the model from a dated table steered me away from `gemini-3.6-flash`, whose Vertex retirement of 2026-11-19 falls inside a plausible pilot window.
- `adk-system-designer/references/implementation-handoff.md:39-51` (supporting-skill selection rules). These made the Primary and Supporting lines for each goal mechanical.
- `adk-system-designer/assets/implementation-plan-template.md:82-98` ("Resume here" block). It made the handoff prompt unambiguous.

## 6. Exact next prompt the skills told the user to type

The skill (`adk-system-designer/SKILL.md:241-249`) says to end with the prompt for the next ready goal, and gives this form as its example:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Filled in for this plan, as written in the plan's "Resume here" block:

```text
/adk-engineer Carry out G01 — Cited policy answers, measured from docs/plans/expense-assistant.md.
Read docs/architecture/expense-assistant.md and preserve its accepted decisions.
Use adk-agent-instructions with adk-agent-evaluation and adk-model-and-output-contracts.
Work within local code and, only if authorised, a capped Vertex run in a dev project; verify
G01's acceptance cases, and update the plan with actual evidence and remaining blockers.
```
