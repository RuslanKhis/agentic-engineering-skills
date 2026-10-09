# REPORT: IT helpdesk ADK assistant (design only)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`.
   The SKILL.md was loaded with the invocation.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/assets/system-design-template.md`
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-system-designer/assets/ticket-template.md`
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`.
    SKILL.md:199 directs model IDs to come from this table.
11. A grep, not a full read, of `compatibility.md` in `adk-workflow-design`,
    `adk-memory-architecture` and `safe-api-tool-calls`, and of the
    `adk-tool-auth-and-secrets/references/` files. Its purpose was to find the
    ADK version pin (2.8.0) and the `adk web` identity caveat
    (`adk-tool-auth-and-secrets/references/identity-and-output.md:9`).

I did **not** open `references/runtime-and-delivery.md`. Its trigger
(SKILL.md:180) covers context limits, downloads, browser streams, concurrent
sessions and release continuity, and none of these is material for 25
internal users in phase 1. No other skill was invoked; the plan hands
implementation to `adk-engineer`.

## 2. Questions I would have asked, and the answers I assumed

These are also recorded as the **Assumed answers** table (A1–A14) at the top of
`docs/architecture/helpdesk-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When is the first useful version due, and is it continued? | In 2 weeks; continued, so phase 1 code is kept |
| A2 | What does "half their time" mean in hours? | 0.5 of a 6-hour day, 10 working days each, at a 0.6 focus factor, which gives 36 focused hours |
| A3 | What is the budget for models and cloud? | Up to about US$100 a month |
| A4 | Who uses it and who judges phase 1? | 25 helpdesk staff eventually. Phase 1 is judged by the helpdesk lead from a demo plus a gold-question score |
| A5 | Which identity provider? | Google Workspace or Cloud Identity, so IAP can admit a Google group |
| A6 | Atlassian Cloud or Data Center? | Cloud, over the public REST APIs |
| A7 | Is the runbook space readable by all helpdesk staff, with no page restrictions? | Yes, so a single read-only bot account is enough |
| A8 | Do runbooks contain credentials or personal data? | No credentials by policy; conversations may name end users |
| A9 | Which Jira project, issue types, fields and reporter? | `ITHD`; Incident or Service Request; summary, description, priority and component; the bot is reporter plus a "Requested by" line |
| A10 | Create only, or also update and transition? | Create only |
| A11 | Is there an existing GCP organisation and billing account? | No; an admin must create them, which is a calendar wait |
| A12 | Is Vertex AI approved for runbook text, and is there a residency constraint? | Approved; no residency constraint |
| A13 | Where do staff use it? | A simple internal web page (phase 2) |
| A14 | Who labels the gold questions? | The helpdesk lead, about 2 hours |
| O1 | Is the cut line right (G01–G04 now, hosting in phase 2)? | Assumed yes |
| O4 | Real `ITHD` or a sandbox project for the phase 1 live ticket? | Left open for the Jira admin; it blocks only G04's live check |

## 3. Files written or changed, and what is unfinished

Written (all new; nothing existing was changed):

- `docs/architecture/helpdesk-assistant.md`: the design (draft). It contains the
  assumed answers, the profile and depth table, invariants I1–I5, decisions
  D1–D8, the security posture, budgets, failure table and open decisions O1–O6.
- `docs/plans/helpdesk-assistant.md`: the plan. It covers capacity, the load
  per engineer, the implementation map, phase 1 goals G01–G04 in full, phase 2
  goals G05–G11, the Later list and Resume here.
- `docs/tickets/helpdesk-assistant/G01-gcp-and-atlassian-access.md`
- `docs/tickets/helpdesk-assistant/G02-runbook-answers-offline.md`
- `docs/tickets/helpdesk-assistant/G03-runbook-answers-measured.md`
- `docs/tickets/helpdesk-assistant/G04-ticket-after-confirmation.md`
- `REPORT.md` (this file)

Not finished, or deliberately not done:

- **No implementation**, as the user asked.
- **Provider facts were not looked up** because network use was not allowed:
  - `gemini-3.8-flash` availability on Vertex in a region, and its price;
  - IAP and identity-provider details;
  - Confluence CQL syntax;
  - ADK 2.8.0 tool-confirmation support with `adk web` and in-memory sessions.

  Each is a named verification item (O5, O6, and the G01, G02 and G04
  acceptance). The cost estimate is symbolic, in token volumes only.
- **The model choice rests on the bundled lifecycle snapshot**
  (checked_on 2026-10-08), not a fresh lookup.
- **All decisions are provisional** until the user confirms A1–A14 and the cut
  line.
- **Phase 2 goals have no ticket files.** They are coarse by design.
- **Workload is lopsided:** Engineer B's high-end load (14 h) is 0.5 h over
  their share after the reserve. The plan names the mitigation.

## 4. Checks run and not run

Run (local, standard-library Python with `-I`, no network):

- **Relative links:** every relative link and `design:`/`plan:` front-matter
  path in `docs/**` resolves. Result: 0 broken.
- **Ticket estimates against the plan:** each ticket's total estimate equals
  its plan row. Result: G01 4–7, G02 3–5, G03 4–7 and G04 4–7, all OK.
- **Phase totals:** phase 1 sums to 15–26 h, phase 2 to 23–42 h. Both match
  the text in the design and plan.
