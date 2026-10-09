# REPORT: IT helpdesk assistant design session

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`; SKILL.md loaded with it).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/assets/system-design-template.md`
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-system-designer/assets/ticket-template.md`
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
11. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md` (first 40 lines)
12. `grep` over every `.claude/skills/*/references/compatibility.md` for the ADK version (all name google-adk 2.8.0)
13. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (read because in-memory sessions are lost on deploy, which is a "continuity during a release" trigger)
14. `grep` in `.claude/skills/adk-agent-observability/references/compatibility.md` (content-capture default), `adk-operational-guardrails/SKILL.md` and `deploy-adk-on-google-cloud/SKILL.md` (no matches for the last two patterns).

No other skills were invoked. `adk-engineer` was not invoked (implementation was not requested).

## 2. Questions I would have asked, and the answers I assumed

Also recorded as the "Assumed answers" table in the design.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist, and is it kept? | End of the two weeks; kept and continued |
| A2 | How much money for models and cloud? | About USD 100/month, budget alert at 50% and 100% |
| A3 | Atlassian Cloud or Data Center? | Cloud (`*.atlassian.net`) |
| A4 | Which Confluence spaces; can all 25 staff read them; any page restrictions? | One or two IT runbook spaces, readable by all staff, no page restrictions |
| A5 | Do runbooks contain secrets or personal data? | They should not; pages labelled `restricted` are excluded |
| A6 | How do staff sign in? | Google Workspace; a `helpdesk@` group lists the 25 |
| A7 | Which Jira project/issue type; who should be reporter? | One project (e.g. `HELP`); the staff member who asked |
| A8 | Is "assistant drafts, person submits in Jira" acceptable for phase 1, with API creation in phase 2? | Yes. This sets the cut line. |
| A9 | Data residency? | None beyond normal company GCP use; `europe-west1`, model at `global` |
| A10 | Is the ADK dev UI acceptable as the phase 1 front end, accepting that team members can see each other's sessions? | Yes, for the 25-person team only, as an accepted risk |
| A11 | Who runs it afterwards? | The same two engineers, a few hours a month |
| — | Confirm the profile ("internal tool") and the cut line (G01–G04, G04 first to slip)? | Assumed confirmed |

## 3. Files written or changed, and what was not finished

Written (nothing else changed; no code; no commits):

- `docs/architecture/helpdesk-assistant.md`: draft design (assumed answers, journey, profile, depth table, floor, accepted risk, capacity and cut line, invariants I1–I6, decisions D1–D6, model-facing contracts, security posture, failure table, open decisions).
- `docs/plans/helpdesk-assistant.md`: plan with phase 1 goals G01–G04 in full, phase 2 G05–G08 in brief, Later list and resume prompt.
- `docs/tickets/helpdesk-assistant/G01-agent-answers-locally.md` (status ready)
- `docs/tickets/helpdesk-assistant/G02-cited-runbook-search.md` (blocked: G01, spaces, token)
- `docs/tickets/helpdesk-assistant/G03-hosted-behind-iap.md` (blocked: G02, GCP permission, group, A10)
- `docs/tickets/helpdesk-assistant/G04-jira-ticket-draft.md` (blocked: G01, Jira project)
- `REPORT.md` (this file)

Not finished:

- All assumptions still need the user to confirm them. The design stays **draft**.
- These provider facts were not verified (no network): the Confluence Cloud CQL search endpoint and fields, Jira Cloud create-URL pre-fill, IAP directly on Cloud Run vs a load balancer, and Vertex pricing. Each is an acceptance item in the goal that first relies on it. The cost estimate is symbolic.
- No implementation was done, as requested. No ticket files were written for phase 2 goals because the request asked only for phase 1.

## 4. Checks run and not run

Run:

- Relative `design:`/`plan:` links in all four tickets resolve to existing files: **ok** (8/8).
- Design↔plan cross-links resolve: **ok**.
- Grep for unfilled template placeholders (`<...>`) in `docs/`: **none found**.
- Arithmetic of phase 1 estimates (4–6 + 8–11 + 6–8 + 3–6 = 21–31 h) against capacity (2 × 0.5 × 10 × 6 × 0.6 = 36 h, 27 h after a 25% reserve). I checked it by hand. I found and fixed one inconsistency ("17–25" corrected to "18–25" for G01–G03).
- Word count: design 3,016 words, plan 2,229 words.

Not run:

