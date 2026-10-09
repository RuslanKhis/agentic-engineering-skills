# REPORT: helpdesk assistant design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer` command. No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (full)
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (full)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (full)
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md` (full)
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (full)
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (full)
8. `.claude/skills/adk-system-designer/assets/ticket-template.md` (full)
9. `.claude/skills/adk-system-designer/assets/system-design-template.md` (full)
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full; SKILL.md:197-199 tells you to choose the model from it)
11. The first lines of each specialist's `references/compatibility.md`, read with grep to find the ADK version they were checked against (2.8.0; 2.11.0 upstream)
12. `.claude/skills/adk-tool-interface-design/references/function-tool-contract.md:160-185` (`require_confirmation` semantics)
13. `.claude/skills/deploy-adk-on-google-cloud/references/cloud-run.md`, lines matching IAP (lines 58 and 140 only)
14. `.claude/skills/adk-engineer/SKILL.md`, lines matching "ticket", to confirm it accepts ticket files

I did not open `references/runtime-and-delivery.md`. Its trigger (context
limits, downloads, streams, concurrency, release continuity; SKILL.md:180) did
not apply to a 25-user, non-streaming tool.

## 2. Questions I would have asked, and the answers I assumed

These are also recorded as the **Assumed answers** table (A1–A13) at the top
of `docs/architecture/helpdesk-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first useful version exist, and is it continued? | End of the two weeks; continued by the same engineers |
| A2 | What does "half their time" mean in hours? | 20 h/week each (40 h week) → 80 nominal, 48 focused at 0.6 |
| A3 | Budget for models and cloud? | About USD 100–300/month; alert-only budget |
| A4 | Who uses it, and through what? | The 25 helpdesk staff, daily, in a browser; no end customers |
| A5 | Atlassian Cloud or Data Center? | Cloud (REST plus API tokens) |
| A6 | Which runbook spaces, how big, who edits, any restrictions? | 1–3 spaces, a few hundred pages, readable by all helpdesk staff, edited by IT staff only |
| A7 | Which Jira project and issue types, and does create notify outside requesters? | One internal project (`ITSD`; sandbox `ITSDTEST`), Incident / Service Request / Task, no outside notification |
| A8 | Is a bot account acceptable as reporter? | Yes for phase 1, with the requester's verified email in the ticket footer |
| A9 | What do staff sign in with? | Google Workspace / Cloud Identity, so IAP works directly; a helpdesk Google group exists or can be created |
| A10 | Is there a GCP organisation and a cloud admin? | Yes; the admin creates the project and billing link on request |
| A11 | Any data residency or regulated data? | No; one region, internal and personal (not regulated) data |
| A12 | Can runbooks contain credentials? | Possibly; accepted risk R2 until the G11 scan |
| A13 | Is there CI? | No; tests run locally in phase 1 |
| — | Region? | Left open: one region where the pinned model is available, chosen in G01 |
| — | Gold-set targets? | Provisional 9/12 hit@5 and 10/12 cited; they trigger G07 and do not block |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/helpdesk-assistant.md`: design (draft). It has the assumed answers, profile, depth table, invariants I1–I8, decisions D1–D9, model-facing contracts, data and security posture, budgets, failure table, verification and open decisions.
- `docs/plans/helpdesk-assistant.md`: plan with capacity, load per person, longest chain, cut line, implementation map, phase 1 goals G01–G05 in full, phase 2 goals G06–G12 (coarse), the later list and a "Resume here" section.
- `docs/tickets/helpdesk-assistant/G01-gcp-foundation.md`, `G02-cited-runbook-answers.md`, `G03-confirmed-jira-ticket.md`, `G04-chat-page-verified-identity.md`, `G05-cloud-run-behind-iap.md`: one ticket per phase 1 goal.
- `REPORT.md` (this file).

Nothing was implemented, as requested. No changes were made outside the current directory.

Not finished:

- All provider facts are still unverified: model region availability and price, IAP for Cloud Run setup, Confluence CQL and Jira create endpoints, and Jira idempotency support. Each one is an acceptance item on G01, G02, G03 or G05.
- The design is about 4,200 words, which is longer than the internal-tool guidance of "roughly two to four pages" (SKILL.md:84-85). I did not trim it (see friction).
- Phase 2 goals have no ticket files. The request covered phase 1 tickets only.

## 4. Checks run and checks not run

Run:

- A Python consistency script (`python3 -I`, stdlib only, reads the docs). For every phase 1 goal in the plan, hands-on + review = total. The phase 1 sum is 21–36 h, against 36 h available. Every ticket's hands-on, review and total figures **match** the plan. All relative links and the `design:`/`plan:` front-matter paths **resolve**. Result: passed.
- `wc -w` on the design and plan: 4,191 and 4,157 words.

Not run:

- No application tests. There is no code, and `google-adk` is not installed, so anything importing `google.adk` could not run.
- No network, cloud, Atlassian or model calls, and no lookups of current Google or Atlassian documentation (forbidden this session). Provider facts stay provisional, as listed above.
- The skills' own test suites under `.claude/skills/*/tests` were not run; they are not this project's tests.

## 5. Friction log

**Unsure what to do**

- Capacity hours. `delivery-profiles.md:162` gives people × hours × focus, but the worked example at `delivery-profiles.md:239` uses 6-hour days. "Half time for two weeks" gives 36 focused hours with 6-hour days and 48 with 8-hour days. That one choice decides whether phase 1 includes Jira creation. I picked 40-hour weeks (A2) and recorded it, but the reference does not say which day length to assume.
- The "add a day" for a team new to GCP (`delivery-profiles.md:144`) does not say how many hours a day is, or whether the 1.5× multiplier applies to it. I used 4–6 h with no multiplier, on G01 only.
- Ticket status for goals waiting only on an earlier goal. `assets/ticket-template.md:8` says `blocked_by` is "empty when ready", and `:17` defaults to `status: ready`. G03 and G04 depend only on G02, which has not started, so I set `blocked`. The plan's table says "ready after G02". The two vocabularies differ slightly.
- Splitting chains across people. `delivery-profiles.md:152-155` asks for the longest chain and the busiest person. My chain crosses both engineers (G02 → G04 → G05) and only fits if G02's offline part overlaps G01. I had to reason about partial dependencies myself; the reference has no pattern for "offline part ready now, live part waits on X".
- Reserve choice. The 20–30% range (`delivery-profiles.md:167`) left room to make the plan fit by picking 20%. I used 25% and cut differently. A sentence on what sets the reserve (for example, new-to-platform → upper end) would remove the temptation.

**Heavier than needed**

- Document size. With the full `assets/system-design-template.md` plus every topic in `design-decisions.md`, the internal-tool design came out at about 4,200 words, above the `SKILL.md:84-85` target. The template has no compact internal-tool variant (the compact form at `delivery-profiles.md:202-224` is for POCs and assignments only), so filling every section pushes length up.
- The plan repeats the design's decision rationale in its implementation map, even though `implementation-handoff.md:67-69` says to link rather than copy. Some overlap seemed hard to avoid when filling the template's map columns.

**Genuinely helpful**

- `delivery-profiles.md:131-146`, the estimate table plus the 1.5× multiplier, made it obvious that the naive scope (about 23–45 h) did not fit. It forced a real cut line, with G03 as the first goal to move.
- `delivery-profiles.md:122-126` on calendar waits pushed the Atlassian and GCP admin requests to day 1. Those waits, not hours, are the real schedule risk.
- `design-decisions.md:182-196`, the lethal-trifecta check, gave a clear structure for accepting one agent with a confirmation-gated write instead of either ignoring injection or over-splitting.
- `SKILL.md:197-199` together with `model-lifecycle-2026-10-01.json` stopped me from picking `gemini-3.6-flash` or `3.7-flash`, which retire on Vertex on 2026-11-19 and 2027-01-28, inside the maintenance horizon.
- `function-tool-contract.md:160-175` gave exact `require_confirmation` behaviour (rejection text, `function_call_id` requirement), which shaped invariant I3 and the G04 `/confirm` contract.
- `failure-review.md:30` ("Provider commits, reply is lost") produced the label-based reconciliation in I5 and G03 instead of a naive retry.

## 6. Exact next prompt the skills told the user to type

The plan's "Resume here" section and the closing message give, built from the
`SKILL.md:277-279` example and the plan template's continuation prompt:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use deploy-adk-on-google-cloud with adk-model-and-output-contracts.
Work within the team's own GCP project and local machine, verify G01's acceptance
cases, and update the plan with actual evidence and remaining blockers.
```

The verbatim example in `SKILL.md:277-279` is
`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`, which for this
project is `/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.`
