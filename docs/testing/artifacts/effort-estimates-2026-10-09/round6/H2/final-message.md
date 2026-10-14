I've written the design, the plan and tickets for the five phase 1 goals, plus REPORT.md. Nothing is implemented. Every decision is still provisional, because with no one to ask I assumed all 14 scope answers (A1–A14, at the top of the design).

**The design in brief:** one ADK agent on Cloud Run, reachable only by the helpdesk through IAP (Google's sign-in gate). It searches the IT runbook spaces in Confluence live and cites the page in each answer. It never creates a Jira ticket itself: it shows a preview card, and the ticket is created only when the staff member presses **Create**. That button calls ordinary application code the model can't reach, so a runbook page with planted instructions can at most shape a draft that a person reads first. I picked `gemini-3.5-flash` from the dated model list bundled with the skills, because `gemini-3.6-flash` retires on Vertex on 2026-11-19, inside the plan's horizon.

**Profile:** internal tool. The users are 25 known colleagues and the only write is a Jira issue a human confirms.

**Cut line:**
- **Phase 1:** G01 search agent, G02 confirmed ticket creation, G03 signed-in page, G04 Cloud Run deployment, G05 deployed walkthrough with the helpdesk lead. That is 14–23 hours of the 27 available after a 25% reserve, finishing in 5.9–9.6 of the 10 working days. The schedule script confirmed this and that the tickets match the plan.
- **Phase 2:** G06–G10, about 16–29 hours: rollout to all 25 with feedback, durable ticket proposals, Jira reporter attribution, a CI evaluation gate, and a retrieval decision if keyword search scores under 80%.

**What made it fit:** the first two schedule runs only fitted the calendar at the low end. Durable ticket records and automatic recovery from Jira timeouts went into phase 2, since this profile only requires confirmation before writes. If you'd rather keep them in phase 1, either 12 working days or Dev B at 2.3 focused hours a day instead of 1.8 also fits; I ran both through the schedule script.

**Schedule risk:** Dev A has about half an hour of slack at the high end, on G01 → G03 → G05.

**Decisions still open:**
- Do all staff sign in with Google accounts, so IAP works?
- Atlassian Cloud or Data Center?
- The real Jira project key, issue types and required fields, and whether creating a ticket emails its reporter.
- Which runbook spaces, and whether any runbook contains credentials.
- The monthly model and cloud budget (I assumed about US$200).

**Not done:**
- No tests could run: nothing is implemented and `google-adk` isn't installed. There were no network or cloud checks either, so prices and Atlassian API behaviour are unverified and listed as checks in the plan.
- The documents run over the skill's reading budget: design and plan are about 7,100 words against about 4,000. I didn't trim further because the skill forbids cutting acceptance cases to meet it.

Next prompt, as the skill gives it:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

Files are in `docs/`:
- architecture/helpdesk-assistant.md
- plans/helpdesk-assistant.md
- tickets/helpdesk-assistant/ (G01–G05)

REPORT.md is in the project root.