- I ran no tests. No code exists, and google-adk is not installed, so anything that imports `google.adk` could not have run.
- No live, cloud or network checks were run (forbidden in this session): no model calls, no Confluence/Jira API checks, no `gcloud` or `adk deploy --help`.
- The installed ADK version could not be confirmed. 2.8.0 is a working assumption, and confirming it is a G01 acceptance item.

## 5. Friction log

Unsure what to do:

- **Headless vs "ask the user to confirm the cut line".** `.claude/skills/adk-system-designer/SKILL.md:92` says to show the cut line and ask the user to confirm it. `SKILL.md:119-121` says to ask nothing further when the user cannot answer. I resolved this by putting the confirmation into the assumed-answers table, but the rule that wins could be stated explicitly.
- **Which model to pin.** `SKILL.md` (about lines 193–197) points to the lifecycle table, and the table was useful. But it lists both `gemini-3.5-flash` (most evidence in the specialist skills; Vertex retirement "2027-05-19 or later") and `gemini-3.8-flash` (newest, no retirement date), and the designer gives no tie-break rule such as "prefer the model with no retirement date" or "prefer the one the specialists verified". I chose 3.5-flash, with migration on the Later list.
- **ADK pin.** Every specialist `references/compatibility.md` names 2.8.0. `adk-agent-observability/references/compatibility.md` (after line 18, "For a new production deployment prefer google-adk 2.10.0 or later") recommends a newer version. `SKILL.md:192` says to use "the version the specialists were checked against", so I kept 2.8.0 and noted the tension.
- **The call cap under `adk web`.** `delivery-profiles.md:77-80` says to use `RunConfig.max_llm_calls` when the app owns the Runner, otherwise a quota on the model project. Phase 1 serves through the dev UI, so I chose a `before_model_callback` counter. The skills don't say whether that is acceptable or how it interacts with `max_llm_calls`; the ticket leaves it for adk-operational-guardrails to confirm.
- **Ticket readiness with external prerequisites.** `assets/ticket-template.md:8` says `blocked_by` is empty when ready, and `:12` defaults `status: ready`. I couldn't tell whether "needs a GCP project / bot token from the user" counts as a blocker. I left G01 ready with the prerequisite in prose, and marked G02–G04 blocked with both goal and decision blockers.
- **Two prompt formats.** `assets/implementation-plan-template.md:67` gives a long per-goal run prompt, `ticket-template.md` gives another, and `SKILL.md:276` gives a short one. I couldn't tell which is "the" next prompt. I used the short form for the closing message and the template forms inside goals and tickets.
- **When to read runtime-and-delivery.md.** The trigger list in `SKILL.md` (the "Read runtime and delivery" paragraph) is broad. I read it only because of session loss on deploy, and it changed nothing in the design.

Heavier than needed:

- The design came out at about 3,000 words, beyond the "two to four pages" in `SKILL.md:84-85`. Together, the full system-design template (`assets/system-design-template.md`, 151 lines), the depth table, invariants, decisions, contracts, security posture and failure table push an internal tool past its target. A compact form for internal tools, like the one for POCs at `delivery-profiles.md:144-166`, would help.
- The plan and the tickets repeat the same goal content (by design, `implementation-handoff.md:109-112`). Four tickets plus four full plan entries is mostly duplication at this size.

Genuinely helpful:

- `delivery-profiles.md:180-185`: the worked example ("two engineers at half time for three weeks … internal tool … ≈ 54 focused hours") matched this request almost exactly and gave the capacity formula directly.
- `delivery-profiles.md:88-92` ("drafts a human sends instead of automatic replies") led to the key cut: a pre-filled Jira create link in phase 1 instead of API writes. That keeps the approval floor and removes credentials, duplicates and the trifecta, and it makes phase 1 fit.
- `design-decisions.md:182-196`: the lethal-trifecta check made the security posture for phase 1 vs phase 2 clear in two rows.
- `failure-review.md:3-5` ("do not invent write machinery for a read-only product") justified marking the write-failure scenarios not applicable for phase 1.
- `.claude/skills/adk-agent-observability/references/compatibility.md:9` (`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS` defaults on) gave a concrete, testable control for "no content in logs".

## 6. Exact next prompt the skills told the user to type

The skill (`SKILL.md:273-276`) gives this form verbatim: "/adk-engineer Carry out G01 from docs/plans/<topic>.md."

Instantiated for this plan:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```
