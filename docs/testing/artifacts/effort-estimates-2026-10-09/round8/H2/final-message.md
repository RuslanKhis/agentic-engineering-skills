The assistant is designed and planned and the five phase 1 tickets are written. Nothing was implemented. The biggest point for you: **Jira ticket creation is not in phase 1.** I moved it to phase 2 because, at the hours I assumed, it doesn't fit in the two weeks.

**Profile:** internal tool. It's for 25 colleagues using their own Google sign-in, on real internal runbooks, with one reversible write (creating Jira tickets, phase 2 only).

**What phase 1 delivers:** a web page behind Google sign-in, open only to the helpdesk group. It searches the Confluence runbook spaces and answers with a link to the page and version it used. It's measured on 15 real questions and tried by three helpdesk staff. That's 15.5–24.5 hours of work against 27 hours available, finishing in 7–10 of the 10 working days. The schedule checker confirms it fits, with no slack at the high end.

**What waits for phase 2:**
- **G03:** the assistant drafts a ticket for review.
- **G07:** a ticket is created only after the person confirms it, at most one per confirmation.
- **G08:** tests with runbook pages that contain hidden instructions.
- **G09:** an automatic quality check in CI.

**The cut line depends on one assumption you should check.** I assumed each engineer has 1.8 focused hours a day ("half their time" on a 6-hour focused day, at 60% focus). If they really have about 2.4, ticket drafting (G03) fits in phase 1, but confirmed creation (G07) still doesn't. Every alternative was run through the schedule checker; the results are in the plan's what-if table.

**Other decisions still open:**
- **Restricted runbook pages:** are any visible to only some of the 25? Phase 1 reads Confluence through one shared read-only account, which would show restricted pages to everyone. This blocks go-live (G05).
- **Jira reporter:** should tickets name the requesting agent as reporter? The bot account then needs the "Modify reporter" permission. This blocks G07.
- **Not yet verified:** whether Gemini 3.8 Flash is available on Vertex AI in your region (G01 checks this, with Gemini 3.5 Flash as the fallback), and whether Jira can find a ticket by an ID we attach to it (needed to avoid duplicates; G07 starts with this check).

All 13 assumptions are in a table at the top of the design, and each question is also in `REPORT.md`.

**Checks:** the schedule checker passed, with tickets consistent with the plan, and all links between the documents resolve. It ran on Python 3.9 although the skill names 3.11. No tests, live checks or network commands were run, and `google.adk` tests can't run here.

The design and plan come to about 4,600 words against the skill's 4,000 budget, and tickets are about 250 words each against about 150. I didn't trim them.

Next, Dev A starts G01; Dev B can start G04 at the same time:

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G01-runbook-search-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Files are in `docs/`:
- architecture/helpdesk-assistant.md
- plans/helpdesk-assistant.md
- tickets/helpdesk-assistant/G01-runbook-search-agent.md
- tickets/helpdesk-assistant/G02-gold-set-measurement.md
- tickets/helpdesk-assistant/G04-identity-bound-chat.md
- tickets/helpdesk-assistant/G05-deploy-behind-iap.md
- tickets/helpdesk-assistant/G06-pilot.md

`REPORT.md` is in the project folder.