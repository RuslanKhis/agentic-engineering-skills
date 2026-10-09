# Report: card-dispute ADK agent, design session

This session produced a design and an implementation plan only. Nothing was
implemented, no cloud resources were touched, and nothing was installed.

## 1. Skills invoked and reference files opened, in order

**Skills invoked:**

1. `adk-system-designer`. The user invoked it with the `/adk-system-designer`
   slash command. No other skill was invoked through the Skill tool.

**Files opened, in order** (all paths under `.claude/skills/`):

1. `adk-system-designer/references/design-decisions.md`, read in full.
2. `adk-system-designer/references/failure-review.md`, read in full.
3. `adk-system-designer/references/gcp-decisions.md`, read in full.
4. `adk-system-designer/references/implementation-handoff.md`, read in full.
5. `adk-system-designer/references/runtime-and-delivery.md`, read in full.
   Its trigger applies here: concurrent sessions, browser delivery and
   release continuity.
6. `adk-system-designer/assets/system-design-template.md`
7. `adk-system-designer/assets/implementation-plan-template.md`
8. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`,
   read in full. SKILL.md:169 requires it for the model choice.
9. `*/references/compatibility.md` for all 17 specialists. I only grepped the
   version lines to find the ADK pin. All 17 say `google-adk` 2.8.0, and
   several note that upstream is at 2.11.0.

**Files not opened:** `assets/ticket-template.md` (the user did not ask for
tickets) and `agents/openai.yaml`.

## 2. Questions I would have asked, and the answers I assumed

The design's **Assumed answers** table records each of these with the
decisions that depend on it, in `docs/architecture/card-dispute-agent.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | How much time and money is there? | 6 engineers + 1 security reviewer, about 17 weeks to GA (early February 2027). No fixed cloud budget. Non-production model spend is capped in the application. |
| Q2 | Who judges the result, and what do they read? | The security reviewer, Compliance/DPO, Model Risk Management and the disputes ops lead. They read the design, threat model, eval report and pilot metrics. Customers then use the running service. |
| Q3 | What kind of artifact is this? | A production service, with a staff and limited-customer pilot before GA. |
| Q4 | Which channels? | Authenticated web and mobile banking only, using the existing OIDC identity provider and app shell. |
| Q5 | Which languages? | English plus one local language (German as a placeholder). |
| Q6 | What may the agent change? | It may open a dispute case for the customer's own transaction after confirmation. No refunds, card blocks or promises of an outcome. |
| Q7 | How is the core banking dispute API reached, and does it support idempotency? | An internal REST API over private connectivity with mTLS. Whether it supports idempotency or lookup is **unknown** (D-02). |
| Q8 | Is the bank on GCP, and what is its platform standard? | It has an EU landing zone with a location org policy. Cloud Run is approved. |
| Q9 | Is step-up authentication required at confirmation? | Yes, using the existing in-app step-up. |
| Q10 | Are evidence uploads allowed? | Yes. They are stored and attached to the case, and the model never reads them in v1. |
| Q11 | What is the transcript retention period? | 90 days. The case and operation records follow the bank's own schedule. |
| Q12 | What volume do we expect? | About 20,000 conversations a month, with 10x bursts. This is illustrative. |
| Q13 | What is the baseline, and what outcome should improve? | Follow-up contacts on filed disputes. The baseline is unknown and will be measured in D-03. |
| Q14 | Which model hosting is acceptable? | Vertex AI in an EU region only, under the existing Google contract and DPA. |
| Q15 | Who owns the dispute rules? | Disputes ops + Compliance, who supply a versioned rule table. |

The design also records seven open decisions (D-01 to D-07) that need evidence
from other teams rather than from the user.

## 3. Files written or changed, and what was not finished

**Files written:**

- `docs/architecture/card-dispute-agent.md`, the design.
  - Status is **draft**: every decision is proposed and none is
    user-accepted.
  - It contains the assumed answers, scope gate, deferred controls,
    invariants I1–I8 and targets T1–T3, a component diagram and sequence, the
    decision record DD-01 to DD-10, the model-facing contracts, the data and
    authority table, the security posture, budgets, the failure table,
    verification and open decisions.
- `docs/plans/card-dispute-agent.md`, the plan.
  - It contains the implementation map, a goal table, a 17-week schedule,
    full goal blocks for G01, G02, G04, G05 and G08, three discovery goals,
    coarse later goals and a resume section.
- `REPORT.md`, this file.

No other files were changed.

**Not finished:**

- **Provider facts are unverified.** No network access was allowed, so these
  are all unconfirmed:
  - availability of `gemini-3.8-flash` on Vertex in the EU,
  - SDP and Model Armor regions,
  - quotas,
  - prices.
  
  The cost estimate is therefore symbolic only. Discovery goal D-01 carries
  these lookups.
- **The core API replay contract is unknown** (D-02). Invariant I3 is designed
  but not yet backed by a provider guarantee.
