I've written the design, the plan and four phase-1 tickets; nothing is implemented. You weren't available, so all 14 product answers in the design are assumptions, listed in a table at the top, and the design stays a **draft** until you confirm them. Nothing was run against Confluence, Jira, Vertex AI or GCP, and no tests ran (none exist yet, and the ADK packages aren't installed).

**Profile:** an internal tool for known colleagues, using real runbooks and one internal write (creating Jira tickets).

**Capacity:** 2 engineers × half time × 10 days × 6 h × 0.6 focus gives about 36 hours. After a 25% reserve, 27 hours are available.

**Cut line (please confirm or move it):**

| Phase | Goals | Delivers | Hours |
| --- | --- | --- | --- |
| 1, now | G01–G04 | The assistant runs locally on the real runbooks and Jira, scored on 20 questions labelled by the helpdesk lead, and a ticket is created only after the analyst confirms its exact contents | 15–26 of 27 |
| 2, next block | G05–G11 | Sign-in with each user's own identity, hosting behind Google's login proxy (IAP) for all 25 staff, tests in CI, attack tests on the ticket tool, tickets attributed to the requesting analyst, and a before/after timing check | 23–42 |

- **Main design choices:**
  - One agent with four tools.
  - Live Confluence search limited in code to the runbook space(s).
  - Tickets go through a draft-then-confirm step, with no automatic retry. If the outcome is unclear, the analyst is told to check Jira.
  - The model is `gemini-3.8-flash`, picked from the skill's dated model table; the newer-but-retiring 3.6 and 3.7 models are ruled out.
- **Load:** Engineer B's share (setup and tickets, 8–14 h) runs about 0.5 h over their half of the hours. The plan says what to do about it.
- **Real critical path:** the GCP and Atlassian admins setting up the project and bot accounts, not the coding. Request both on day 1.
- **If time runs short:** stop after the scored runbook answers (G02 → G03), which are still useful without ticket creation.

**Still open:**
- **Sign-in provider:** which one staff use (O2); this blocks phase 2.
- **Atlassian hosting:** Cloud or Data Center (O3); assumed Cloud.
- **Phase 1 test ticket:** the real `ITHD` project or a sandbox (O4).
- **Model:** whether it is offered on Vertex in our region, and its price (O5). This was not looked up because network access wasn't allowed.
- **Confirmation step:** whether ADK 2.8.0's confirmation works in `adk web` (O6).

Next ready goal is G02, because G01 needs your go-ahead for a GCP project and billing:

```text
/adk-engineer Carry out G02 — Runbook answers with citations, offline from docs/plans/helpdesk-assistant.md.
Read docs/architecture/helpdesk-assistant.md and preserve its accepted decisions.
Use adk-tool-interface-design with adk-agent-instructions and adk-model-and-output-contracts.
Work within local file changes only, verify the G02 acceptance cases offline, and update
the plan with actual evidence and remaining blockers.
```

The report has the friction log. The main points: the design (about 3,600 words) and plan (about 2,900) run past the skill's "two to four pages" for this profile, and the skill gives no hours-per-day default for capacity, so I used the 6-hour day from its worked example.

Files are in `docs/`:
- architecture/helpdesk-assistant.md
- plans/helpdesk-assistant.md
- tickets/helpdesk-assistant/G01-gcp-and-atlassian-access.md
- tickets/helpdesk-assistant/G02-runbook-answers-offline.md
- tickets/helpdesk-assistant/G03-runbook-answers-measured.md
- tickets/helpdesk-assistant/G04-ticket-after-confirmation.md

`REPORT.md` is in the project root.