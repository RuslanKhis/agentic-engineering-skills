I've written the design and a three-phase plan for the expense assistant. Both are drafts: you weren't available, so every decision rests on an assumed answer, and none of them has been confirmed. I didn't write any code, and no tests ran, because there is no code yet and `google-adk` isn't installed here.

**What it is:** an internal tool for 40 known colleagues, read only. It is one ADK agent with three read-only tools:
- **Policy search:** looks up a reviewed copy of the expense policy and answers with the section it came from.
- **Claims lookup (two tools):** list your claims and show one claim, using fixed, reviewed SQL queries rather than model-written SQL.
- **Who you are:** comes from your Google Workspace sign-in, checked in code. The model never sees an employee ID it could swap, so users only ever see their own claims.

It runs on one Cloud Run instance behind Google's sign-in gateway (IAP). The model is `gemini-3.8-flash` on Vertex AI, with `gemini-3.5-flash` as the fallback.

**Capacity and cut line:** two engineers at half time for three weeks is about 54 focused hours.
- **Phase 1** is estimated at 32–43 hours (about 37 expected): one discovery task and five build goals, G01–G05.
- **If time runs short:** a policy-only assistant goes live first, before any personal data is added, so it's still useful on its own.
- **Phase 2** (G06–G10, about 25–35 hours) waits: database-level row restrictions, conversations that survive restarts, a policy publishing process, user feedback, and tests of attempts to read other people's claims.

Please confirm or move the cut line.

**Open decisions, each with a working assumption in the docs:**
- **Can finance staff see other employees' claims?** Their job often needs it. I assumed own claims only; changing that reshapes the security design.
- **The database:** I assumed Cloud SQL with Google-account database login and an email-to-employee table. A DBA needs to confirm this; the plan's discovery task covers it.
- **The policy documents:** where they live and who approves changes.
- **Region and data residency.**
- **Which GCP project to deploy to,** and your go-ahead for that and the access changes. Nothing cloud-side is authorised yet.
- **Unchecked facts:** I couldn't look up model availability on Vertex or prices, since network access wasn't allowed. They're acceptance checks in the plan.

The design is about 3,900 words, longer than the 2–4 pages the skill suggests for an internal tool; I didn't trim it. `REPORT.md` has the six sections you asked for.

The skill's next step for you to type:

```text
/adk-engineer Carry out G01 from docs/plans/expense-assistant.md.
```

Files are in `docs/`:
- `architecture/expense-assistant.md`
- `plans/expense-assistant.md`

`REPORT.md` is in the project root.