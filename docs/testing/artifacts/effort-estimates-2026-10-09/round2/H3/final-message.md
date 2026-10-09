I've written the design, the plan and one ticket for each of the five phase 1 goals, and nothing is implemented. You weren't available, so every scope question is an assumed answer (13 in all), listed at the top of the design. Everything stays a draft until you confirm or correct them.

**What it is:** an internal tool for the 25 helpdesk staff. Staff sign in with their own accounts and work on the real runbooks. The only thing it can change is creating an internal Jira ticket, and only after the person confirms the exact draft.

**Cut line:** I assumed "half their time" means 20 hours a week each. That gives about 48 focused hours over two weeks. After keeping 25% in reserve, 36 hours are available.
- **Phase 1 (G01 to G05) is estimated at 21 to 36 hours.** It delivers a hosted assistant behind Google sign-in: runbook answers with links to the source pages, checked against 12 sample questions, plus ticket creation after confirmation.
- It only fits at the high end with nothing to spare. If work runs long, ticket creation (G03) moves to phase 2. Search alone is still useful to all 25 staff.
- The real schedule risk is waiting on other teams. The GCP project, the Atlassian bot accounts and the sign-in setup all need admins, so those requests should go in on day 1.
- **Phase 2 (G06 to G12, 28.5 to 57 hours) waits.** It covers:
  - conversations that survive restarts;
  - a decision on whether keyword search is good enough;
  - tickets filed under the requester's name instead of a bot;
  - evaluation in CI;
  - tracing;
  - a scan for passwords in runbooks;
  - stronger handling of duplicate tickets.

**Main design choices:**
- **One agent, three tools:** search the runbooks, read a page, create a ticket.
- **Search:** Confluence's own search runs live against a short list of approved spaces, so there is no index to build or keep up to date.
- **Ticket creation:** a bot account files the ticket, after a confirmation step enforced in code rather than in the prompt. The project and ticket types are fixed by code.
- **Hosting:** Cloud Run behind Google sign-in; the app also checks the sign-in itself.
- **Model:** `gemini-3.8-flash` on Vertex AI. I chose it because the 3.6 and 3.7 versions are retired on Vertex AI within the next few months.

**Open decisions:**
- **Sign-in system:** if staff don't sign in with Google accounts, G05 turns into an investigation.
- **Jira:** which project and ticket types, and whether creating a ticket emails anyone outside IT.
- **Runbooks:** which spaces are included and who can edit them.
- **Region:** where to host, which depends on where the model is available.
- **Bot as reporter:** whether tickets showing the bot as reporter is acceptable for now.
- **Search quality bar:** the targets for the 12 sample questions, which decide whether better search is worth building.

**Checks:** a script confirmed the hours add up and every ticket's estimate matches the plan, and all links between the documents work. No application tests exist yet. Nothing touching the network, cloud, Atlassian or the model was run, so model availability, prices and the Confluence, Jira and sign-in setup details are still unchecked. Each of those is an acceptance item on its goal.

The design came out at about 4,200 words, longer than the skill's two-to-four-page guidance for an internal tool; I didn't trim it. `REPORT.md` has the questions I'd have asked, the checks, and a friction log with pointers into the skill files.

Files are in `docs/`:
- architecture/helpdesk-assistant.md
- plans/helpdesk-assistant.md
- tickets/helpdesk-assistant/ (G01 to G05)

Next step:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use deploy-adk-on-google-cloud with adk-model-and-output-contracts.
Work within the team's own GCP project and local machine, verify G01's acceptance
cases, and update the plan with actual evidence and remaining blockers.
```

G02 doesn't need the cloud setup to start, so the second engineer can begin it in parallel with `/adk-engineer Carry out docs/tickets/helpdesk-assistant/G02-cited-runbook-answers.md.`