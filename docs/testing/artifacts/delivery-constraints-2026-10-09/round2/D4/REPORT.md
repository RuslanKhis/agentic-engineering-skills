# REPORT: card dispute assistant design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`). Its SKILL.md was loaded.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
10. `.claude/skills/adk-system-designer/assets/ticket-template.md` (read; not used, because no tickets were requested)
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (model IDs and retirement dates)
12. A `grep` across `.claude/skills/*/references/compatibility.md` for the ADK version baseline. Matching lines were read from: adk-observability, adk-model-and-output-contracts, adk-release-engineering, adk-agent-security, adk-operational-guardrails, adk-sql-agent-engineering, adk-frontend-integration, adk-memory-architecture, adk-agent-interoperability, adk-agent-evaluation and adk-tool-interface-design. These were excerpts, not full reads.

No other skill was invoked. Specialist skills are named in the plan as owners of each goal but were not loaded, because this was a design-only request.

## 2. Questions I would have asked, and the answers I assumed

The canonical list, with the decisions each answer affects, is the
**Assumed answers** table at the top of `docs/architecture/card-dispute-agent.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | GA date, and what happens after it? | About 2027-02-08. The service is then operated and extended |
| A2 | People, hours, ADK/GCP familiarity, who runs it? | 6 full-time engineers (~16 working weeks), who know GCP and are new to ADK. The security reviewer gives ~0.25 FTE. Bank SRE runs it. The existing app team builds the screens and is not counted in the six |
| A3 | Model and cloud budget? | Illustrative: €15k/month production, €5k/month non-production |
| A4 | Users and judges? | Retail cardholders in the existing authenticated app. Compliance, Security, Dispute Ops and Model Risk judge it |
| A5 | Data and effects? | Regulated personal and payment data. The effect is creating dispute cases in core banking; no money is moved by the agent |
| A6 | Dispute types at GA? | Merchant disputes only. Unauthorised/fraud claims go to the existing fraud journey |
| A7 | Core dispute API: idempotency and lookup? | REST behind the integration gateway, with a sandbox and lookup by transaction. Idempotency is unknown, so it became a discovery goal (G00) |
| A8 | GCP landing zone? | EU, VPC-SC, CMEK, Interconnect; Cloud Run and Cloud SQL allowed |
| A9 | Existing fallbacks? | A classic dispute form and live chat with a transfer API |
| A10 | Languages? | One at GA; a second in phase 2 |
| A11 | Volume, latency, availability? | 3,000 conversations/day peak, ~10 turns each. p95 ≤ 8 s, 99.5% |
| A12 | Retention? | Sessions 90 days; dispute records per bank policy; the DPO confirms |
| A13 | AI Act / DORA classification? | Transparency obligation only, not high-risk. Google is already in the DORA register. Compliance confirms |
| A14 | EU model processing? | Regional EU Vertex AI endpoint under the existing contract. Unverified (V1, V2) |
| — | Is the cut line acceptable (phase 1 fits only at low/mid estimate; contingency cuts C1–C4)? | Assumed acceptable; flagged for the user to confirm |
| — | Streaming vs complete replies? | Complete-reply JSON, so output can be screened before release |
| — | Hosting mandate (Cloud Run vs a GKE platform)? | Cloud Run |

## 3. Files written or changed, and what was not finished

Written (no existing files were changed):

- `docs/architecture/card-dispute-agent.md` is the system design, status
  **draft**. It contains the assumed answers, journey, profile, depth table,
  deferred controls, capacity and cut line, invariants I1–I10 and T1,
  decisions D1–D12, provider facts to verify V1–V6, model-facing contracts,
  data and authority, security posture, budgets, failure table, verification
  ladder and open decisions.
- `docs/plans/card-dispute-agent.md` is the implementation plan. It covers
  phases, capacity, contingency cuts, parallel streams, regulatory milestones,
  the implementation map, goals G00–G13 (full fields and run prompts) and
  G14–G20 (coarser), the later list and the resume prompt.
- `REPORT.md` is this file.

Not finished:

- No decision is user-accepted. Everything is provisional on A1–A14.
- Provider facts V1–V6 (model regional availability and retirement, data
  terms, VPC-SC/CMEK support, the `DatabaseSessionService` contract at the
  pin, the core API contract, SDP regionality) were not verified, because
  network lookups were not allowed. No URLs or access dates are cited for
  them.
- The cost estimate is symbolic. No prices were looked up.
- Regulatory statements (PSD2 unauthorised-transaction handling, AI Act
  transparency, DORA) are assumptions for Compliance to confirm. They are not
  legal analysis.
- No tickets were written under `docs/tickets/`, because tickets were not
  requested.
- No application code, as instructed.

## 4. Checks run, and checks not run

Run:

- A Python script (`python3 -I`) summed the goal estimates from the plan's
  goal table. Phase 1 has 14 goals totalling 1,440–2,180 h, matching the
  stated figures. Phase 2 has 7 goals totalling 700–1,120 h. That check found
  a mismatch in the phase table ("700 to 1,100"), which was **corrected** to
  1,120.
- The same script counted 14 detailed goal sections, each with a
  `Run this goal` prompt.
- Relative Markdown links between the design and the plan all resolve
  (3 of 3).
- Word counts: design about 6,200 words, plan about 4,900 words. This is
  consistent with the production profile ("as long as its decisions
  require").
- A manual correction while drafting: a wrong symbolic monthly cost formula
  in the design was fixed.

Not run:

- Any test importing `google.adk`. ADK is not installed and nothing was
  implemented, so there are no tests to run. **Not run.**
- No network, cloud, model or package-install commands, per the session
  rules.
- No Markdown or mermaid renderer or linter was run. The diagrams are
  unrendered.
- No review by the user, Security, Compliance or Dispute Ops.

## 5. Friction log

| # | Kind | Moment | Pointer |
| --- | --- | --- | --- |
| 1 | Helpful | The headless case is handled directly: "When the user cannot answer … put an **Assumed answers** table at the top." This removed any doubt about whether to stop and ask | `.claude/skills/adk-system-designer/SKILL.md:119-122` |
| 2 | Unsure | The skill says "Show the user the cut line … and ask them to confirm" and "Let the user answer before treating a material product choice as settled". With no user available, I put the confirmation request in the plan as text and marked everything provisional. Point 1 covers questions, but not explicitly the cut-line confirmation | `SKILL.md:91-92`, `SKILL.md:119-122` |
| 3 | Unsure | The focus factor only covers "part-time or interrupted (0.6)" and "a dedicated block such as a single afternoon (0.8)". There is no guidance for a dedicated team over months with regulated-bank overhead. I chose 0.65 | `.claude/skills/adk-system-designer/references/delivery-profiles.md:104-106` |
| 4 | Helpful | "If only the low end fits, say so and name the goals that move to phase 2" gave a clean pattern for the contingency cuts C1–C4. The worked example of six engineers and four months matches this exact request | `delivery-profiles.md:112-121`, `delivery-profiles.md:5-6` |
| 5 | Unsure | The capacity rules have no slot for calendar-bound external lead times (DPIA, pen test, model-risk sign-off), which are the real critical path for a regulated GA. I added a "Regulatory milestones" table to the plan myself | `delivery-profiles.md:98-121`; `assets/implementation-plan-template.md:16-28` |
| 6 | Unsure | The lifecycle JSON gives `gemini-3.8-flash` no `vertex_retirement` key, while older models have one. It is unclear whether this means "no date announced" or "not on Vertex / not checked". The design depends on Vertex EU, so I recorded it as V1 | `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12` |
| 7 | Helpful | The instruction to pick models from the lifecycle table, and to treat "a model that retires within the plan's horizon" as a designed-in migration, directly ruled out 3.6/3.7-flash (Vertex retirement before or near GA) | `SKILL.md:195-198` |
| 8 | Helpful | The instruction to record the specialists' ADK baseline (2.8.0) and make pin confirmation a G01 acceptance item resolved the "no installed version" problem | `SKILL.md:190-194` |
| 9 | Unsure | "Check service availability, regions, limits and prices … cite sources and dates", but network is forbidden. The fallback ("keep those decisions provisional and name the exact verification") worked. The GCP starting-point URLs could not be opened | `SKILL.md:199-202`; `references/gcp-decisions.md:35-50` |
| 10 | Heavier than needed | The design template's "Name the deliverable the evaluator will judge … regenerated" paragraph is aimed at assignments. For production it reads oddly, and the template asks every section to be filled or marked not applicable | `assets/system-design-template.md:123-127`; `SKILL.md:85-86` |
| 11 | Heavier than needed | `design-decisions.md` (343 lines) is mandatory reading for every design, and its analytical-questions section did not apply. For production this was fine; the length is noted | `SKILL.md:95-96`; `references/design-decisions.md:327-343` |
| 12 | Unsure | There are two forms of the next-step prompt: the short one in SKILL.md (`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`) and the longer multi-line "Continuation prompt" in the plan template. I used the long form in the plan's Resume section and the per-goal one-line form in each goal | `SKILL.md:273-277`; `assets/implementation-plan-template.md:67-69,111-119` |
| 13 | Helpful | The trifecta check, plus "tier tools … gate irreversible ones with confirmation in code the model cannot reach", led directly to D2 (no submit tool for the model) | `references/design-decisions.md:182-196` |
| 14 | Helpful | The supporting-skill selection rules ("the first goal that reaches a shared environment gets observability and release-engineering") made the `Supporting skills` lines mechanical | `references/implementation-handoff.md:39-51` |
| 15 | Unsure | Which runtime-and-delivery triggers apply was a judgment call. I read it because of concurrent sessions and release continuity. It yielded D8 (per-session turn lock) and D11 (complete-reply JSON) | `SKILL.md:178-181` |
| 16 | Unsure | The skill text says domain constraints come "from the user, a cited source or a labelled assumption". No skill covers EU banking regulation (PSD2, AI Act, DORA), so all of it is labelled as assumptions for Compliance to confirm | `SKILL.md:115-117` |

## 6. The exact next prompt the skills told the user to type

The skill instructs (`SKILL.md:270-277`) that the closing message gives the
next ready goal's prompt in a copyable block, in the form
`/adk-engineer Carry out G01 from docs/plans/<topic>.md.` Filled in for this
plan:

```text
/adk-engineer Carry out G01 from docs/plans/card-dispute-agent.md.
```

The plan's "Resume here" section gives the longer template form:

```text
/adk-engineer Carry out G01 (Pinned skeleton with scripted-model tests) from docs/plans/card-dispute-agent.md.
Read docs/architecture/card-dispute-agent.md and preserve its accepted decisions.
Use adk-workflow-design with adk-release-engineering and adk-agent-evaluation.
Work within local files only, verify the offline scripted-model test and the recorded ADK pin confirmation, and update
the plan with actual evidence and remaining blockers.
```
