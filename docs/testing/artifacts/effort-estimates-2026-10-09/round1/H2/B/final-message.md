I've written the design, the build plan and four phase 1 ticket files, plus `REPORT.md`; nothing is implemented. You weren't available, so every answer to the setup questions is an assumption. Those are listed at the top of the design, and every design decision is still a proposal. The only checks run were a link check (no broken links), a check of the ticket headers, an estimate sum and a scan for secret-like strings (none found). No tests ran, since there's no code and google-adk isn't installed.

**Documents:**
- `docs/architecture/helpdesk-assistant.md` (the design)
- `docs/plans/helpdesk-assistant.md` (the build plan)
- `docs/tickets/helpdesk-assistant/` (G01–G04)
- `REPORT.md`

**Profile:** an internal tool. It's for 25 known colleagues, signing in as themselves, on real runbooks, with one kind of write (creating Jira issues).

**Design in brief:**
- **Agent:** one agent with three tools: search the runbooks, fetch a page, and draft a ticket. Search is live against the allowed Confluence spaces only, and every answer links the pages it used.
- **Ticket creation:** the model can only *draft* a ticket. The issue is created only when the engineer presses **Create**, and that runs in the app's own code, which the model can't call. So hostile text inside a Confluence page can't create a ticket by itself. Each click is recorded, so a double click gives one issue. If Jira's reply is lost, the app searches Jira for the issue and never blindly retries.
- **Hosting:** one Cloud Run service behind Google sign-in (Identity-Aware Proxy), limited to the helpdesk's Google Workspace group.
- **Model:** pinned to `gemini-3.8-flash`, with `gemini-3.5-flash` as the fallback. The skills' model-retirement table ruled out `gemini-3.6-flash`, which retires on Vertex AI on 2026-11-19.

**Cut line:** phase 1 is G01–G04, estimated at 19–27 focused hours. Your capacity is about 36 focused hours, which leaves 27 after a 25% reserve, so the high estimate just fits with no slack.
- **G01:** confirm the Confluence, Jira and model facts the build depends on.
- **G02:** cited runbook answers, running locally.
- **G03:** hosted behind sign-in for the helpdesk.
- **G04:** Jira creation after the engineer confirms.

If G04 runs over, the fallback is a prefilled Jira "create issue" link the engineer submits in Jira themselves, and direct creation moves to phase 2. Phase 2 (G05–G09) covers measuring quality, a release gate, tickets created under each engineer's own Jira account, screening secrets out of runbook text, and conversations that survive restarts.

**Open decisions:**
- Are your Confluence and Jira Cloud or Data Center?
- Do any runbook pages have restrictions narrower than the whole helpdesk? If so, the shared search account could expose them.
- Can the Jira account set the reporter, and which fields are required?
- Is `gemini-3.8-flash` available on Vertex AI in your region?
- How will the helpdesk lead judge success?
- What daily per-user limit and budget alert do you want? I assumed 40 questions per person per day.

**Issues for you:**
- **Design length:** the design is about 3,400 words, longer than the two to four pages the skill sets for an internal tool.
- **Blocked tickets:** the skill says to write tickets only for goals that are ready to start. I wrote all four because you asked for every phase 1 goal; G03 and G04 are marked blocked until their prerequisites are done.

Next prompt, as the skill gives it:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

G01 needs someone with Atlassian admin access. G02 can start in parallel using stand-in Confluence and Jira clients.