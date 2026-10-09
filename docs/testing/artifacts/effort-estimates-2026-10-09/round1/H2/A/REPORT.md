# REPORT: helpdesk assistant design session

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, through the user's slash command. No
other skill was invoked. Files were opened in this order (paths are relative to
`.claude/skills/`):

1. `adk-system-designer/SKILL.md` (supplied with the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/references/gcp-decisions.md`
7. `adk-system-designer/assets/implementation-plan-template.md`
8. `adk-system-designer/assets/ticket-template.md`
9. `adk-system-designer/assets/system-design-template.md`
10. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
11. `adk-model-and-output-contracts/references/compatibility.md`, first 40 lines
12. A grep of `*/references/compatibility.md` for the pinned ADK version (2.8.0)

Not opened: `adk-system-designer/references/runtime-and-delivery.md`. I judged
that its trigger did not apply: there is no streaming, no result download, and
one instance serves 25 users. See the friction log.

## 2. Questions I would have asked, and the answers I assumed

The design's **Assumed answers** table (A1–A15) also lists the decisions that
depend on each answer.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist, and is it continued afterwards? | End of week 2 (2026-10-23); continued |
| A2 | Who runs it after the build? | The same two engineers (the build team itself was given) |
| A3 | What is the model and cloud budget? | About USD 300 a month, with a budget alert |
| A4 | Who uses and judges it? | 25 helpdesk technicians daily; the helpdesk lead judges |
| A5 | What data does it touch, and what may it change? | Internal runbooks, read only; creates issues in one Jira project; chats may contain end-user names and emails |
| A6 | Atlassian Cloud or Data Center? | Cloud |
| A7 | Which Jira project, issue types and required fields? | `ITHD`; Incident and Service Request; summary, description, priority |
| A8 | Whose name goes on the ticket? | An Atlassian service account creates it; the technician's email goes in the description and a label; reporter mapping waits for phase 2 |
| A9 | Where do technicians work: web page, Google Chat, Slack, Jira panel? | A web page behind IAP |
| A10 | Is a Google group usable with IAP for the helpdesk? | Yes (`it-helpdesk@`) |
| A11 | Which spaces are runbooks, and are any pages restricted? | 1–3 spaces readable by all of the helpdesk; restricted pages excluded |
| A12 | What hosting, region, ADK pin and session store do the existing agents use? | Cloud Run with the team's deploy template and usual region; `google-adk==2.8.0` |
| A13 | Any data-residency limits on inference? | None beyond Vertex AI in the team's region |
| A14 | What is the success measure and baseline? | No baseline; measure gold-set citation accuracy plus timed pilot tasks |
| A15 | Can tickets notify outside or customer users (JSM)? | No; `ITHD` is internal |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/helpdesk-assistant.md`: the design, status **draft**,
  with assumed answers, profile, depth table, invariants I1–I7, decisions
  D1–D7, security posture and failure table.
- `docs/plans/helpdesk-assistant.md`: the plan, with capacity, person load,
  the cut line, G01–G05 in full, G06–G11 coarse, the later list and the resume
  prompt.
- `docs/tickets/helpdesk-assistant/G01-runbook-answers-with-links.md`
- `docs/tickets/helpdesk-assistant/G02-gold-questions-measured.md`
- `docs/tickets/helpdesk-assistant/G03-ticket-draft-confirm-create-once.md`
- `docs/tickets/helpdesk-assistant/G04-signed-in-page-per-user-scope.md`
- `docs/tickets/helpdesk-assistant/G05-cloud-run-iap-pilot.md`
- `REPORT.md` (this file)

Not finished or not done:

- No implementation, as instructed.
- All decisions are provisional: none were confirmed by the user, and the
  cut line was not confirmed either.
- These were not verified against current sources, because no network was
  available: the Confluence and Jira REST endpoints, Vertex pricing, IAP
  details and the `state_delta` session-append API. Each is listed as a
  verification item on its goal.
- The design runs to about 3,600 words, longer than the skill's "two to four
  pages" for an internal tool. I did not trim it further.
- Nothing was committed. The changes are left untracked in the working tree.

## 4. Checks run and not run

Run:

- **Link and path check** (a local Python script over `docs/**/*.md`): every
  relative link and every `docs/...md` path resolves. Result: OK.
- **Estimate consistency check** (same script): each ticket's total equals its
  plan row and equals hands-on plus review. Phase 1 sums to 18–28 hours, within
  the 28 hours left after reserve. Result: OK.
- **Phase 2 total, checked by hand.** This found an error: the plan said
  22–43. It now says 16–31, or 24–45 with G08. I fixed this after the script
  ran, and the script's check does not cover the phase 2 row.
- **Word counts** (`wc -w`): design 3,572, plan 3,441 and tickets 316–382
  words each, measured before the fix above.

Not run:

- No tests exist, and none could run: there is no code, and google-adk is not
  installed.
- No live checks against Confluence, Jira, Vertex AI or GCP: network and cloud
  commands were not allowed.
- Model IDs were checked only against the bundled lifecycle snapshot
  (`checked_on` 2026-10-08), not live.

## 5. Friction log

**Unsure**

- **Whether to read `runtime-and-delivery.md`**
  (`.claude/skills/adk-system-designer/SKILL.md:180`). The trigger list
  ("context limits, result downloads, browser streams, concurrent sessions,
  capacity…") arguably covers any multi-user chat, because every such service
  has concurrent sessions. I skipped it. A clearer "skip when…" line would help.
- **Tickets for all phase 1 goals or only the ready ones.**
  `.claude/skills/adk-system-designer/SKILL.md:268-269` says "one file per
  ready goal", but the user asked for "ticket files for the phase 1 goals".
  G04 and G05 are blocked. I wrote all five, with `blocked_by` and
  `status: blocked`. `.claude/skills/adk-system-designer/assets/ticket-template.md:17`
  defaults `status` to `ready`, and the template gives no guidance on blocked
  tickets.
- **Hours per working day in the capacity formula.**
  `.claude/skills/adk-system-designer/references/delivery-profiles.md:153-155`
  gives the focus factor but not the hours in a day. I took 6 hours from the
  worked example at `delivery-profiles.md:229-231`.
- **Reserve when the high end fits only barely.** The reserve is 20–30%
  (`delivery-profiles.md:158`). Phase 1's high end of 28 hours fits only with
  a reserve of about 22%. The guidance does not say which end of the band an
  experienced team should use.
- **Which ADK version to use with no installed project.**
  `SKILL.md:192-197` resolved this cleanly: use the specialists'
  `compatibility.md` version and make confirming it an acceptance item of the
  first goal.

**Heavier than needed**

- **Design length against "two to four pages".** `SKILL.md:85` asks for two to
  four pages, but `.claude/skills/adk-system-designer/assets/system-design-template.md`
  has about ten sections plus an Assumed-answers table with 15 rows. Filling it
  honestly for a small internal tool gave about 3,600 words. The template has a
  compact form only for a POC (`delivery-profiles.md:193-215`), not for an
  internal tool.
- **Ticket and plan duplication.** The plan template wants every goal fully
  filled (`assets/implementation-plan-template.md:56-79`), and the tickets
  copy the same content (`references/implementation-handoff.md:109-112`).
  Phase 1 acceptance criteria therefore exist twice, and they will drift.

**Genuinely helpful**

- **Model choice.** The model lifecycle snapshot
  (`.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`)
  together with `SKILL.md:197-201` stopped me from choosing `gemini-3.6-flash`
  (Vertex retirement 2026-11-19) or `gemini-3.7-flash` (2027-01-28).
- **Close worked example.** `delivery-profiles.md:229-234` (two engineers, half
  time, internal tool) matched this case almost exactly. The estimate table at
  `delivery-profiles.md:124-136` gave defensible per-goal ranges.
- **Removing the write leg.** The lethal-trifecta guidance
  (`references/design-decisions.md:182-196`) led to the key design move, D3:
  the model gets no create tool, and app code creates the issue after a human
  click.
- **Choosing supporting skills.** The rules at
  `references/implementation-handoff.md:39-51` made the supporting-skill lines
  mechanical rather than guesswork.
- **Budget alerts are not caps.** `references/gcp-decisions.md:64-66` kept the
  design from claiming that a budget alert caps spend.
- **Headless runs.** The rule at `SKILL.md:120-124` (an Assumed-answers table
  and provisional decisions) was exactly the instruction this run needed.

## 6. Next prompt the skills told the user to type

The skill (`.claude/skills/adk-system-designer/SKILL.md:275-279`) requires a
copyable prompt for the next ready goal. Its example form is
"`/adk-engineer Carry out G01 from docs/plans/<topic>.md.`". The prompt given,
filled in for this plan:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```
