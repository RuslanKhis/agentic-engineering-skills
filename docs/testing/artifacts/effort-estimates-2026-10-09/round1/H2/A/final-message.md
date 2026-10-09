I've written the design, the plan and five phase 1 tickets, plus `REPORT.md`; nothing is implemented. Every decision is provisional, because each product question was answered by assumption (15 of them, listed at the top of the design). No tests could run: there is no code yet and google-adk isn't installed. I also made no live calls to Confluence, Jira or GCP, so the API endpoints and Vertex pricing are unchecked.

**Profile:** an internal tool. The 25 helpdesk staff sign in with their own identity and use it daily on real runbooks, and it creates issues in one internal Jira project (I assumed `ITHD`).

**The main design choice:** the model never creates Jira issues itself. It can only write a draft. The technician checks the draft and clicks Create, and ordinary app code then creates exactly one issue for that draft. So a runbook containing planted instructions can at worst produce a draft that a person reads before anything happens.

**Capacity and cut line:**
- Two engineers at half time for two weeks gives about 36 focused hours; after a 22% reserve that leaves 28.
- **Phase 1 (G01–G05) is 18–28 hours**, so even the high end fits:
  - G01: answers with runbook links, run locally.
  - G02: a 20–25 question set to measure answer quality.
  - G03: draft, confirm, then exactly one Jira issue.
  - G04: a signed-in web page where each person sees only their own chats and drafts.
  - G05: a pilot on Cloud Run behind IAP with 3–5 technicians.
- If the work runs high, the pilot stays at those 3–5 technicians and opening it to all 25 moves to phase 2.
- **Phase 2 (G06–G11) is 16–31 hours**, or 24–45 if the gold set comes in below 80% and better search (G08) is needed. It covers chats that survive restarts, automatic checking of uncertain ticket creates, a test gate in CI, prompt-injection tests and usage metrics.

**Open decisions:**
- Whether Confluence and Jira are Cloud, plus the Jira project and required fields.
- Web page or Google Chat for the interface.
- The ADK version, region and deployment template the team's other agents use.
- Whether Jira search finds a just-created issue straight away (this decides whether G07 can safely automate checks).
- Whether plain Confluence search is good enough; G02's result answers that.

**Start on day 1:** these can take days, so request them early:
- Two Atlassian service accounts with tokens.
- An hour of the helpdesk lead's time to pick test questions.
- The Google group for IAP.

The design runs to about 3,600 words, longer than the skill's two-to-four-page target for an internal tool; I didn't trim it. `REPORT.md` also has the friction log.

G03 has no dependencies, so it can run in a second session alongside G01. The next prompt to type:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```

Files are in `docs/`:
- `architecture/helpdesk-assistant.md`
- `plans/helpdesk-assistant.md`
- `tickets/helpdesk-assistant/` (G01–G05)