- **G03, G06, G07 and G09–G13 are coarse.** They have no full goal blocks yet.
- **No ticket files.** The user did not ask for them.
- **The regulatory mapping is an assumption** that needs Compliance
  confirmation. It is not legal advice.
- **Nothing was implemented,** as the user requested.

## 4. Checks

**Run:**

- **Relative-link check** on both documents, using a local Python script
  (`python3 -I`, no third-party imports): 2 of 2 links resolve.
- **Markdown table column-count consistency** on both documents: 0 issues.
- **Model IDs checked by hand against the lifecycle JSON:**
  - `gemini-3.8-flash` is stable with no shutdown date (line 12).
  - `gemini-3.7-flash` has a Vertex retirement date of 2027-01-28 (line 13),
    so I rejected it because it retires before GA.
  - `gemini-3.6-flash` has a Vertex retirement date of 2026-11-19 (line 14).
- **ADK pin grep** across the specialists' `compatibility.md` files: all say
  2.8.0.

**Not run:**

- **Any ADK or Python application tests.** None exist, and `google-adk` is not
  installed. Every acceptance case in the plan is planned, not executed.
- **Official documentation lookups** for regions, prices, quotas and the ADK
  2.11.0 changelog. Network access was prohibited.
- **Markdown linting.** No linter is installed, and installing one is
  prohibited.

## 5. Friction log

**Moments I was unsure what to do:**

- **Asking versus a headless run.** `adk-system-designer/SKILL.md:50` says to
  let the user answer before treating a material product choice as settled.
  That conflicts with a headless run. `SKILL.md:93-96` resolves it with the
  "Assumed answers" table, and that worked well. The two passages are about
  45 lines apart, so I only found the resolution on a second read.
- **Scope-gate defaults.** `SKILL.md:56-60` defaults the judge to "the user,
  reading the design" and the artifact type to "exploration". The request
  clearly said production but said nothing about the judge or the money. The
  defaults did not fit, so I wrote my own assumptions instead.
- **Proportionality for a production service.**
  `references/design-decisions.md:37-44` applies the proportionality rule only
  to artifacts judged on output quality. For production it is unclear whether
  the rule affects anything. I used it only to order work (measure
  classification early, G03), not to drop controls.
- **Owner for a deterministic rules engine.** No row in
  `references/implementation-handoff.md:19-37` covers ordinary-code business
  rules such as eligibility. I assigned G02 to `adk-model-and-output-contracts`
  as the nearest fit, but this is a guess.
- **Primary skill on discovery goals.** `SKILL.md:234` requires a
  `Primary skill` line on every goal. That is awkward for discovery goals that
  are mostly human or other-team work (D-02, D-03), but I filled it anyway.
- **"Fill every field" versus "leave goals coarse".**
  `assets/implementation-plan-template.md:56-57` says to fill every field with
  real values. Lines 31-32 say to leave dependent goals coarse. I used full
  blocks for ready goals and one line each for blocked ones.
- **Missing Vertex retirement for gemini-3.8-flash.**
  `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12`
  has no `vertex_retirement` field. It is unclear whether that means "none
  announced" or "not captured". The design treats it as unknown and routes it
  to D-01. The table also has no region information, which matters for EU
  residency.

**Heavier than needed:**

- **Finding the ADK version.** `SKILL.md:167` points to "each specialist's
  `references/compatibility.md`". That means 17 files that all say 2.8.0. A
  single shared pin note would save the sweep.
- **Document length.** `SKILL.md:66` ("as long as its decisions require, with
  every template section either filled or marked not applicable") is
  open-ended. The design came out at about 5,500 words, which is justified for
  a regulated write path but slow to review.

**Genuinely helpful:**

- **Lethal-trifecta check.** `references/design-decisions.md:180-194` led to
  the two most important structural decisions:
  - the filing is not a model tool (DD-02),
  - the model does not read uploaded evidence (Q10).
  
  It also prompted me to treat merchant descriptors as untrusted content.
- **External effects and recovery.**
  `references/design-decisions.md:226-247` (the operation identity and
  "a later rejected attempt cannot prove...") shaped the `UNCERTAIN` state and
  the reconciler, and the rule never to re-dispatch.
- **Failure scenarios.** The scenario table in
  `references/failure-review.md:23-43` mapped almost one-to-one onto the
  design's failure table.
- **Model lifecycle table.** In the lifecycle JSON, lines 13-14 caught that
  `gemini-3.7-flash` retires on Vertex just before the planned GA. From memory
  I would probably have picked it.
- **Supporting-skill rules.** `references/implementation-handoff.md:39-51`
  made supporting-skill selection mechanical.

## 6. Next prompt the skills told the user to type

The skill's own example at `adk-system-designer/SKILL.md:246`, verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated for this plan:

```text
/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md.
```

The plan's "Resume here" section also has a fuller continuation prompt, built
from `assets/implementation-plan-template.md:89-95`.