- **Per-person load:** A 7–12 h, B 8–14 h, as stated in the plan.
- **Skill names:** every skill named in the design, plan and tickets exists
  under `.claude/skills/`. Result: 0 missing.
- **Size:** `wc -w` gives the design about 3,600 words, the plan about 2,900,
  and each ticket about 330–370.
- **Repository state:** `git status` shows only the new `docs/` tree, plus this
  report once written.

Not run:

- **Tests:** none exist, and nothing that imports `google.adk` can run
  (dependencies not installed).
- **Live checks:** none for Confluence, Jira, Vertex AI or GCP (not allowed).
  Every acceptance case in the tickets is a planned check, not evidence.

## 5. Friction log

**Unsure what to do:**

- **Asking versus assuming.** SKILL.md:52 says "Let the user answer before
  treating a material product choice as settled", and the scope gate
  (SKILL.md:54–68) asks for one turn of questions. The session rules forbid
  asking. SKILL.md:121–123 resolves this cleanly (an Assumed answers table, with
  decisions marked provisional). Helpful, but it sits roughly 70 lines after
  the instruction to ask, so I read the ask instruction first and had to look
  for the exception.
- **Converting "half their time for two weeks" into hours.** Only the worked
  example at `references/delivery-profiles.md:229-230` gives a 6-hour day. The
  capacity rule at `references/delivery-profiles.md:153` gives the focus factor
  but not hours per day. I copied the example's 6 h; a one-line default ("assume
  a 6-hour working day") in the rule would remove the guess.
- **Stacking multipliers.** `references/delivery-profiles.md:138-140` says ×1.5
  for a team new to ADK *and* +1 day for a team new to GCP. It is unclear
  whether "a day" means 6 focused hours or 8, and whether the ×1.5 also applies
  to that day. I folded the GCP day into G01 at 4–7 h; a reviewer might argue it
  should be larger.
- **Which ID goes in the closing prompt.** The skill's example closing prompt
  names G01 (SKILL.md:278; `references/implementation-handoff.md:105`). In this
  plan G01 is gated on admin waits and user authorisation for billing, so the
  next *ready* local goal is G02. I gave G02 and said why. The skill does say
  "next ready goal", so this is consistent, but the G01 example nudges towards
  copying it literally.
- **Choosing the primary skill for an "agent plus two tools" goal (G02).** The
  handoff table maps bounded orchestration to `adk-workflow-design`
  (`references/implementation-handoff.md:21`), but most of G02's work is tool
  declarations (`references/implementation-handoff.md:23`). I chose
  `adk-tool-interface-design`; the table gives no tie-breaker.
- **The model table is ambiguous for Vertex.** In
  `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12`,
  `gemini-3.8-flash` has no `vertex_retirement` field. I could not tell whether
  that means "no retirement announced" or "not on Vertex", so I made it O5 with
  a fallback.

**Heavier than needed:**

- **Document length for the profile.** The full design template
  (`assets/system-design-template.md`, 151 lines of sections) plus the plan
  template with all its fields pushed the design to about 3,600 words and the
  plan to about 2,900. That is at or over the "roughly two to four pages" for
  an internal tool (SKILL.md:85). Each goal's fields are also restated in its
  ticket, so the four phase-1 goals exist twice: plan and tickets.
- **Template asks that don't fit an internal tool.** The template's
  "Verification and implementation handoff" asks about evaluator deliverables
  and regeneration (`assets/system-design-template.md:123-127`), which fit
  assignments, not this profile. I left them out instead of marking them N/A.

**Genuinely helpful:**

- **The floor list** (`references/delivery-profiles.md:70-92`) made the
  confirmation-gated Jira write a non-negotiable, and kept it out of the
  scope-cutting.
- **The capacity rule** ("high end within capacity minus reserve",
  `references/delivery-profiles.md:161`) together with the longest-chain rule
  (`:146`) produced a defensible cut line (15–26 of 27 h) and the "if time runs
  out, stop after G02 → G03" ordering.
- **The model-lifecycle table** turned "which Gemini" into an evidence-based
  choice. It also exposed that `gemini-3.6-flash` (Vertex retirement
  2026-11-19) and `3.7-flash` (2027-01-28) would retire inside the plan
  horizon.
- **The `adk web` identity caveat** at
  `adk-tool-auth-and-secrets/references/identity-and-output.md:9` decided D7:
  `adk web` behind IAP is not an authenticated session, so phase 2 needs its
  own small app.
- **The trifecta table** in the design template
  (`assets/system-design-template.md:89-98`) forced an explicit accepted-risk
  row, with an owner and an end goal (G09), for runbook text plus a Jira write.
- **The calendar-waits rule** (`references/delivery-profiles.md:118-122`)
  surfaced the GCP and Atlassian admin waits as the real critical path, ahead of
  the coding hours.

## 6. The next prompt the skills told the user to type

The skill's own template example (SKILL.md:278) is:

> `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`

Applying the skill's "next ready goal" rule (SKILL.md:272-276), the closing
prompt written in `docs/plans/helpdesk-assistant.md` (Resume here) is:

```text
/adk-engineer Carry out G02 — Runbook answers with citations, offline from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions and adk-model-and-output-contracts.
Work within local file changes only, verify the G02 acceptance cases offline, and update
the plan with actual evidence and remaining blockers.
```
