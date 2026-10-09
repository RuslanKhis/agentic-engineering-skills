I've written the design, the plan, four phase 1 ticket files and `REPORT.md`, and implemented nothing, as you asked. The design is a **draft**: I couldn't reach you, so every scoping answer is an assumption listed in a table at the top of the design.

**Files**
- `docs/architecture/helpdesk-assistant.md`: the design.
- `docs/plans/helpdesk-assistant.md`: the plan, with phase 1 and phase 2 goals and a list of later items.
- `docs/tickets/helpdesk-assistant/G01`–`G04`: one ticket per phase 1 goal. G01 is ready; G02–G04 are marked blocked until earlier goals and your inputs exist.
- `REPORT.md`: the six sections you asked for.

**Profile:** an internal tool. Your 25 helpdesk colleagues sign in with their own identity, it reads real runbooks, and it has one write action (Jira tickets).

**Design in brief**
- **Agent:** one ADK agent with two tools, using the `gemini-3.5-flash` model on Vertex AI.
- **Runbook search:** live keyword search of allowlisted Confluence spaces through a read-only account. Every answer links the pages it came from, or says "no runbook found".
- **Hosting:** one Cloud Run service behind Google sign-in (IAP), limited to a `helpdesk@` group.
- **Spend:** each question is capped at 6 model calls, plus a billing alert. The alert only notifies; it doesn't stop spending.

**The main cut: Jira tickets.** In phase 1 the assistant doesn't create tickets itself. It builds a link that opens Jira's create screen with the summary and description filled in, and the person submits it under their own login. That way no ticket exists without a human, there's no Jira credential to manage and no risk of duplicate tickets, and phase 1 fits the time. Direct creation through the Jira API, with a confirmation step and duplicate protection, is phase 2 (G05).

**Capacity and cut line**
- **Hours:** about 36 focused hours (2 people × half time × 10 days × 6 h × 0.6 focus). A 25% reserve leaves 27 usable.
- **Phase 1:** G01 local agent, G02 cited search, G03 hosted behind sign-in, G04 ticket drafts. Estimated 21–31 hours, so it fits only at the low-to-middle end. If work runs high, G04 moves to phase 2 and G01–G03 (18–25 h) still give colleagues hosted runbook search.
- **Phase 2:**
  - G05: direct ticket creation.
  - G06: per-user conversations and a small front end.
  - G07: a regression set in CI.
  - G08: tracing and cost.

**Decisions still open** (each is assumed in the design; changing it can move the cut line):
- Whether drafts that a person submits are acceptable for phase 1.
- Whether the ADK developer web UI is acceptable as the front end. In it, team members can open each other's conversations; I recorded that as an accepted risk until G06.
- Which Confluence spaces to search, and whether any pages in them are restricted.
- How staff sign in, and which Jira project tickets go to.
- Whether data must stay in a particular region.

**Not checked:** I had no network access, so four things the design relies on are unconfirmed:
- Confluence Cloud's search API.
- Pre-filling Jira's create screen from a link.
- Whether sign-in (IAP) works directly on Cloud Run or needs a load balancer.
- Vertex pricing.

Each one is an acceptance item in the goal that first depends on it. I ran no tests, since there is no code and google-adk isn't installed. The only checks were that the links between documents resolve, that no template placeholders are left, and that the estimates add up. Nothing is committed.

Next prompt for the ready goal:

```text
/adk-engineer Carry out G01 from docs/plans/helpdesk-assistant.md.
```